from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes
from config import BOT_USERNAME, REQUIRED_REFERRALS
from handlers.force_join import is_user_in_channel
from handlers.referral import register_user, get_user
from handlers.payout import payout_keyboard

def join_keyboard(link):
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🔔 Join Channel", url=link)],
        [InlineKeyboardButton("✅ I've Joined", callback_data="check_join")]
    ])

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    args = context.args
    referrer = int(args[0]) if args else None

    if not await is_user_in_channel(context.bot, user_id):
        await update.message.reply_text(
            "🚫 You must join our channel before using the bot.",
            reply_markup=join_keyboard(context.bot.username)
        )
        return

    register_user(user_id, referrer)
    referrals, unlocked = get_user(user_id)

    if referrals < REQUIRED_REFERRALS:
        link = f"https://t.me/{BOT_USERNAME}?start={user_id}"
        await update.message.reply_text(
            f"🔒 Access Locked\n\n"
            f"Refer {REQUIRED_REFERRALS - referrals} more users to unlock payment access.\n\n"
            f"Your referral link:\n{link}"
        )
        return

    if not unlocked:
        from database import cursor, conn
        cursor.execute("UPDATE users SET unlocked=1 WHERE user_id=?", (user_id,))
        conn.commit()

    await update.message.reply_text(
        "✅ Access Unlocked!\n\n"
        "You can now request **BANK TRANSFER PAYMENT**.\n\n"
        "⚠️ Payments are manual and subject to verification.",
        reply_markup=payout_keyboard(),
        parse_mode="Markdown"
    )
