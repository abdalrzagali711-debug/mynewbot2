import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# قراءة التوكن من Environment Variable
TOKEN = os.environ.get("TOKEN")
if not TOKEN:
    raise ValueError("يرجى تعيين توكن البوت كمتغير بيئة باسم TOKEN")

# قراءة البورت من Environment Variable (Render يعطي PORT تلقائيًا)
PORT = int(os.environ.get("PORT", 5000))

# عدد المستخدمين المتصلين (يمكنك حفظه لاحقًا في قاعدة بيانات)
users = set()

# خدمات مجانية
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    users.add(update.message.from_user.id)  # حفظ المستخدم
    name = update.message.from_user.first_name
    await update.message.reply_text(f"أهلاً {name} 👋\nالبوت شغال 24 ساعة!\nالخدمات المجانية:\n1- خدمة تحويل صورة\n2- خدمة إزالة خلفية\n3- خدمة معلومات عامة\n4- خدمة ترحيب شخصي")

async def service1(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ هذه خدمة تحويل صورة مجانية (تطوير لاحق للاشتراك)")

async def service2(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ هذه خدمة إزالة خلفية الصور مجانية")

async def service3(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ هذه خدمة معلومات عامة مجانية")

async def count_users(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"عدد المستخدمين الذين استخدموا البوت: {len(users)}")

def main():
    app = ApplicationBuilder().token(TOKEN).build()
    
    # إضافة أوامر
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("service1", service1))
    app.add_handler(CommandHandler("service2", service2))
    app.add_handler(CommandHandler("service3", service3))
    app.add_handler(CommandHandler("users", count_users))

    # تشغيل Webhook على Render
    app.run_webhook(
        listen="0.0.0.0",
        port=PORT,
        webhook_url=f"https://{os.environ.get('RENDER_EXTERNAL_URL')}/{TOKEN}"
    )

if __name__ == "__main__":
    main()
