import schedule
import time
import re
from datetime import datetime
from telegram import Bot
import urllib.request
import json

BOT_TOKEN = "8830939229:AAGC-WcUFrOw9RUiI34iGr0cyuTbfMJ-WgY"
CHANNEL_ID = "@KabulNarkh12"

def get_rates_from_web():
    rates = {}
    try:
        url = "https://api.exchangerate-api.com/v4/latest/AFN"
        req = urllib.request.urlopen(url, timeout=10)
        data = json.loads(req.read())
        r = data['rates']
        
        if 'USD' in r: rates['🇺🇸 دالر امریکایی'] = round(1/r['USD'], 2)
        if 'EUR' in r: rates['🇪 یورو'] = round(1/r['EUR'], 2)
        if 'GBP' in r: rates['🇬🇧 پوند'] = round(1/r['GBP'], 2)
        if 'PKR' in r: rates['🇵🇰 روپیه پاکستانی'] = round(1/r['PKR'], 2)
        if 'IRR' in r: rates['🇮🇷 تومان'] = round(1/r['IRR']*10, 2)
        if 'AED' in r: rates['🇦🇪 درهم'] = round(1/r['AED'], 2)
        if 'SAR' in r: rates['🇸🇦 ریال سعودی'] = round(1/r['SAR'], 2)
        if 'TRY' in r: rates['🇹🇷 لیره ترکی'] = round(1/r['TRY'], 2)
        if 'CNY' in r: rates['🇨🇳 یوان چینی'] = round(1/r['CNY'], 2)
        
        print("✅ نرخ‌ها از API گرفته شد")
    except Exception as e:
        print(f"خطا: {e}")
    return rates

def format_message(rates):
    now = datetime.now().strftime("%Y/%m/%d - %H:%M")
    msg = "━━━━━━━━━━━━━━━━━━\n"
    msg += "💱 نرخ اسعار امروز\n"
    msg += "🏪 بازار کابل - افغانستان\n"
    msg += f"🕐 {now}\n"
    msg += "━━━━━━━━━━━━━━━━━━\n\n"
    for currency, rate in rates.items():
        msg += f"{currency}: {rate} افغانی\n"
    msg += "\n━━━━━━━━━━━━━━━━━━\n"
    msg += "📢 @KabulNarkh12"
    return msg

def post_rates():
    print(f"شروع - {datetime.now()}")
    rates = get_rates_from_web()
    if rates:
        try:
            bot = Bot(token=BOT_TOKEN)
            message = format_message(rates)
            bot.send_message(
                chat_id=CHANNEL_ID,
                text=message
            )
            print("✅ نشر شد!")
        except Exception as e:
            print(f"خطا در ارسال: {e}")
    else:
        print("❌ نرخی پیدا نشد")

schedule.every(30).minutes.do(post_rates)
print("🚀 ربات شروع کرد...")
post_rates()

while True:
    schedule.run_pending()
    time.sleep(30)
