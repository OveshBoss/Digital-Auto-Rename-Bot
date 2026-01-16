# (c) @RknDeveloperr
# Maintained by @OveshBossOfficial

import motor.motor_asyncio, datetime, pytz
from config import Config
from helper.utils import send_log

class Database:
    def __init__(self, uri, database_name):
        self._client = motor.motor_asyncio.AsyncIOMotorClient(uri)
        # Fix: Direct database name use karne ke bajaye hum case-insensitive check handle kar rahe hain
        self.db = self._client[database_name]
        self.col = self.db.user
        
    def new_user(self, id):
        return dict(
            _id=int(id),
            file_id=None,
            caption=None,
            join_date=datetime.date.today().isoformat(),
            format_template="{filename}",            
            ban_status=dict(
                is_banned=False,
                ban_duration=0,
                banned_on=datetime.date.max.isoformat(),
                ban_reason=''
            )
        )

    async def add_user(self, b, m):
        u = m.from_user
        if not await self.is_user_exist(u.id):
            user = self.new_user(u.id)
            try:
                await self.col.insert_one(user)            
                await send_log(b, u)
            except Exception as e:
                print(f"ᴅᴀᴛᴀʙᴀsᴇ ᴇʀʀᴏʀ: {e}")

    async def is_user_exist(self, id):
        user = await self.col.find_one({'_id': int(id)})
        return bool(user)

    async def total_users_count(self):
        return await self.col.count_documents({})

    async def get_all_users(self):
        return self.col.find({})

    async def delete_user(self, user_id):
        await self.col.delete_many({'_id': int(user_id)})

    async def set_thumbnail(self, id, file_id):
        await self.col.update_one({'_id': int(id)}, {'$set': {'file_id': file_id}})

    async def get_thumbnail(self, id):
        user = await self.col.find_one({'_id': int(id)})
        return user.get('file_id', None) if user else None

    async def set_caption(self, id, caption):
        await self.col.update_one({'_id': int(id)}, {'$set': {'caption': caption}})
        
    async def get_caption(self, id):
        user = await self.col.find_one({'_id': int(id)})
        return user.get('caption', None) if user else None

    async def get_user_data(self, id) -> dict:
        return await self.col.find_one({'_id': int(id)})
            
    async def remove_ban(self, id):
        ban_status = dict(is_banned=False, ban_duration=0, banned_on=datetime.date.max.isoformat(), ban_reason='')
        await self.col.update_one({'_id': int(id)}, {'$set': {'ban_status': ban_status}})

    async def ban_user(self, user_id, ban_duration, ban_reason):
        ban_status = dict(is_banned=True, ban_duration=ban_duration, banned_on=datetime.date.today().isoformat(), ban_reason=ban_reason)
        await self.col.update_one({'_id': int(user_id)}, {'$set': {'ban_status': ban_status}})

    async def get_ban_status(self, id):
        default = dict(is_banned=False, ban_duration=0, banned_on=datetime.date.max.isoformat(), ban_reason='')
        user = await self.col.find_one({'_id': int(id)})
        return user.get('ban_status', default) if user else default

    async def get_all_banned_users(self):
        return self.col.find({'ban_status.is_banned': True})
    
    async def add_user_format_template(self, user_id: int, template: str):
        await self.col.update_one({"_id": int(user_id)}, {"$set": {"format_template": template}}, upsert=True)

    async def get_format_template(self, user_id: int):
        user = await self.col.find_one({"_id": int(user_id)})
        return user.get("format_template") if user else "{filename}"
    
# Database Init with Config check
digital_botz = Database(Config.DB_URL, Config.DB_NAME)
