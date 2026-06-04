import telebot
import sqlite3
import datetime
import threading
import time
import os

# The token is read securely from the Render environment variable
TOKEN = os.environ.get('API_TOKEN')
GROUP_ID = -1004250088932

# Admin IDs
ADMIN_IDS = [6794495658, 7368666569] 

bot = telebot.TeleBot(TOKEN)

conn = sqlite3.connect('users.db', check_same_thread=False)
cursor = conn.cursor()
cursor.execute('CREATE TABLE IF NOT EXISTS users (user_id INTEGER PRIMARY KEY, start_date TEXT)')
conn.commit()

@bot.message_handler(content_types=['new_chat_members'])
def auto_add_user(message):
    for member in message.new_chat_members:
        if member.id not in ADMIN_IDS:
            start_date = datetime.datetime.now().strftime('%Y-%m-%d')
            cursor.execute('INSERT OR REPLACE INTO users (user_id, start_date) VALUES (?, ?)', (member.id, start_date))
            conn.commit()

@bot.message_handler(commands=['add'])
def add_user(message):
    try:
        user_id = int(message.text.split()[1])
        if user_id not in ADMIN_IDS:
            start_date = datetime.datetime.now().strftime('%Y-%m-%d')
            cursor.execute('INSERT OR REPLACE INTO users (user_id, start_date) VALUES (?, ?)', (user_id, start_date))
            conn.commit()
            bot.reply_to(message, "User added successfully.")
        else:
            bot.reply_to(message, "This user is an admin.")
    except:
        bot.reply_to(message, "Usage: /add <user_id>")

def check_and_kick():
    while True:
        try:
            today = datetime.datetime.now()
            cursor.execute('SELECT user_id, start_date FROM users')
            for user in cursor.fetchall():
                uid, sdate = user
                if uid in ADMIN_IDS:
                    continue
                
                start_date = datetime.datetime.strptime(sdate, '%Y-%m-%d')
                if (today - start_date).days >= 30:
                    try:
                        bot.ban_chat_member(GROUP_ID, uid)
                        cursor.execute('DELETE FROM users WHERE user_id = ?', (uid,))
                        conn.commit()
                    except: pass
        except: pass
        time.sleep(86400)

threading.Thread(target=check_and_kick, daemon=True).start()

print("Bot is running...")
bot.infinity_polling()
