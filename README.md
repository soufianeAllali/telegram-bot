Telegram Bot

A multifunctional Telegram bot developed with Python, providing several useful services directly through Telegram.

✨ Features

The bot provides a variety of services, including:

- 🌤️ Weather — Get current weather information.
- 💱 Currency Exchange Rates — Check currency exchange rates.
- 📰 News — Get the latest news and updates.
- 🔲 QR Code — Generate QR codes.
- 📄 File Conversion — Convert files between different formats.
- 📸 CV Photo — Create or prepare a professional photo suitable for a CV.
- 🤖 More useful services — Additional features integrated into the bot.

🛠️ Technologies

- Python
- Telegram Bot API
- APIs for external services
- Environment variables for secure configuration

📦 Installation

Clone the repository:

git clone https://github.com/USERNAME/telegram-bot.git

Install dependencies:

pip install -r requirements.txt

Create a ".env" file and add your Telegram Bot Token:

BOT_TOKEN=YOUR_BOT_TOKEN

Run the bot:

python bot.py

🔐 Security

The ".env" file contains sensitive information such as the Telegram Bot Token and should never be uploaded to GitHub.

Make sure ".env" is included in ".gitignore".

📁 Project Structure

telegram-bot/
│
├── bot.py
├── requirements.txt
├── README.md
├── .gitignore
└── .env

«Note: ".env" is used locally and should not be committed to the repository.»

👨‍💻 About

This project is a Python-based multifunctional Telegram bot designed to provide useful everyday services through a simple Telegram interface.
