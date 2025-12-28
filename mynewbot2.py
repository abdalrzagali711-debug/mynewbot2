import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters

# تسجيل الأخطاء
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# قراءة التوكن من Environment Variable
TOKEN = os.environ.get("TOKEN")
if not TOKEN:
    raise ValueError("يرجى تعيين توكن البوت كمتغير بيئة باسم TOKEN")

USERS_FILE = "users.txt"

# حفظ المستخدمين الجدد
def save_user(user_id):
    if not os.path.exists(USERS_FILE):
        with open(USERS_FILE, "w") as f:
            f.write(f"{user_id}\n")
        return
    with open(USERS_FILE, "r") as f:
        users = f.read().splitlines()
    if str(user_id) not in users:
        with open(USERS_FILE, "a") as f:
            f.write(f"{user_id}\n")

# أمر /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    save_user(user.id)
    await update.message.reply_text(f"أهلاً {user.first_name} 👋\nالبوت جاهز للاستخدام!")

# خدمة تحويل النصوص إلى صورة (مجرد مثال)
async def text_to_image(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) == 0:
        await update.message.reply_text("يرجى كتابة النص بعد الأمر.\nمثال: /image مرحبا")
        return
    text = " ".join(context.args)
    # هنا يمكن ربط مكتبة توليد الصور أو AI لاحقًا
    await update.message.reply_text(f"تم استلام النص: {text}\nسيتم تحويله لصورة لاحقاً 🚀")

# خدمة إزالة الخلفية من الصورة (مجرد مثال)
async def remove_bg(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message.photo:
        await update.message.reply_text("أرسل صورة لإزالة الخلفية.")
        return
    await update.message.reply_text("تم استلام الصورة، سيتم إزالة الخلفية لاحقاً ✂️")

# معرفة عدد المستخدمين
async def count_users(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not os.path.exists(USERS_FILE):
        await update.message.reply_text("لا يوجد مستخدمين حالياً.")
        return
    with open(USERS_FILE, "r") as f:
        users = f.read().splitlines()
    await update.message.reply_text(f"عدد المستخدمين الحاليين: {len(users)}")

def main():
    app = ApplicationBuilder().token(TOKEN).build()

    # أوامر
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("image", text_to_image))
    app.add_handler(CommandHandler("removebg", remove_bg))
    app.add_handler(CommandHandler("users", count_users))

    # تشغيل البوت
    app.run_polling()

if __name__ == "__main__":
    main()