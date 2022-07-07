import os
import os.path
import logging
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from creds import Credentials
import datetime
from pyrogram.errors import UserNotParticipant, ChatAdminRequired, UsernameNotOccupied
from telegraph import upload_file
import zipfile as z

logging.basicConfig(level=logging.WARNING)


tgraph = Client(
    "Image upload bot",
    bot_token=Credentials.BOT_TOKEN,
    api_id=Credentials.API_ID,
    api_hash=Credentials.API_HASH,

)



@tgraph.on_message(filters.command("start"))
async def start(client, message):
    await message.reply_text(
        text=f"Hello {message.from_user.mention},\nI'm a telegram to telegra.ph image uploader bot by @BotBoii",
        disable_web_page_preview=True
    )


@tgraph.on_message(filters.document)
async def getzip(client, message):
    dwn = await message.reply_text("Downloading to my server...", True)
    file_name = message.document.file_name
    filename = file_name.split(".")[0]
    
    doc_path = await message.download()
    await dwn.edit_text("unzipping...")
    root = z.ZipFile(doc_path)
    root.extractall("downloads/")
    root.close()
    path = f"downloads/{filename}"
    #up_files = os.listdir(path)
    upfiles = os.path.abspath(path)
    #print(up_files)
    print(upfiles)
    try:
        url_path = upload_file(upfiles)
    except Exception as error:
        await dwn.edit_text(f"Oops something went wrong\n{error}")
        return
    await dwn.edit_text(
        text=f"<b>Link :-</b> <code>https://telegra.ph{filename}</code>",
        disable_web_page_preview=True,
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="Open Link", url=f"https://telegra.ph{url_path}"
                    ),
                    InlineKeyboardButton(
                        text="Share Link",
                        url=f"https://telegram.me/share/url?url=https://telegra.ph{url_path}",
                    )
                ]
            ]
        )
    )
    os.remove(doc_path)
    os.rmdir(f"downloads/{filename}")


tgraph.run()
