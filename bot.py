import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

BOT_TOKEN = os.environ["8297713361:AAGlD1Nu0SnW9ZKHz1UHR33zqqtRC0cpAC0"]
ADMINS = os.environ["8365833368"].split(",")

USERS_FILE = "users.txt"

def save_user(user_id):
    with open(USERS_FILE, "a+") as f:
        f.seek(0)
        if str(user_id) not in f.read():
            f.write(str(user_id) + "\n")

def load_users():
    if not os.path.exists(USERS_FILE):
        return []
    with open(USERS_FILE) as f:
        return [line.strip() for line in f if line.strip()]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    save_user(user_id)
    await update.message.reply_text("You are subscribed ✔")

async def broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    sender = str(update.effective_user.id)
    if sender not in ADMINS:
        await update.message.reply_text("❌ Admin only")
        return

    users = load_users()

    for uid in users:
        try:
            await context.bot.copy_message(
                chat_id=uid,
                from_chat_id=update.message.chat_id,
                message_id=update.message.message_id
            )
        except:
            pass

    await update.message.reply_text(f"✔ Broadcast sent to {len(users)} users")

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.ALL & (~filters.COMMAND), broadcast))

    app.run_polling()

if __name__ == "__main__":
    main()
