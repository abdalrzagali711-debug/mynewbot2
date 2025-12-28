import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = os.environ.get("TOKEN")
if not TOKEN:
    raise ValueError("يرجى تعيين توكن البوت كمتغير بيئة باسم TOKEN")

users = set()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    users.add(update.message.from_user.id)
    name = update.message.from_user.first_name
    await update.message.reply_text(
        f"أهلاً {name} 👋\nالبوت شغال 24 ساعة!\nالخدمات المجانية:\n1- خدمة تحويل صورة\n2- خدمة إزالة خلفية\n3- خدمة معلومات عامة\n4- خدمة ترحيب شخصي"
    )

async def service1(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ خدمة تحويل صورة مجانية")

async def service2(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ خدمة إزالة خلفية مجانية")

async def service3(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ خدمة معلومات عامة مجانية")

async def count_users(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"عدد المستخدمين الذين استخدموا البوت: {len(users)}")

def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("service1", service1))
    app.add_handler(CommandHandler("service2", service2))
    app.add_handler(CommandHandler("service3", service3))
    app.add_handler(CommandHandler("users", count_users))

    # تشغيل البوت باستخدام polling (بدون Webhook)
    app.run_polling()

if __name__ == "__main__":
    main()
