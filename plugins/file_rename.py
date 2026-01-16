from pyrogram import Client, filters
from pyrogram.enums import MessageMediaType
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from helper.utils import progress_for_pyrogram, convert, humanbytes, remove_path
from helper.database import digital_botz
from config import Config
from plugins.auto_rename import EnhancedAutoRenamer
import os, time, asyncio

renamer = EnhancedAutoRenamer()

# Function definition for other plugins to import
async def upload_doc(client, update):
    msg = await update.message.edit("`ᴘʀᴏᴄᴇssɪɴɢ...`")
    user_id = update.from_user.id
    file = update.message.reply_to_message
    media = getattr(file, file.media.value)
    
    # Simple logic to rename and upload
    await msg.edit("⚡ ᴅᴏᴡɴʟᴏᴀᴅɪɴɢ...")
    path = await client.download_media(file)
    
    await msg.edit("🚀 ᴜᴘʟᴏᴀᴅɪɴɢ...")
    await client.send_document(user_id, document=path, caption=f"**{media.file_name}**")
    if os.path.exists(path): os.remove(path)
    await msg.edit("✅ **ᴅᴏɴᴇ!**")

@Client.on_message(filters.private & (filters.document | filters.video | filters.audio))
async def rename_start(client, message):
    media = getattr(message, message.media.value)
    filename = media.file_name or "file.mkv"
    buttons = [[InlineKeyboardButton("📁 ᴅᴏᴄᴜᴍᴇɴᴛ", callback_data="upload#document")]]
    await message.reply(f"📄 `{filename}`", reply_markup=InlineKeyboardMarkup(buttons))

# Exporting 'app' for bot.py
app = Client("UserSession", api_id=Config.API_ID, api_hash=Config.API_HASH, session_string=Config.STRING_SESSION) if Config.STRING_SESSION else None
