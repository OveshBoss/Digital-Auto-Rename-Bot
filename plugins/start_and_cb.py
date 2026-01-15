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

# extra imports
import random, asyncio, datetime, pytz, time, psutil, shutil

# pyrogram imports
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery

# bots imports
from helper.database import digital_botz
from config import Config, rkn
from helper.utils import humanbytes
from plugins import __version__ as _bot_version_, __developer__, __database__, __library__, __language__, __programer__
from plugins.file_rename import upload_doc


@Client.on_message(filters.private & filters.command("start"))
async def start(client, message):
    start_button = [[        
        InlineKeyboardButton('ᴍᴀɪɴ ᴄʜᴀɴɴᴇʟ', url='https://t.me/@OveshBossOfficial'),
        InlineKeyboardButton('sᴜᴘᴘᴏʀᴛ', url='https://t.me/@OnlyBossMoviesGroup')
        ],[
        InlineKeyboardButton('💌 Aʙᴏᴜᴛ', callback_data='about'),
        InlineKeyboardButton('ℹ️ Hᴇʟᴘ', callback_data='help')       
         ]]
        
    user = message.from_user
    await digital_botz.add_user(client, message) 

    if Config.RKN_PIC:
        await message.reply_photo(
            Config.RKN_PIC,
            caption=rkn.START_TXT.format(user.mention),
            reply_markup=InlineKeyboardMarkup(start_button)
        )
    else:
        await message.reply_text(
            text=rkn.START_TXT.format(user.mention),
            reply_markup=InlineKeyboardMarkup(start_button),
            disable_web_page_preview=True
        )


@Client.on_callback_query()
async def cb_handler(client, query: CallbackQuery):
    data = query.data 

    if data == "start":
        start_button = [[        
            InlineKeyboardButton('ᴍᴀɪɴ ᴄʜᴀɴɴᴇʟ', url='https://t.me/@OveshBossOfficial'),
            InlineKeyboardButton('sᴜᴘᴘᴏʀᴛ', url='https://t.me/@OnlyBossMoviesGroup')
        ],[
            InlineKeyboardButton('💌 Aʙᴏᴜᴛ', callback_data='about'),
            InlineKeyboardButton('ℹ️ Hᴇʟᴘ', callback_data='help')       
        ]]
            
        await query.message.edit_text(
            text=rkn.START_TXT.format(query.from_user.mention),
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(start_button)
        )
        
    elif data == "help":
        await query.message.edit_text(
            text=(
                "ℹ️ Hᴇʟᴘ\n\n"
                "ʙʜᴀɪ ᴀᴜʀ ʏᴇ ᴍᴇʀᴀ ʀᴇɴᴀᴍᴇ ʙᴏᴛ "
                "ᴅᴏᴡɴʟᴏᴀᴅ ʙᴏᴛʜ sʟᴏᴡ ᴋᴀʀᴛᴀ ʜᴀɪ "
                "ᴘʟᴢᴢ ʜᴇʟᴘ"
            ),
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("ᴛʜᴜᴍʙɴᴀɪʟ", callback_data="thumbnail"),
                InlineKeyboardButton("ᴄᴀᴘᴛɪᴏɴ", callback_data="caption")
            ],[
                InlineKeyboardButton("💌 Aʙᴏᴜᴛ", callback_data="about"),
                InlineKeyboardButton("Bᴀᴄᴋ", callback_data="start")
            ]])
        )         
        
    elif data == "about":
        about_button = [[
            InlineKeyboardButton("sᴏᴜʀᴄᴇ", callback_data="source_code"),
            InlineKeyboardButton("ʙᴏᴛ sᴛᴀᴛᴜs", callback_data="bot_status")
        ],[
            InlineKeyboardButton("ʟɪᴠᴇ sᴛᴀᴛᴜs", callback_data="live_status"),
            InlineKeyboardButton("Bᴀᴄᴋ", callback_data="start")
        ]]
            
        await query.message.edit_text(
            text=(
                "💌 Aʙᴏᴜᴛ\n\n" +
                rkn.ABOUT_TXT.format(
                    client.mention,
                    __developer__,
                    __programer__,
                    __library__,
                    __language__,
                    __database__,
                    _bot_version_
                )
            ),
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(about_button)
        )    

    elif data == "thumbnail":
        await query.message.edit_text(
            text=rkn.THUMBNAIL,
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("Bᴀᴄᴋ", callback_data="help")
            ]])
        ) 
      
    elif data == "caption":
        await query.message.edit_text(
            text=rkn.CAPTION,
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("Bᴀᴄᴋ", callback_data="help")
            ]])
        ) 
      
    elif data == "bot_status":
        total_users = await digital_botz.total_users_count()
        uptime = time.strftime("%Hh%Mm%Ss", time.gmtime(time.time() - client.uptime))    
        sent = humanbytes(psutil.net_io_counters().bytes_sent)
        recv = humanbytes(psutil.net_io_counters().bytes_recv)

        await query.message.edit_text(
            text=rkn.BOT_STATUS.format(
                uptime, total_users, "Disabled ✅", sent, recv
            ),
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("Bᴀᴄᴋ", callback_data="about")
            ]])
        ) 
      
    elif data == "live_status":
        total, used, free = shutil.disk_usage(".")
        await query.message.edit_text(
            text=rkn.LIVE_STATUS.format(
                time.strftime("%Hh%Mm%Ss", time.gmtime(time.time() - client.uptime)),
                psutil.cpu_percent(),
                psutil.virtual_memory().percent,
                humanbytes(total),
                humanbytes(used),
                psutil.disk_usage('/').percent,
                humanbytes(free),
                humanbytes(psutil.net_io_counters().bytes_sent),
                humanbytes(psutil.net_io_counters().bytes_recv)
            ),
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("Bᴀᴄᴋ", callback_data="about")
            ]])
        ) 
      
    elif data == "source_code":
        await query.message.edit_text(
            text=rkn.DEV_TXT,
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton(
                    "💞 Sᴏᴜʀᴄᴇ Cᴏᴅᴇ 💞",
                    url="https://github.com/OveshBoss/Digital-Auto-Rename-Bot"
                )
            ],[
                InlineKeyboardButton("🔒 Cʟᴏꜱᴇ", callback_data="close"),
                InlineKeyboardButton("◀️ Bᴀᴄᴋ", callback_data="start")
            ]])
        )

    elif data.startswith("upload"):
        await upload_doc(client, query)

    elif data == "close":
        try:
            await query.message.delete()
            await query.message.reply_to_message.delete()
        except:
            await query.message.delete() 
