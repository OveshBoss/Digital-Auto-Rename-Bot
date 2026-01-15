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

    # edit only every ~5 sec or on finish (huge speed gain)
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

    text = (
        f"{ud_type}\n\n"
        f"{progress_bar}"
        f"{rkn.RKN_PROGRESS.format( round(percentage,2), humanbytes(current), humanbytes(total), humanbytes(speed), TimeFormatter(total_time) )}"
    )

    try:
        await message.edit(
            text=text,
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton("✖️ cancel ✖️", callback_data="close")]]
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

    return f"{round(size,2)} {units[n]}"

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

    return ", ".join(out)

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
    text = (
        "**new user started bot**\n\n"
        f"user: {user.mention}\n"
        f"id: `{user.id}`\n"
        f"username: @{user.username}\n\n"
        f"date: {now.strftime('%d %b %Y')}\n"
        f"time: {now.strftime('%I:%M:%S %p')}\n\n"
        f"by: {bot.mention}"
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

    parts = time_string.split()
    total = 0

    for i in range(0, len(parts), 2):
        try:
            total += int(parts[i]) * factors.get(parts[i+1].rstrip("s"), 0
