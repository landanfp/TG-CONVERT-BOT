import logging
import os

from config import Config
from translation import Translation
import database.database as db

from pyrogram import Client, filters

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
logging.getLogger("pyrogram").setLevel(logging.WARNING)


@Client.on_message(filters.photo)
async def save_photo(bot, update):
    user_id = update.from_user.id

    if user_id in Config.BANNED_USER:
        await bot.delete_messages(chat_id=update.chat.id, message_ids=update.message_id, revoke=True)
        return

    if update.media_group_id is not None:
        download_location = os.path.join(Config.DOWNLOAD_LOCATION, str(user_id), str(update.media_group_id))
        os.makedirs(download_location, exist_ok=True)
        await db.df_thumb(user_id, update.message_id)
        await bot.download_media(message=update, file_name=download_location)
    else:
        download_location = os.path.join(Config.DOWNLOAD_LOCATION, f"{user_id}.jpg")
        await bot.download_media(message=update, file_name=download_location)
        await db.df_thumb(user_id, update.message_id)
        await bot.send_message(
            chat_id=update.chat.id,
            text=Translation.SAVED_CUSTOM_THUMB_NAIL,
            reply_to_message_id=update.message_id
        )


@Client.on_message(filters.command(["deletethumbnail"]))
async def delete_thumbnail(bot, update):
    user_id = update.from_user.id

    if user_id in Config.BANNED_USER:
        await bot.delete_messages(chat_id=update.chat.id, message_ids=update.message_id, revoke=True)
        return

    download_path = os.path.join(Config.DOWNLOAD_LOCATION, f"{user_id}.jpg")

    try:
        await db.del_thumb(user_id)
        if os.path.exists(download_path):
            os.remove(download_path)
    except Exception as e:
        logger.warning(f"Error deleting thumbnail: {e}")

    await bot.send_message(
        chat_id=update.chat.id,
        text=Translation.DEL_ETED_CUSTOM_THUMB_NAIL,
        reply_to_message_id=update.message_id
    )
