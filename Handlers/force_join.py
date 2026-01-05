from telegram.error import BadRequest
from config import CHANNEL_USERNAME

async def is_user_in_channel(bot, user_id):
    try:
        member = await bot.get_chat_member(CHANNEL_USERNAME, user_id)
        return member.status in ["member", "administrator", "creator"]
    except BadRequest:
        return False
