# (c) @RknDeveloperr
# Maintained by @OveshBossOfficial
# Optimized for High Speed & Render Support

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
from pyrogram.raw.all import layer

from config import Config
from plugins.web_support import web_server

# ================= logging ================= #

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
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
            print("❌ ᴇʀʀᴏʀ: sᴛʀɪɴɢ sᴇssɪᴏɴ ᴇxᴘɪʀᴇᴅ. ᴜᴘᴅᴀᴛᴇ ɪɴ ʀᴇɴᴅᴇʀ!")
            return

        me = await self.get_me()
        self.username = me.username
        self.mention = me.mention
        Config.BOT = self
        
        # ================= web server ================= #
        runner = aiohttp.web.AppRunner(await web_server())
        await runner.setup()
        await aiohttp.web.TCPSite(runner, "0.0.0.0", Config.PORT).start()

        # ================= load plugins ================= #
        # Note: file_rename.py is automatically loaded by the plugins dict in __init__
        # Manual loading is removed to prevent 'ImportError' and conflicts
        
        print(f"🚀 ʙᴏᴛ sᴛᴀʀᴛᴇᴅ sᴜᴄᴄᴇssғᴜʟʟʏ ᴀs {me.first_name.lower()}")

        # ================= log channel ================= #
        if Config.LOG_CHANNEL:
            try:
                curr = datetime.datetime.now(pytz.timezone("Asia/Kolkata"))
                # Attractive Welcome Message for Admin/Logs
                log_msg = (
                    f"🚀 **{me.first_name.upper()} ɪs ɴᴏᴡ ᴀʟɪᴠᴇ!**\n\n"
                    f"🤖 **ᴍᴏᴅᴇ:** `ᴀɪ-ᴘᴏᴡᴇʀᴇᴅ ᴜʟᴛʀᴀ ғᴀsᴛ`\n"
                    f"⚡ **ᴇɴɢɪɴᴇ:** `sᴜᴘᴇʀ sᴏɴɪᴄ 10ᴍʙ/s+`\n"
                    f"📂 **sᴛᴀᴛᴜs:** `ᴘᴏᴡᴇʀғᴜʟ ʀᴇɴᴀᴍᴇ ᴀᴄᴛɪᴠᴀᴛᴇᴅ`\n"
                    f"📅 **ᴅᴀᴛᴇ:** `{curr.strftime('%d %b %Y').lower()}`\n\n"
                    f"🌟 **ᴘᴏᴡᴇʀᴇᴅ ʙʏ: @OveshBossOfficial**\n"
                    f"✨ **ᴅᴇᴠᴇʟᴏᴘᴇᴅ ʙʏ: @RknDeveloperr**"
                )
                await self.send_message(Config.LOG_CHANNEL, log_msg)
            except Exception as e:
                print(f"ʟᴏɢ ᴄʜᴀɴɴᴇʟ ᴇʀʀᴏʀ: {e}")

    async def stop(self, *args):
        await super().stop()
        print("❌ ʙᴏᴛ sᴛᴏᴘᴘᴇᴅ")

# ================= start services ================= #

bot = AutoRenameBot()

async def main():
    # Dynamically import app only if STRING_SESSION exists
    user_app = None
    if Config.STRING_SESSION:
        try:
            from plugins.file_rename import app as user_app
            await user_app.start()
            print("✅ ᴜsᴇʀ sᴇssɪᴏɴ (ᴘʀᴇᴍɪᴜᴍ) sᴛᴀʀᴛᴇᴅ")
        except Exception as e:
            print(f"❌ ᴜsᴇʀ sᴇssɪᴏɴ ᴇʀʀᴏʀ: {str(e).lower()}")

    try:
        await bot.start()
        await idle()
    except Exception as e:
        print(f"❌ ʀᴜɴᴛɪᴍᴇ ᴇʀʀᴏʀ: {str(e).lower()}")
    finally:
        if user_app:
            await user_app.stop()
        await bot.stop()

if __name__ == "__main__":
    warnings.filterwarnings("ignore")
    try:
        asyncio.get_event_loop().run_until_complete(main())
    except KeyboardInterrupt:
        pass
