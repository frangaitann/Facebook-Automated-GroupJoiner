import asyncio
from modules.misc import *
from modules.web import *

async def main():
    async with web_driver() as page:
        await group_joiner(page)

if __name__ == "__main__":
    asyncio.run(main())