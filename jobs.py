from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, ConversationHandler
import requests

from states import *
from keyboards import reply_markup

reply_markup_jobs = InlineKeyboardMarkup(
    [
        [InlineKeyboardButton("🐍 Python", callback_data="python")],
        [InlineKeyboardButton("🌐 Web", callback_data="web")],
        [InlineKeyboardButton("☕ Java", callback_data="java")],
    ]
)

async def jobs(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "💼 اختر نوع الوظائف التي تريد البحث عنها:",
        reply_markup=reply_markup_jobs
    )
    return JOB


async def jobs_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if query.data == "python":
        await query.edit_message_text("اختر المدينة للبحث عن وظائف Python:")
        return CITY_PYTHON_JOB
    elif query.data == "web":
        await query.edit_message_text("اختر المدينة للبحث عن وظائف Web:")
        return CITY_WEB_JOB
    elif query.data == "java":
        await query.edit_message_text("اختر المدينة للبحث عن وظائف Java:")
        return CITY_JAVA_JOB



async def get_python_jobs(update: Update, context: ContextTypes.DEFAULT_TYPE):
    city_name = update.message.text
    APP_ID = "39a75cc3"
    APP_KEY = "1ceef05fc2e0afc91b8859ab42501e55"

    url = (
        f"https://api.adzuna.com/v1/api/jobs/gb/search/1"
        f"?app_id={APP_ID}"
        f"&app_key={APP_KEY}"
        f"&what=python"
        f"&where={city_name}"
        f"&results_per_page=5"
        f"&content-type=application/json"
    )

    response = requests.get(url)

    data = response.json()

    job_list = [job["title"] for job in data["results"]]
    await update.message.reply_text(f"💼 وظائف Python في {city_name}:\n" + "\n".join(job_list),reply_markup=reply_markup)
    return ConversationHandler.END

async def get_web_jobs(update: Update, context: ContextTypes.DEFAULT_TYPE):
    city_name = update.message.text
    APP_ID = "39a75cc3"
    APP_KEY = "1ceef05fc2e0afc91b8859ab42501e55"

    url = (
        f"https://api.adzuna.com/v1/api/jobs/gb/search/1"
        f"?app_id={APP_ID}"
        f"&app_key={APP_KEY}"
        f"&what=web"
        f"&where={city_name}"
        f"&results_per_page=5"
        f"&content-type=application/json"
    )

    response = requests.get(url)

    data = response.json()

    job_list = [job["title"] for job in data["results"]]
    await update.message.reply_text(f"💼 وظائف Web في {city_name}:\n" + "\n".join(job_list),reply_markup=reply_markup)
    return ConversationHandler.END

async def get_java_jobs(update: Update, context: ContextTypes.DEFAULT_TYPE):
    city_name = update.message.text
    APP_ID = "39a75cc3"
    APP_KEY = "1ceef05fc2e0afc91b8859ab42501e55"

    url = (
        f"https://api.adzuna.com/v1/api/jobs/gb/search/1"
        f"?app_id={APP_ID}"
        f"&app_key={APP_KEY}"
        f"&what=java"
        f"&where={city_name}"
        f"&results_per_page=5"
        f"&content-type=application/json"
    )

    response = requests.get(url)

    data = response.json()

    job_list = [job["title"] for job in data["results"]]
    await update.message.reply_text(f"💼 وظائف Java في {city_name}:\n" + "\n".join(job_list),reply_markup=reply_markup)
    return ConversationHandler.END