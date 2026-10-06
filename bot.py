from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ConversationHandler,
    ContextTypes,
    filters,
    CallbackQueryHandler
)  

from jobs import *
from weather import *
from prices import *
from help import *
from news import *
from qr import *
from converter import *
from cvPhoto import *

from states import *
from keyboards import reply_markup





app = Application.builder().token(TOKEN).build()



async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 مرحبًا بك في Smart Services Bot اختر الخدمة التي تريدها.",
        reply_markup=reply_markup
    )

app.add_handler(CommandHandler("start", start))


conv_handler = ConversationHandler(
    entry_points=[
        MessageHandler(filters.Regex("^🌤️ الطقس$"), weather), 
        MessageHandler(filters.Regex("^💼 الوظائف$"), jobs),
        MessageHandler(filters.Regex("^💰 الأسعار$"), prices),
        MessageHandler(filters.Regex("^ℹ️ المساعدة$"), help_command),
        MessageHandler(filters.Regex("^📰 الأخبار$"), news),
        MessageHandler(filters.Regex("^📷 QR Code$"), qr_start),
        MessageHandler(filters.Regex("^📂 تحويل الملفات$"), converter_start),
        MessageHandler(filters.Regex("^📄 CV Photo$"), cv_start)
    ],
    states={
        CITY: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_weather)],
        JOB: [CallbackQueryHandler(jobs_callback)],
        CITY_PYTHON_JOB: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_python_jobs)],
        CITY_WEB_JOB: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_web_jobs)],
        CITY_JAVA_JOB: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_java_jobs)],
        PRICE: [CallbackQueryHandler(get_prices)],
        NEWS: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_news)],
        QR: [
                CallbackQueryHandler(qr_type),
                MessageHandler(filters.TEXT & ~filters.COMMAND, generate_qr)
            ],
        CONVERTER: [CallbackQueryHandler(converter_type)],
        CONVERTER_TYPE: [CallbackQueryHandler(send_document)],
        CONVERTE_FILE: [
                            MessageHandler(filters.Document.ALL,convert_document),
                            MessageHandler(filters.PHOTO, photo_handler)
                        ],
        CV_PHOTO: [MessageHandler(filters.PHOTO, improve_cv_photo)]
        
    },
    fallbacks=[],
)

app.add_handler(conv_handler)

app.run_polling()