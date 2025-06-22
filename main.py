import logging
from telegram.ext import Updater, MessageHandler, Filters
import sqlite3
import os

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

def log_expense(user_id, text):
    conn = sqlite3.connect("expenses.db")
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS expenses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id TEXT,
        category TEXT,
        amount REAL
    )''')
    try:
        category, amount = text.split()
        amount = float(amount)
        cursor.execute("INSERT INTO expenses (user_id, category, amount) VALUES (?, ?, ?)", (user_id, category, amount))
        conn.commit()
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False
    finally:
        conn.close()

def handle_message(update, context):
    user_id = update.effective_user.id
    text = update.message.text
    if log_expense(user_id, text):
        update.message.reply_text("✅ Expense saved!")
    else:
        update.message.reply_text("❌ Invalid format. Use: Category Amount (e.g., Food 120)")

def main():
    updater = Updater(TELEGRAM_TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
