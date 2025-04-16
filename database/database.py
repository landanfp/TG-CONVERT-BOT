from pymongo import MongoClient
from config import Config
import threading

client = MongoClient(Config.DB_URI)
db = client["tg_convert_bot"]  # اسم دیتابیس رو به دلخواه تغییر بده

INSERTION_LOCK = threading.RLock()

# ------------------ Thumbnail Collection ------------------
async def df_thumb(id, msg_id):
    with INSERTION_LOCK:
        thumbs = db.thumbnails
        thumbs.delete_one({"id": id})
        thumbs.insert_one({"id": id, "msg_id": msg_id})

async def del_thumb(id):
    with INSERTION_LOCK:
        db.thumbnails.delete_one({"id": id})

async def get_thumb(id):
    return db.thumbnails.find_one({"id": id})

# ------------------ Settings Collection -------------------
async def add(id, value):
    with INSERTION_LOCK:
        settings = db.settings
        settings.delete_one({"id": id})
        settings.insert_one({"id": id, "value": value})

async def remove(id):
    with INSERTION_LOCK:
        db.settings.delete_one({"id": id})

async def check(id):
    return db.settings.find_one({"id": id})
