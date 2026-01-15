# optimized utilities for fast telegram rename bot
# speed focused, render friendly

import math
import time
import re
import datetime
import pytz
import os

from config import Config, rkn
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

# ===================== progress ===================== #

async def progress_for_pyrogram(current, total, ud_type, message, start):
    now = time.time()
    diff = now - start

    # update every 5 sec or on finish
    if current != total and diff < 5:
        return

    if diff <= 0:
        diff = 1

    percentage = (current / total) * 100
    speed = current / diff if diff else 0

    elapsed_ms = int(diff * 1000)
    remaining_ms = int(((total - current) / speed) * 1000) if speed > 0 else 0
    total_time = elapsed_ms + remaining_ms

    progress_bar = (
        "▣" * int(percentage // 5) +
        "▢" * (20 - int(percentage // 5))
    )

    # FIXED: String format fixed to avoid SyntaxError
    rkn_text = rkn.RKN_PROGRESS.format(
        round(percentage, 2),
        humanbytes(current),
        humanbytes(total),
        humanbytes(speed),
        TimeFormatter(total_time)
    )

    text = f"{ud_type}\n\n{progress_bar}\n{rkn_text}"

    try:
        await message.edit(
            text=text,
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton("✖️ ᴄᴀɴᴄᴇʟ ✖️", callback_data="close")]]
            )
        )
    except:
        pass

# ===================== helpers ===================== #

def humanbytes(size):
    if not size:
        return "0 b"

    power = 1024
    n = 0
    units = ["b", "kb", "mb", "gb", "tb"]

    while size >= power and n < len(units) - 1:
        size /= power
        n += 1

    return f"{round(size, 2)} {units[n]}"

def TimeFormatter(milliseconds: int) -> str:
    seconds, ms = divmod(int(milliseconds), 1000)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)

    out = []
    if days: out.append(f"{days}d")
    if hours: out.append(f"{hours}h")
    if minutes: out.append(f"{minutes}m")
    if seconds: out.append(f"{seconds}s")
    if ms: out.append(f"{ms}ms")

    return ", ".join(out) if out else "0s"

def convert(seconds):
    seconds %= 86400
    h = seconds // 3600
    seconds %= 3600
    m = seconds // 60
    s = seconds % 60
    return f"{h}:{m:02d}:{s:02d}"

# ===================== logs ===================== #

async def send_log(bot, user):
    if not Config.LOG_CHANNEL:
        return

    now = datetime.datetime.now(pytz.timezone("Asia/Kolkata"))
    # ʟᴏɢɢɪɴɢ ɪɴ sᴍᴀʟʟ ᴄᴀᴘs ᴀs ᴘᴇʀ ʏᴏᴜʀ ʀᴇǫᴜᴇsᴛ
    text = (
        "**ɴᴇᴡ ᴜsᴇʀ sᴛᴀʀᴛᴇᴅ ʙᴏᴛ**\n\n"
        f"ᴜsᴇʀ: {user.mention}\n"
        f"ɪᴅ: `{user.id}`\n"
        f"ᴜsᴇʀɴᴀᴍᴇ: @{user.username}\n\n"
        f"ᴅᴀᴛᴇ: {now.strftime('%d %b %Y')}\n"
        f"ᴛɪᴍᴇ: {now.strftime('%I:%M:%S %p')}\n\n"
        f"ʙʏ: {bot.mention}"
    )

    await bot.send_message(Config.LOG_CHANNEL, text)

# ===================== time parser ===================== #

async def get_seconds_first(time_string):
    factors = {
        "s": 1,
        "min": 60,
        "hour": 3600,
        "day": 86400,
        "month": 2592000,
        "year": 31536000
    }

    parts = time_string.lower().split()
    total = 0

    for i in range(0, len(parts), 2):
        if i + 1 < len(parts):
            try:
                total += int(parts[i]) * factors.get(parts[i + 1].rstrip("s"), 0)
            except:
                pass

    return total

async def get_seconds(time_string):
    factors = {
        "s": 1,
        "min": 60,
        "hour": 3600,
        "day": 86400,
        "month": 2592000,
        "year": 31536000
    }

    total = 0
    matches = re.findall(r"(\d+)\s*(\w+)", time_string.lower())

    for value, unit in matches:
        total += int(value) * factors.get(unit.rstrip("s"), 0)

    return total

# ===================== file helpers ===================== #

async def add_prefix_suffix(filename, prefix="", suffix=""):
    base, ext = os.path.splitext(filename)
    return f"{prefix} {base} {suffix}{ext}".strip()

async def remove_path(*paths):
    for path in paths:
        if path and os.path.exists(path):
            os.remove(path)
