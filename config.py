# ultra fast config for telegram auto rename bot
# tuned for render + high speed downloading

import os
import re
import time

id_pattern = re.compile(r"^-?\d+$")

class Config:

    # ================= telegram ================= #
    API_ID = int(os.environ.get("API_ID", "23903140"))
    API_HASH = os.environ.get("API_HASH", "579f1bcf3eac1660d81ef34b09906012")
    BOT_TOKEN = os.environ.get("BOT_TOKEN", "")

    STRING_SESSION = os.environ.get("STRING_SESSION", "")
    BOT = None

    # ================= database ================= #
    DB_NAME = os.environ.get("DB_NAME", "digital_auto_rename_bot")
    DB_URL = os.environ.get(
        "DB_URL",
        "mongodb+srv://peyofip118_db_user:OYjWsF84H4ah69Gd@cluster0.scovtfc.mongodb.net/?appName=Cluster0"
    )

    # ================= admin ================= #
    ADMIN = [
        int(x) if id_pattern.match(x) else x
        for x in os.environ.get("ADMIN", "1416433622").split()
    ]

    LOG_CHANNEL = int(os.environ.get("LOG_CHANNEL", "-1003166629808"))

    # ================= force sub ================= #
    FORCE_SUB = os.environ.get("FORCE_SUB", "")
    try:
        FORCE_SUB = int(FORCE_SUB)
    except:
        pass

    # ================= limits ================= #
    FREE_UPLOAD_LIMIT = 6 * 1024 * 1024 * 1024  # 6gb
    UPLOAD_LIMIT_MODE = True
    PREMIUM_MODE = True

    # ================= speed tuning ================= #
    # (used indirectly by bot.py & utils)
    MAX_DOWNLOAD_WORKERS = 100
    MAX_UPLOAD_WORKERS = 100
    PROGRESS_UPDATE_GAP = 5  # seconds (less edit = more speed)
    FAST_MODE = True

    # ================= misc ================= #
    RKN_PIC = os.environ.get(
        "RKN_PIC",
        "https://graph.org/file/fc480c25a52ffb1a6363b-3e0e68a18b9f7a0517.jpg"
    )

    PORT = int(os.environ.get("PORT", "8080"))
    BOT_UPTIME = time.time()


# ================= text constants ================= #

class rkn:

    START_TXT = """<b>hi, {} 👋

this is a super fast and powerful auto rename bot.

you can rename files, change thumbnails,
and convert video ↔ file easily.

powered and maintained by @oveshbossofficial</b>"""

    ABOUT_TXT = """<b>
╭───────────⍟
├ 🤖 name : {}
├ 🖥 developers : {}
├ 👨‍💻 programmer : {}
├ 📕 library : {}
├ ✏️ language : {}
├ 💾 database : {}
├ 📊 version : {}
╰───────────────⍟
</b>"""

    HELP_TXT = """<b>
• /start – start the bot

✏️ how to rename:
• send any file
• send new filename
</b>"""

    THUMBNAIL = """<b>
how to set thumbnail:
• send photo
• use /setthumb
</b>"""

    CAPTION = """<b>
how to set caption:
• use /setcaption
</b>"""

    BOT_STATUS = """⚡ bot status"""
    LIVE_STATUS = """⚡ server status"""

    DEV_TXT = """<b>
special thanks & developers
• ovesh boss
</b>"""

    RKN_PROGRESS = """<b>
╭━━━━━━━━◉🚀◉━━━━━━━━╮
┃ processing...
┣━━━━━━━━━━━━━━━━━━━━╯
┣ size: {1} | {2}
┣ done: {0}%
┣ speed: {3}/s
┣ eta: {4}
╰━━━━━━━━◉🔥◉━━━━━━━━╯
</b>"""
