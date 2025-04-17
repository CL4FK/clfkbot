from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

# 🔐 Токен твоего бота
TOKEN = "7369403731:AAFCd0gQQmOEDnvdXp9t0CuCY8K3QYR-djE"

# 📢 Список каналов, на которые нужно подписаться
REQUIRED_CHANNELS = ["@CLFK4"]  # ← Убедись, что бот админ в этом канале

# 🔗 Скрытая ссылка на приватный канал (через join link)
PRIVATE_CHANNEL_LINK = "https://t.me/+5ASvs47WQxU4YTE6"

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    buttons = [[InlineKeyboardButton(text="Проверить подписку", callback_data="check_subscription")]]
    channel_list = "\n".join([f"👉 {ch}" for ch in REQUIRED_CHANNELS])
    await update.message.reply_text(
        f"Привет! Чтобы продолжить, подпишись на канал:\n\n{channel_list}",
        reply_markup=InlineKeyboardMarkup(buttons)
    )

# Проверка подписки
async def check_subscription(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    not_subscribed = []

    for channel in REQUIRED_CHANNELS:
        try:
            member = await context.bot.get_chat_member(chat_id=channel, user_id=user_id)
            if member.status not in ["member", "administrator", "creator"]:
                not_subscribed.append(channel)
        except:
            not_subscribed.append(channel)

    if not not_subscribed:
        # Все ок — отправляем кнопку на приватный канал
        join_button = [[InlineKeyboardButton("Перейти в канал", url=PRIVATE_CHANNEL_LINK)]]
        await query.edit_message_text(
            "✅ Подписка подтверждена! Нажми на кнопку ниже, чтобы перейти в наш канал:",
            reply_markup=InlineKeyboardMarkup(join_button)
        )
    else:
        # Не подписан на один или несколько каналов
        retry_button = [[InlineKeyboardButton("Проверить снова", callback_data="check_subscription")]]
        channels_text = "\n".join([f"❗ Подпишись на {ch}" for ch in not_subscribed])
        await query.edit_message_text(
            f"Ты ещё не подписан на:\n\n{channels_text}",
            reply_markup=InlineKeyboardMarkup(retry_button)
        )

# Запуск бота
if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(check_subscription, pattern="check_subscription"))
    app.run_polling()