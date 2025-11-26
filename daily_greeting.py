import os
import requests
from datetime import datetime
import schedule
import time
from groq import Groq

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
        model="llama3-8b-8192",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=100,
        temperature=0.9
    )
    return response.choices[0].message.content.strip()

def send_daily_greeting():
    greeting = generate_greeting()
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": greeting}
    requests.post(url, data=payload)
    print(datetime.now(), "- ارسال شد:", greeting)

schedule.every().day.at("04:30").do(send_daily_greeting)  # ۸ صبح ایران

print("ربات سلام روزانه فعال شد...")
while True:
    schedule.run_pending()
    time.sleep(60)
