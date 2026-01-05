from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from config import ADMIN_LINK

def payout_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🏦 Request Bank Payment", callback_data="bank_payout")],
        [InlineKeyboardButton("💬 Contact Admin", url=ADMIN_LINK)]
    ])
