# (c) @RknDeveloperr
# Maintained by @OveshBossOfficial

import aiohttp, asyncio, warnings, pytz, datetime
import logging, glob, sys, importlib.util
from pathlib import Path
from pyrogram import Client, idle, errors
from config import Config
from plugins.web_support import web_server

# Safe Import for 'app'
try:
    from plugins.file_rename import app
except ImportError:
    app = None

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(message)s")

class DigitalAutoRenameBot(Client):
    def __init__(self):
        super().__init__(
            name="DigitalRenameBot",
            api_id=Config.API_ID, api_hash=Config.API_HASH, bot_token=Config.BOT_TOKEN,
            workers=200, plugins={"root": "plugins"}
        )
                
    async def start(self):
        await super().start()
        me = await self.get_me()
        Config.BOT = self
        
        # Start Web Server
        runner = aiohttp.web.AppRunner(await web_server())
        await runner.setup()
        await aiohttp.web.TCPSite(runner, "0.0.0.0", Config.PORT).start()
        
        # --- AI POWERED WELCOME MESSAGE ---
        welcome_text = (
            f"🚀 **{me.first_name.upper()} ɪs ɴᴏᴡ ᴀʟɪᴠᴇ!**\n\n"
            f"🤖 **ᴍᴏᴅᴇ:** `ᴀɪ-ᴘᴏᴡᴇʀᴇᴅ ᴜʟᴛʀᴀ ғᴀsᴛ`\n"
            f"⚡ **ᴇɴɢɪɴᴇ:** `sᴜᴘᴇʀ sᴏɴɪᴄ v3`\n\n"
            f"🌟 **ᴘᴏᴡᴇʀᴇᴅ ʙʏ: @OveshBossOfficial**"
        )

        for admin_id in Config.ADMIN:
            try: await self.send_message(admin_id, welcome_text)
            except: pass
                    
        if Config.LOG_CHANNEL:
            curr = datetime.datetime.now(pytz.timezone("Asia/Kolkata"))
            log_msg = (
                f"✨ **{me.mention} ʀᴇsᴛᴀʀᴛᴇᴅ sᴜᴄᴄᴇssғᴜʟʟʏ !!**\n\n"
                f"📅 **ᴅᴀᴛᴇ :** `{curr.strftime('%d %B, %Y')}`\n"
                f"🚀 **ᴇɴɢɪɴᴇ :** `ᴀɪ ᴘᴏᴡᴇʀᴇᴅ ᴘᴏᴡᴇʀғᴜʟ`\n\n"
                f"👑 **ᴘᴏᴡᴇʀᴇᴅ ʙʏ : @OveshBossOfficial**"
            )
            try: await self.send_message(Config.LOG_CHANNEL, log_msg)
            except: print("Make Bot Admin in Log Channel!")

    async def stop(self, *args):
        await super().stop()

digital_instance = DigitalAutoRenameBot()

async def start_services():
    # Start User Session if exists
    if Config.STRING_SESSION and app:
        try: await app.start()
        except Exception as e: print(f"User Session Error: {e}")
    
    await digital_instance.start()
    await idle()

if __name__ == "__main__":
    warnings.filterwarnings("ignore")
    asyncio.get_event_loop().run_until_complete(start_services())
