# (c) @RknDeveloperr
# Rkn Developer 
# Don't Remove Credit 😔
# Telegram Channel @RknDeveloper & @Rkn_Botz
# Developer @RknDeveloperr
# Special Thanks To @ReshamOwner
# Update Channel @Digital_Botz & @DigitalBotz_Support
"""
Apache License 2.0
Copyright (c) 2025 @Digital_Botz
"""

import re, os, time
id_pattern = re.compile(r'^.\d+$') 

class Config(object):
    API_ID = os.environ.get("API_ID", "23903140")
    API_HASH = os.environ.get("API_HASH", "579f1bcf3eac1660d81ef34b09906012")
    BOT_TOKEN = os.environ.get("BOT_TOKEN", "") 
    BOT = None

    STRING_SESSION = os.environ.get("STRING_SESSION", "")
    
    DB_NAME = os.environ.get("DB_NAME","Digital_Auto_Rename_Bot")     
    DB_URL = os.environ.get(
        "DB_URL",
        "mongodb+srv://peyofip118_db_user:OYjWsF84H4ah69Gd@cluster0.scovtfc.mongodb.net/?appName=Cluster0"
    )
 
    RKN_PIC = os.environ.get(
        "RKN_PIC",
        "https://graph.org/file/fc480c25a52ffb1a6363b-3e0e68a18b9f7a0517.jpg"
    )
    ADMIN = [
        int(admin) if id_pattern.search(admin) else admin
        for admin in os.environ.get('ADMIN', '1416433622').split()
    ]
    LOG_CHANNEL = int(os.environ.get("LOG_CHANNEL", "-1003166629808"))

    FREE_UPLOAD_LIMIT = 6442450944

    UPLOAD_LIMIT_MODE = True 
    PREMIUM_MODE = True 
    
    try:
        FORCE_SUB = int(os.environ.get("FORCE_SUB", "-1002342243776")) 
    except:
        FORCE_SUB = os.environ.get("FORCE_SUB", "Digital_Botz")
        
    PORT = int(os.environ.get("PORT", "8080"))
    BOT_UPTIME = time.time()


class rkn(object):

    START_TXT = """<b>ʜɪ, {} 👋

ᴛʜɪs ɪs ᴀɴ ᴀᴅᴠᴀɴᴄᴇᴅ ᴀɴᴅ ʏᴇᴛ ᴘᴏᴡᴇʀꜰᴜʟ ʀᴇɴᴀᴍᴇ ʙᴏᴛ.

ᴜꜱɪɴɢ ᴛʜɪꜱ ʙᴏᴛ ʏᴏᴜ ᴄᴀɴ ʀᴇɴᴀᴍᴇ ᴀɴᴅ ᴄʜᴀɴɢᴇ ᴛʜᴜᴍʙɴᴀɪʟ ᴏꜰ ʏᴏᴜʀ ꜰɪʟᴇꜱ.

ʏᴏᴜ ᴄᴀɴ ᴀʟꜱᴏ ᴄᴏɴᴠᴇʀᴛ ᴠɪᴅᴇᴏ ᴛᴏ ꜰɪʟᴇ ᴀɴᴅ ꜰɪʟᴇ ᴛᴏ ᴠɪᴅᴇᴏ ɪɴ ᴍɪɴᴜᴛᴇs.

ᴛʜɪꜱ ʙᴏᴛ ᴀʟꜱᴏ ꜱᴜᴘᴘᴏʀᴛꜱ ᴄᴜꜱᴛᴏᴍ ᴛʜᴜᴍʙɴᴀɪʟ ᴀɴᴅ ᴄᴜꜱᴛᴏᴍ ᴄᴀᴘᴛɪᴏɴ ᴀɴᴅ ᴀɪ ᴘᴏᴡᴇʀᴇᴅ.

ᴛʜɪꜱ ʙᴏᴛ ᴡᴀꜱ ᴄʀᴇᴀᴛᴇᴅ ʙʏ : @OveshBossOfficial </b>"""

    ABOUT_TXT = """<b>╭───────────⍟
├🤖 ᴍy ɴᴀᴍᴇ : {}
├🖥️ Dᴇᴠᴇʟᴏᴩᴇʀꜱ : {}
├👨‍💻 Pʀᴏɢʀᴀᴍᴇʀ : {}
├📕 Lɪʙʀᴀʀy : {}
├✏️ Lᴀɴɢᴜᴀɢᴇ: {}
├💾 Dᴀᴛᴀ Bᴀꜱᴇ: {}
├📊 ᴠᴇʀsɪᴏɴ: <a href=https://github.com/DigitalBotz/Digital-Auto-Rename-Bot>{}</a></b>     
╰───────────────⍟ """

    HELP_TXT = """
<b>•></b> /start Tʜᴇ Bᴏᴛ.

✏️ <b><u>Hᴏᴡ Tᴏ Rᴇɴᴀᴍᴇ A Fɪʟᴇ</u></b>
<b>•></b> Sᴇɴᴅ Aɴy Fɪʟᴇ Aɴᴅ Tyᴩᴇ Nᴇᴡ Fɪʟᴇ Nᴀᴍᴇ
"""

    THUMBNAIL = """
🌌 <b><u>Hᴏᴡ Tᴏ Sᴇᴛ Tʜᴜᴍʙɴɪʟᴇ</u></b>
"""

    CAPTION = """
📑 <b><u>Hᴏᴡ Tᴏ Sᴇᴛ Cᴜꜱᴛᴏᴍ Cᴀᴩᴛɪᴏɴ</u></b>
"""

    BOT_STATUS = """
⚡️ ʙᴏᴛ sᴛᴀᴛᴜs ⚡️
"""

    LIVE_STATUS = """
⚡ ʟɪᴠᴇ sᴇʀᴠᴇʀ sᴛᴀᴛᴜs ⚡
"""

    DEV_TXT = """<b><u>Sᴩᴇᴄɪᴀʟ Tʜᴀɴᴋꜱ & Dᴇᴠᴇʟᴏᴩᴇʀꜱ</u></b>

• ❣️ <a href=https://github.com/r>RknDeloper</a>
• ❣️ <a href=https://github.com/DiBotz>DigalBz</a>
"""

    RKN_PROGRESS = """<b>
╭━━━━━━━━◉🚀◉━━━━━━━━╮
┃   𝗥𝗞𝗡 𝗣𝗥𝗢𝗖𝗘𝗦𝗦𝗜𝗡𝗚...❱━➣  
┣━━━━━━━━━━━━━━━━━━━━╯
┣⪼ 📦 𝗦𝗜𝗭𝗘: {1} | {2}
┣⪼ 📊 𝗗𝗢𝗡𝗘: {0}%
┣⪼ 🚀 𝗦𝗣𝗘𝗘𝗗: {3}/s
┣⪼ ⏰ 𝗘𝗧𝗔: {4}
╰━━━━━━━━◉🔥◉━━━━━━━━╯</b>"""
