from playwright.async_api import async_playwright, Error
from playwright_stealth import Stealth
from modules.misc import *
import random
import logging
from contextlib import asynccontextmanager


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s') 
logger = logging.getLogger(__name__)


@asynccontextmanager
async def web_driver():
    async with Stealth().use_async(async_playwright()) as p:
            browser = await p.chromium.launch(
                headless=False,
                args=[
                    '--log-level=3',
                    '--disable_notifications',
                    '--disable-search-engine-choice-screen',
                    '--disable-blink-features=AutomationControlled'
                ],
            )
            
            page = await browser.new_page(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                        "AppleWebKit/537.36 (KHTML, like Gecko) "
                        "Chrome/134.0.0.0 Safari/537.36",
                locale="en-US",
                timezone_id="America/Argentina/Buenos_Aires",
                        
            )
            
            await page.goto("https://www.facebook.com")
            await cookies(page)
            
            await page.mouse.wheel(0, random.uniform(23, 732))
            try:
                csv_log("driver", "Browser launched and Facebook opened.", "", "INFO")
                yield page
            except Exception as e:
                logger.error(f"Error in web driver: {e}")
                csv_log("driver", f"Error in web driver: {e}", "", "ERROR")
                raise
            finally:
                await browser.close()


@sleeper_f
async def group_joiner(page):
    """For each group in groups.csv, finds the URL and joins to it."""

    with open(groups_file, "r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for row in reader:
            group_name = row["NAME"]
            url = row["URL"]
            
            try:
                await page.goto(url)
                await sleeper(3, 10)
                await page.mouse.wheel(0, random.uniform(14, 562))
                join_button = page.locator("//html/body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div[1]/div[2]/div/div/div/div/div[2]/div/div[1]/div/div/div").first or page.locator("//html/body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div[1]/div[2]/div/div/div/div/div[2]/div/div[1]/div").first

                button_text = page.get_by_role("button", name="Join group").first or page.get_by_text("Join group").first
                try:
                    await button_text.wait_for(timeout=5000)
                except Error as e:
                    logger.warning(f"Join button text not found for {group_name} or already joined. | ERROR: {e}")
                    continue

                await join_button.wait_for(timeout=5000)
                await join_button.click()
                await sleeper(5, 14)

                await page.mouse.wheel(0, random.uniform(14, 562))
                logger.info(f"Joined {group_name} successfully.")
                csv_log("join", f"Joined {group_name} successfully.", group_name, "INFO")

            except Exception as e:
                logger.error(f"Error occurred while joining {group_name}: {e}")
                csv_log("join", f"Error occurred while joining {group_name}: {e}", group_name, "ERROR")