# telegram auto rename bot
# maintained by @OveshBossOfficial
# optimized for high speed & render support

import aiohttp
import asyncio
import warnings
import pytz
import datetime
import logging
import glob
import sys
import importlib.util
from pathlib import Path

from pyrogram import Client, errors, idle, __version__

from config import Config
from plugins.web_support import web_server
from plugins.file_rename import app

# ================= logging ================= #

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("bot.log"),
        logging.StreamHandler()
    ]
)

logging.getLogger("pyrogram").setLevel(logging.WARNING)
logging.getLogger("pyrofork").setLevel(logging.WARNING)

# ================= bot class ================= #

class AutoRenameBot(Client):
    def __init__(self):
        super().__init__(
            name="autorenamebot",
            api_id=Config.API_ID,
            api_hash=Config.API_HASH,
            bot_token=Config.BOT_TOKEN,
            workers=300,
            plugins={"root": "plugins"},
            sleep_threshold=10,
            max_concurrent_transmissions=100
        )

    async def start(self):
        try:
            await super().start()
        except errors.AuthKeyUnregistered:
            print("❌ string session expired.")
            return

        me = await self.get_me()
        self.username = me.username
        self.mention = me.mention
        Config.BOT = self
        self.uptime = Config.BOT_UPTIME

        # ================= web server ================= #
        runner = aiohttp.web.AppRunner(await web_server())
        await runner.setup()
        site = aiohttp.web.TCPSite(runner, "0.0.0.0", Config.PORT)
        await site.start()

        # ================= load plugins ================= #
        for file in glob.glob("plugins/*.py"):
            path = Path(file)
            name = path.stem
            spec = importlib.util.spec_from_file_location(f"plugins.{name}", file)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            sys.modules[f"plugins.{name}"] = module
            print(f"✅ plugin loaded: {name}")

        print(f"🚀 bot started successfully as {me.first_name.lower()}")

        # ================= log channel ================= #
        if Config.LOG_CHANNEL:
            try:
                now = datetime.datetime.now(pytz.timezone("Asia/Kolkata"))
                await self.send_message(
                    Config.LOG_CHANNEL,
                    f"✅ **bot restarted successfully**\n\n"
                    f"👤 owner: @oveshbossofficial\n"
                    f"📅 date: `{now.strftime('%d %b %y').lower()}`\n"
                    f"⏰ time: `{now.strftime('%i:%m:%s %p').lower()}`\n"
                    f"⚙️ pyrogram: `{__version__.lower()}`"
                )
            except:
                pass

    async def stop(self, *args):
        await super().stop()
        print("❌ bot stopped")

# ================= start services ================= #

bot = AutoRenameBot()

async def main():
    try:
        if Config.STRING_SESSION:
            try:
                await app.start()
            except Exception as e:
                print(f"user session error: {str(e).lower()}")

        await bot.start()
        await idle()

    except Exception as e:
        print(f"runtime error: {str(e).lower()}")

    finally:
        if Config.STRING_SESSION:
            try:
                await app.stop()
            except:
                pass
        await bot.stop()

if __name__ == "__main__":
    warnings.filterwarnings("ignore")
    asyncio.get_event_loop().run_until_complete(main())
