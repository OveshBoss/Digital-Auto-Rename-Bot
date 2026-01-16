# (c) @RknDeveloperr
# Rkn Developer 

from pyrogram import Client, filters
from pyrogram.enums import MessageMediaType
from pyrogram.file_id import FileId
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from hachoir.metadata import extractMetadata
from hachoir.parser import createParser
from PIL import Image

from helper.utils import progress_for_pyrogram, convert, humanbytes, remove_path
from helper.database import digital_botz
from config import Config
from plugins.auto_rename import EnhancedAutoRenamer

import os, time, asyncio

UPLOAD_TEXT = "🚀 Uploading..."
DOWNLOAD_TEXT = "⚡ Downloading..."

renamer = EnhancedAutoRenamer()

# User Session (Premium) setup
app = Client("UserSession", api_id=Config.API_ID, api_hash=Config.API_HASH, session_string=Config.STRING_SESSION) if Config.STRING_SESSION else None

@Client.on_message(filters.private & (filters.document | filters.video | filters.audio))
async def rename_start(client, message):
    media = getattr(message, message.media.value)
    filename = media.file_name or "file.mkv"
    size = humanbytes(media.file_size)
    dcid = FileId.decode(media.file_id).dc_id

    buttons = [[InlineKeyboardButton("📁 Document", callback_data="upload#document")]]
    if message.media in [MessageMediaType.VIDEO, MessageMediaType.DOCUMENT]:
        buttons.append([InlineKeyboardButton("🎥 Video", callback_data="upload#video")])
    elif message.media == MessageMediaType.AUDIO:
        buttons.append([InlineKeyboardButton("🎵 Audio", callback_data="upload#audio")])

    await message.reply(
        f"**Select Output Type**\n\n📄 `{filename}`\n📦 `{size}`\n📡 DC `{dcid}`",
        reply_markup=InlineKeyboardMarkup(buttons)
    )

@Client.on_callback_query(filters.regex('^upload'))
async def upload_doc(client, update):
    # Ye function ab properly accessible hai
    msg = await update.message.edit("`Processing...`")
    user_id = update.from_user.id
    file = update.message.reply_to_message
    media = getattr(file, file.media.value)

    info = renamer.extract_all_info(media.file_name)
    user = await digital_botz.get_user_data(user_id)

    new_name = renamer.apply_format_template(info, user.get("format_template"))
    if not new_name.endswith(f".{info['extension']}"):
        new_name += f".{info['extension']}"

    path = f"Renames/{new_name}"
    await msg.edit(DOWNLOAD_TEXT)

    dl = await client.download_media(
        file, file_name=path,
        progress=progress_for_pyrogram,
        progress_args=(DOWNLOAD_TEXT, msg, time.time())
    )

    duration = 0
    try:
        meta = extractMetadata(createParser(path))
        if meta and meta.has("duration"):
            duration = meta.get("duration").seconds
    except: pass

    caption = user.get("caption")
    if caption:
        caption = caption.format(filename=new_name, filesize=humanbytes(media.file_size), duration=convert(duration))
    else:
        caption = f"**{new_name}**"

    thumb = None
    if user.get("file_id"):
        thumb = await client.download_media(user["file_id"])
    elif media.thumbs:
        thumb = await client.download_media(media.thumbs[0].file_id)

    if thumb:
        Image.open(thumb).convert("RGB").resize((320, 320)).save(thumb)

    await msg.edit(UPLOAD_TEXT)
    upload_type = update.data.split("#")[1]

    send_func = {
        "document": client.send_document,
        "video": client.send_video,
        "audio": client.send_audio
    }.get(upload_type, client.send_document)

    await send_func(
        chat_id=user_id,
        **{upload_type: path},
        caption=caption,
        thumb=thumb,
        duration=duration,
        progress=progress_for_pyrogram,
        progress_args=(UPLOAD_TEXT, msg, time.time())
    )

    await remove_path(thumb, path, dl)
    await msg.edit("✅ **Uploaded Successfully!**")
