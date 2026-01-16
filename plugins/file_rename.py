# (c) @RknDeveloperr
# Rkn Developer 
# Don't Remove Credit 😔
# Telegram Channel @RknDeveloper & @Rkn_Botz
# Developer @RknDeveloperr
# Special Thanks To @ReshamOwner
# Update Channel @Digital_Botz & @DigitalBotz_Support

# pyrogram imports
from pyrogram import Client, filters
from pyrogram.enums import MessageMediaType
from pyrogram.errors import FloodWait
from pyrogram.file_id import FileId
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ForceReply

# hachoir imports
from hachoir.metadata import extractMetadata
from hachoir.parser import createParser
from PIL import Image

# bots imports
from helper.utils import progress_for_pyrogram, convert, humanbytes, add_prefix_suffix, remove_path
from helper.database import digital_botz
from config import Config
from plugins.auto_rename import EnhancedAutoRenamer

# extra imports
from asyncio import sleep
import os, time, asyncio


UPLOAD_TEXT = """Uploading Started...."""
DOWNLOAD_TEXT = """Download Started..."""

# Optimization: Added workers and sleep_threshold for faster 4GB handling
app = Client(
    "4gb_FileRenameBot", 
    api_id=Config.API_ID, 
    api_hash=Config.API_HASH, 
    session_string=Config.STRING_SESSION,
    workers=100,
    sleep_threshold=15
)


@Client.on_message(filters.private & (filters.audio | filters.document | filters.video))
async def rename_start(client, message):
    user_id  = message.from_user.id
    rkn_file = getattr(message, message.media.value)
    if not Config.STRING_SESSION:
        if rkn_file.file_size > 2000 * 1024 * 1024:
             return await message.reply_text("Sᴏʀʀy Bʀᴏ Tʜɪꜱ Bᴏᴛ Iꜱ Dᴏᴇꜱɴ'ᴛ Sᴜᴩᴩᴏʀᴛ Uᴩʟᴏᴀᴅɪɴɢ Fɪʟᴇꜱ Bɪɢɢᴇʀ Tʜᴀɴ 2Gʙ+")

    filename = rkn_file.file_name
    if not "." in filename:
        if "." in filename:
            extn = filename.rsplit('.', 1)[-1]
        else:
            extn = "mkv"
        filename = filename + "." + extn

    filesize = humanbytes(rkn_file.file_size)
    mime_type = rkn_file.mime_type
    dcid = FileId.decode(rkn_file.file_id).dc_id
    extension_type = mime_type.split('/')[0]

    button = [[InlineKeyboardButton("📁 Dᴏᴄᴜᴍᴇɴᴛ",callback_data = "upload#document")]]
    if message.media in [MessageMediaType.VIDEO, MessageMediaType.DOCUMENT]:
        button.append([InlineKeyboardButton("🎥 Vɪᴅᴇᴏ", callback_data = "upload#video")])
    elif message.media == MessageMediaType.AUDIO:
        button.append([InlineKeyboardButton("🎵 Aᴜᴅɪᴏ", callback_data = "upload#audio")])
    await message.reply(
            text=f"**Sᴇʟᴇᴄᴛ Tʜᴇ Oᴜᴛᴩᴜᴛ Fɪʟᴇ Tyᴩᴇ**\n\n**__ᴍᴇᴅɪᴀ ɪɴꜰᴏ:\n\n◈ ᴏʟᴅ ꜰɪʟᴇ ɴᴀᴍᴇ: `{filename}`\n\n◈ ᴇxᴛᴇɴꜱɪᴏɴ: `{extension_type.upper()}`\n◈ ꜰɪʟᴇ ꜱɪᴢᴇ: `{filesize}`\n◈ ᴍɪᴍᴇ ᴛʏᴇᴩ: `{mime_type}`\n◈ ᴅᴄ ɪᴅ: `{dcid}`....__**",        
            reply_to_message_id=message.id,
            reply_markup=InlineKeyboardMarkup(button)
        )

async def upload_files(bot, sender_id, upload_type, file_path, ph_path, caption, duration, rkn_processing):
    try:
        if not os.path.exists(file_path):
            return None, f"File not found: {file_path}"

        if upload_type == "document":
            filw = await bot.send_document(
                sender_id,
                document=file_path,
                thumb=ph_path,
                caption=caption,
                progress=progress_for_pyrogram,
                progress_args=(UPLOAD_TEXT, rkn_processing, time.time()))

        elif upload_type == "video":
            filw = await bot.send_video(
                sender_id,
                video=file_path,
                caption=caption,
                thumb=ph_path,
                duration=duration,
                progress=progress_for_pyrogram,
                progress_args=(UPLOAD_TEXT, rkn_processing, time.time()))

        elif upload_type == "audio":
            filw = await bot.send_audio(
                sender_id,
                audio=file_path,
                caption=caption,
                thumb=ph_path,
                duration=duration,
                progress=progress_for_pyrogram,
                progress_args=(UPLOAD_TEXT, rkn_processing, time.time()))
        else:
            return None, f"Unknown upload type: {upload_type}"

        return filw, None

    except Exception as e:
        return None, str(e)

renamer = EnhancedAutoRenamer()

async def upload_doc(bot, update):
    rkn_processing = await update.message.edit("`Processing...`")

    user_id = int(update.message.chat.id) 
    new_name = update.message.text

    file = update.message.reply_to_message
    media = getattr(file, file.media.value)

    info = renamer.extract_all_info(media.file_name)
    user_data = await digital_botz.get_user_data(user_id)
    format_template = user_data.get('format_template', None)

    new_name = renamer.apply_format_template(info, format_template)

    if not new_name.endswith(f".{info['extension']}"):
        new_name += f".{info['extension']}"

    new_filename = new_name
    file_path = f"Renames/{new_filename}"

    await rkn_processing.edit("`Try To Download....`")    
    try:            
        # Optimization: Download with bot client for regular speed
        dl_path = await bot.download_media(message=file, file_name=file_path, progress=progress_for_pyrogram, progress_args=(DOWNLOAD_TEXT, rkn_processing, time.time()))                    
    except Exception as e:        
        return await rkn_processing.edit(f"Download Error: {e}")

    await rkn_processing.edit("`Try To Uploading....`")        
    duration = 0
    try:
        parser = createParser(file_path)
        metadata = extractMetadata(parser)
        if metadata and metadata.has("duration"):
            duration = metadata.get('duration').seconds
        if parser:
            parser.close()
    except Exception as e:
        print(f"Error extracting metadata: {e}")
        pass

    ph_path = None
    c_caption = user_data.get('caption', None)
    c_thumb = user_data.get('file_id', None)

    if c_caption:
         try:
             caption = c_caption.format(filename=new_filename, filesize=humanbytes(media.file_size), duration=convert(duration))
         except Exception as e:             
             return await rkn_processing.edit(text=f"Yᴏᴜʀ Cᴀᴩᴛɪᴏɴ Eʀʀᴏʀ Exᴄᴇᴩᴛ Kᴇyᴡᴏʀᴅ Aʀɢᴜᴍᴇɴᴛ ●> ({e})")             
    else:
         caption = f"**{new_filename}**"

    if (media.thumbs or c_thumb):
         try:
             if c_thumb:
                 ph_path = await bot.download_media(c_thumb) 
             else:
                 ph_path = await bot.download_media(media.thumbs[0].file_id)

             if ph_path and os.path.exists(ph_path):
                 img = Image.open(ph_path).convert("RGB")
                 img.thumbnail((320, 320))
                 img.save(ph_path, "JPEG")
         except Exception as e:
             print(f"Error processing thumbnail: {e}")
             ph_path = None

    upload_type = update.data.split("#")[1]
    final_file_path = file_path    

    if media.file_size > 2000 * 1024 * 1024:
        # Optimized Upload with 'app' (Premium)
        filw, error = await upload_files(
            app, Config.LOG_CHANNEL, upload_type, final_file_path, 
            ph_path, caption, duration, rkn_processing
        )

        if error:            
            await remove_path(ph_path, file_path, dl_path)
            return await rkn_processing.edit(f"Upload Error: {error}")

        from_chat = filw.chat.id
        mg_id = filw.id
        await asyncio.sleep(2)
        await bot.copy_message(update.from_user.id, from_chat, mg_id)
        await bot.delete_messages(from_chat, mg_id)        
    else:
        filw, error = await upload_files(
            bot, update.message.chat.id, upload_type, final_file_path, 
            ph_path, caption, duration, rkn_processing
        )

        if error:            
            await remove_path(ph_path, file_path, dl_path)
            return await rkn_processing.edit(f"Upload Error: {error}")        

    await remove_path(ph_path, file_path, dl_path)
    return await rkn_processing.edit("Uploaded Successfully....")
