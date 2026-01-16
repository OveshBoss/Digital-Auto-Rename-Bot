# (c) @RknDeveloperr
# Rkn Developer 
# Don't Remove Credit 😔
# Telegram Channel @RknDeveloper & @Rkn_Botz
# Developer @RknDeveloperr
# Special Thanks To @ReshamOwner
# Update Channel @Digital_Botz & @DigitalBotz_Support

# extra imports
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

# Get logging configurations
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler('BotLog.txt'),
             logging.StreamHandler()]
)
logging.getLogger("pyrofork").setLevel(logging.WARNING)

class DigitalAutoRenameBot(Client):
    def __init__(self):
        super().__init__(
            name="DigitalRenameBot",
            api_id=Config.API_ID,
            api_hash=Config.API_HASH,
            bot_token=Config.BOT_TOKEN,
            workers=300, # Fast processing
            plugins={"root": "plugins"},
            sleep_threshold=10, # Speed ke liye zaroori
            max_concurrent_transmissions=100 # ULTRA FAST DOWNLOAD/UPLOAD
        )


    async def start(self):
        await super().start()
        me = await self.get_me()
        self.mention = me.mention
        self.username = me.username  
        self.uptime = Config.BOT_UPTIME
        self.premium = Config.PREMIUM_MODE
        self.uploadlimit = Config.UPLOAD_LIMIT_MODE
        Config.BOT = self

        app_runner = aiohttp.web.AppRunner(await web_server())
        await app_runner.setup()
        bind_address = "0.0.0.0"
        await aiohttp.web.TCPSite(app_runner, bind_address, Config.PORT).start()

        # LOGGING IN SMALL CAPS AS REQUESTED
        print(f"🚀 {me.first_name.lower()} sᴛᴀʀᴛᴇᴅ sᴜᴄᴄᴇssғᴜʟʟʏ")


        for id in Config.ADMIN:
            if Config.STRING_SESSION:
                try: await self.send_message(id, f"𝟮𝗚𝗕+ ғɪʟᴇ sᴜᴘᴘᴏʀᴛ ʜᴀs ʙᴇᴇɴ ᴀᴅᴅᴇᴅ ᴛᴏ ʏᴏᴜʀ ʙᴏᴛ.\n\nNote: 𝐓𝐞𝐥𝐞𝐠𝐫𝐚𝐦 𝐩𝐫𝐞𝐦𝐢𝐮𝐦 𝐚𝐜𝐜𝐨𝐮𝐧𝐭 𝐬𝐭𝐫𝐢𝐧𝐠 𝐬𝐞𝐬𝐬𝐢𝐨𝐧 𝐫𝐞𝐪𝐮𝐢𝐫𝐞𝐝 𝐓𝐡𝐞𝐧 𝐬𝐮𝐩𝐩𝐨𝐫𝐭𝐬 𝟐𝐆𝐁+ 𝐟𝐢𝐥𝐞𝐬.\n\n**__{me.first_name}  Iꜱ Sᴛᴀʀᴛᴇᴅ.....✨️__**")                                
                except: pass
            else:
                try: await self.send_message(id, f"𝟮𝗚𝗕- ғɪʟᴇ sᴜᴘᴘᴏʀᴛ ʜᴀs ʙᴇᴇɴ ᴀᴅᴅᴇᴅ ᴛᴏ ʏᴏᴜʀ ʙᴏᴛ.\n\n**__{me.first_name}  Iꜱ Sᴛᴀʀᴛᴇᴅ.....✨️__**")                                
                except: pass

        if Config.LOG_CHANNEL:
            try:
                curr = datetime.datetime.now(pytz.timezone("Asia/Kolkata"))
                date = curr.strftime('%d %B, %Y')
                time = curr.strftime('%I:%M:%S %p')
                await self.send_message(Config.LOG_CHANNEL, f"**__{me.mention} Iꜱ Rᴇsᴛᴀʀᴛᴇᴅ !!**\n\n📅 Dᴀᴛᴇ : `{date}`\n⏰ Tɪᴍᴇ : `{time}`\n🌐 Tɪᴍᴇᴢᴏɴᴇ : `Asia/Kolkata`\n\n🉐 Vᴇʀsɪᴏɴ : `v{__version__} (Layer {layer})`</b>")                                
            except:
                print("Pʟᴇᴀꜱᴇ Mᴀᴋᴇ Tʜɪꜱ Iꜱ Aᴅᴍɪɴ Iɴ Yᴏᴜʀ Lᴏɢ Cʜᴀɴɴᴇʟ")

    async def stop(self, *args):
        for id in Config.ADMIN:
            try: await self.send_message(id, f"**Bot Stopped....**")                                
            except: pass

        print("Bot Stopped 🙄")
        await super().stop()


digital_instance = DigitalAutoRenameBot()

def main():
    async def start_services():
        if Config.STRING_SESSION:
            await asyncio.gather(app.start(), digital_instance.start())
        else:
            await asyncio.gather(digital_instance.start())

        await idle()

        if Config.STRING_SESSION:
            await asyncio.gather(app.stop(), digital_instance.stop())
        else:
            await asyncio.gather(digital_instance.stop())

    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(start_services())
    except KeyboardInterrupt:
        print("\n🛑 Bot stopped by user!")
    finally:
        loop.close()

if __name__ == "__main__":
    warnings.filterwarnings("ignore", message="There is no current event loop")
    try:
        main()
    except errors.FloodWait as ft:
        asyncio.run(asyncio.sleep(ft.value))
        main()
