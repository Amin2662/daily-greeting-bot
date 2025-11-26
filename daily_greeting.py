import os
import requests
from datetime import datetime
import schedule
import time
from groq import Groq
import threading

# تنظیمات از متغیرهای محیطی
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

client = Groq(api_key=GROQ_API_KEY)

def generate_greeting():
    current_hour = datetime.now().hour
    if 5 <= current_hour < 12:
        time_of_day = "صبح"
    elif 12 <= current_hour < 17:
        time_of_day = "ظهر"
    elif 17 <= current_hour < 21:
        time_of_day = "عصر"
    else:
        time_of_day = "شب"
    
    prompt = f"یک پیام سلام گرم، انگیزشی و کوتاه فارسی بنویس. فقط {time_of_day} بخیر باشه. حداکثر ۲-۳ جمله با ایموجی."

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",  # مدل جدید و پیشنهادی Groq
        messages=[{"role": "user", "content": prompt}],
        max_tokens=100,
        temperature=0.9
    )
    return response.choices[0].message.content.strip()

def send_daily_greeting():
    greeting = generate_greeting()
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": greeting}
    try:
        requests.post(url, data=payload)
        print(f"{datetime.now()} - پیام ارسال شد: {greeting}")
    except Exception as e:
        print("خطا در ارسال پیام:", e)

# اولین سلام همین الان (برای تست)
send_daily_greeting()

# زمان‌بندی روزانه (۸ صبح ایران = 04:30 UTC)
schedule.every().day.at("04:30").do(send_daily_greeting)

# این بخش برای زنده نگه داشتن سرویس Render (هر ۱۰ دقیقه یه پیام چاپ می‌کنه)
def keep_alive():
    count = 0
    while True:
        time.sleep(600)  # هر ۱۰ دقیقه
        count += 1
        print(f"ربات زنده است - {count * 10} دقیقه از شروع گذشت ❤️")

threading.Thread(target=keep_alive, daemon=True).start()

print("ربات سلام روزانه با موفقیت فعال شد و در حال اجراست... 🚀")
