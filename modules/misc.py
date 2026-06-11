import csv
import os
import pickle
import asyncio
import random
from datetime import datetime

BASE_PATH = os.path.dirname(os.path.abspath(__file__))
cookies_file = os.path.join(BASE_PATH, 'cookies.pkl')
groups_file = os.path.join(BASE_PATH, 'groups.csv')
logs_file = os.path.join(BASE_PATH, 'logs.csv')


async def sleeper(min_t:int=5 ,max_t:int=18):
    sleeping_time= random.uniform(min_t, max_t)
    await asyncio.sleep(sleeping_time)


def sleeper_f(func):    # Dumb way to use decorators but for showing how decorators work and just for not being that simple ;)
    async def wrapper(*args, **kwargs):
        await sleeper()
        result = await func(*args, **kwargs)
        await sleeper()
        return result
    return wrapper



def csv_log(category, message, group_name="", level="INFO"):
    """Append one log row to logs.csv with category and severity."""
    write_header = not os.path.exists(logs_file)
    with open(logs_file, "a", newline="", encoding="utf-8") as logf:
        writer = csv.writer(logf)
        if write_header:
            writer.writerow(["timestamp", "category", "level", "group", "message"])
        writer.writerow([datetime.now().isoformat(timespec="seconds"), category, level, group_name, message])

@sleeper_f
async def cookies(page):
    """Function used for loading cookies from cookies.pkl file"""
    
    if os.path.exists(cookies_file) and os.path.isfile(cookies_file):

        cookies = pickle.load(open(cookies_file, "rb"))
        await page.context.clear_cookies()
        for i in cookies:

            cookie_dict = {
                "domain": i["domain"],
                "httponly": i["httponly"],
                "name": i["name"],
                "path": i["path"],
                "samesite": i["samesite"],
                "secure": i["secure"],
                "value": i["value"]
            }

            await page.context.add_cookies([cookie_dict])

        await page.reload()

    else:
        raise Exception("cookies.pkl not found")