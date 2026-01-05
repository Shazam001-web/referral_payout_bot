from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler
)
from config import TOKEN, ADMIN_USERNAME
from handlers.start import start
from handlers.force_join import is_user_in_channel

async def check_join(update, context):
    query = update.callback_query
    user_id = query.from_user.id

    if await is_user_in_channel(context.bot, user_id):
        await query.message.edit_text("✅ Verified! Now send /start")
    else:
        await query.answer("❌ Join the channel first.", show_alert=True)

async def bank_payout(update, context):
    query = update.callback_query
    user = query.from_user

    await query.message.reply_text(
        "🏦 BANK TRANSFER REQUEST\n\n"
        f"User ID: `{user.id}`\n"
        f"Username: @{user.username}\n\n"
        "📌 Please send the following to admin:\n"
        "- Bank name\n"
        "- Account number\n"
        "- Account name\n\n"
        f"Admin: {ADMIN_USERNAME}",
        parse_mode="Markdown"
    )

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(check_join, pattern="check_join"))
app.add_handler(CallbackQueryHandler(bank_payout, pattern="bank_payout"))

app.run_polling()
