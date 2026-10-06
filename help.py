from telegram import Update
from telegram.ext import ContextTypes


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        '''🤖 مرحبًا بك في Smart Services Bot

        يمكنك استخدام الخدمات التالية:

        🌤️ الطقس
        • اضغط على زر "الطقس".
        • اكتب اسم المدينة.
        • سيعرض لك البوت حالة الطقس.

        💼 الوظائف
        • اضغط على زر "الوظائف".
        • اختر التخصص (Python / Web / Java).
        • اكتب اسم المدينة.
        • سيعرض لك البوت الوظائف المتوفرة.

        💰 الأسعار
        • اضغط على زر "الأسعار".
        • اختر العملة (USD / EUR / GBP).
        • سيعرض لك سعرها مقابل الدرهم المغربي (MAD).

        إذا واجهت أي مشكلة، أعد كتابة /start لإعادة تشغيل البوت.''')