import os
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
    plugins=dict(root="plugins/Force_sub.py")

)



@tgraph.on_message(filters.command("start"))
async def start(client, message):
    await message.reply_text(
        text=f"Hello {message.from_user.mention},\nI'm a telegram to telegra.ph image uploader bot by @W4RR10R",
        disable_web_page_preview=True
    )


@tgraph.on_message(filters.document)
async def getzip(client, message):
    dwn = await message.reply_text("Downloading to my server...", True)
    doc_path = await message.download()
    file_name = doc_path.file_name
    await dwn.edit_text("unzipping...")
    root = z.ZipFile(doc_path)
    root.extractall()
    root.close()
    try:
        url_path = upload_file(f"{file_name}/")
    except Exception as error:
        await dwn.edit_text(f"Oops something went wrong\n{error}")
        return
    await dwn.edit_text(
        text=f"<b>Link :-</b> <code>https://telegra.ph{url_path}</code>",
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
    os.remove(img_path)


tgraph.run()
