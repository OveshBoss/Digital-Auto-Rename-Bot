# (c) @RknDeveloperr
# Optimized for 10MB/s+ Speed on Render

import aiohttp, asyncio, warnings, pytz, datetime
import logging
import logging.config
import glob, sys
import importlib.util
from pathlib import Path

# pyrogram imports
from pyrogram import Client, __version__, errors
from pyrogram.raw.all import layer
from pyrogram import idle

# bots imports
from config import Config
from plugins.web_support import web_server
from plugins.file_rename import app

# Logging configuration
logging.basicConfig(
    level=logging.INFO, 
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler('BotLog.txt'), logging.StreamHandler()]
)
logging.getLogger("pyrofork").setLevel(logging.WARNING)
logging.getLogger("pyrogram").setLevel(logging.WARNING)

class DigitalAutoRenameBot(Client):
    def __init__(self):
        super().__init__(
            name="DigitalRenameBot",
            api_id=Config.API_ID,
            api_hash=Config.API_HASH,
            bot_token=Config.BOT_TOKEN,
            workers=300, # Increased for speed
            plugins={"root": "plugins"},
            sleep_threshold=10,
            max_concurrent_transmissions=100 # Fast Upload/Download
        )
                
    async def start(self):
        try:
            await super().start()
        except errors.AuthKeyUnregistered:
            print("❌ ERROR: String Session expire ho gaya hai! Naya session generate karein.")
            return

        me = await self.get_me()
        self.mention = me.mention
        self.username = me.username  
        self.uptime = Config.BOT_UPTIME
        Config.BOT = self
        
        # Web server for Render 24/7
        app_runner = aiohttp.web.AppRunner(await web_server())
        await app_runner.setup()
        await aiohttp.web.TCPSite(app_runner, "0.0.0.0", Config.PORT).start()
        
        # Load Plugins
        path = "plugins/*.py"
        for name in glob.glob(path):
            patt = Path(name)
            plugin_name = patt.stem
            import_path = f"plugins.{plugin_name}"
            spec = importlib.util.spec_from_file_location(import_path, name)
            load = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(load)
            sys.modules[import_path] = load
            print(f"✅ Imported: {plugin_name}")
                
        print(f"🚀 {me.first_name} is Started with High Speed Mode!")

        # Log Channel Notification
        if Config.LOG_CHANNEL:
            try:
                curr = datetime.datetime.now(pytz.timezone("Asia/Kolkata"))
                await self.send_message(Config.LOG_CHANNEL, f"**{me.mention} Is Restarted!**\n\n📅 Date: `{curr.strftime('%d %B, %Y')}`\n🉐 Version: `v{__version__}`")
                # User login log in small caps as per instructions
                print(f"ʟᴏɢ: ʙᴏᴛ sᴛᴀʀᴛᴇᴅ ʙʏ ᴜsᴇʀ ᴀᴛ {curr}")
            except: pass

    async def stop(self, *args):
        await super().stop()
        print("Bot Stopped.")

digital_instance = DigitalAutoRenameBot()

async def start_services():
    try:
        # Start user app (Premium) and bot instance
        if Config.STRING_SESSION:
            try:
                await app.start()
            except Exception as e:
                print(f"❌ User Session Error: {e}")
            
        await digital_instance.start()
        await idle()
    except Exception as e:
        print(f"❌ Runtime Error: {e}")
    finally:
        if Config.STRING_SESSION:
            try: await app.stop() 
            except: pass
        await digital_instance.stop()

if __name__ == "__main__":
    warnings.filterwarnings("ignore")
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(start_services())
    except KeyboardInterrupt:
        pass
    except Exception as e:
        print(f"Fatal Error: {e}")
