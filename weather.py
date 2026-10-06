from telegram import Update, ReplyKeyboardRemove
from telegram.ext import ContextTypes, ConversationHandler

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from states import *
from keyboards import reply_markup

async def weather(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🌤️ من فضلك أدخل اسم المدينة لمعرفة الطقس:",
        reply_markup=ReplyKeyboardRemove()
    )
    return CITY

async def get_weather(update: Update, context: ContextTypes.DEFAULT_TYPE):
    driver = webdriver.Chrome()
    driver.get("https://soufianeallali.github.io/weather-app")
    city_name = update.message.text
    city_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//*[@id='root']/form/input[1]"))
    )
    city_input.clear()
    city_input.send_keys(city_name)
    city_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//*[@id='root']/form/input[2]"))
    )
    city_button.click()
    weather_info = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//*[@id='root']/div/div[2]/div/div[2]/div[2]/h1"))
    )
    await update.message.reply_text(f"🌤️ الطقس في {city_name}: {weather_info.text}", reply_markup=reply_markup)
    driver.quit()
    return ConversationHandler.END
