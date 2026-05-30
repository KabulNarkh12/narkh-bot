import schedule
import time
from datetime import datetime
from telegram import Bot
import urllib.request
import json
import os

BOT_TOKEN = os.environ.get('BOT_TOKEN', '8830939229:AAGC-WcUFrOw9RUiI34iGr0cyuTbfMJ-WgY')
CHANNEL_ID = os.environ.get('CHANNEL_ID', '@KabulNarkh12')

SOURCE_CHANNELS = [
    'aqbazjgani',
    'KabulNarkh', 
    'rahimallahjan1',
]

last_rates = {}

def get_rates():
    try:
        url = "https://api.exchangerate-api.com/v4/latest/AFN"
        req = urllib.request.urlopen(url, timeout=10)
        data = json.loads(req.read())
        r = data['rates']
        rates = {}
        if 'USD' in r: rates['🇺🇸 دالر امریکایی'] = round(1/r['USD'], 2)
        if 'EUR' in r: rates['🇪🇺 یورو'] = round(1/r['EUR'], 2)
        if 'GBP' in r: rates['🇬🇧 پوند انگلیسی'] = round(1/r['GBP'], 2)
        if 'PKR' in r: rates['🇵🇰 روپیه پاکستانی'] = round(1/r['PKR'], 2)
        if 'IRR' in r: rates['🇮🇷 تومان ایرانی'] = round(1/r['IRR']*10, 4)
        if 'AED' in r: rates['🇦🇪 درهم اماراتی'] = round(1/r['AED'], 2)
        if 'SAR' in r: rates['🇸 ریال سعودی'] = round(1/r['SAR'], 2)
        if 'TRY' in r: rates['🇹🇷 لیره ترکی'] = round(1/r['TRY'], 2)
        if 'CNY' in r: rates['🇨🇳 یوان چینی'] = round(1/r['CNY'], 2)
        if 'BRL' in r: rates['🇧🇷 ریال برزیلی'] = round(1/r['BRL'], 2)
        if 'INR' in r: rates['🇮🇳 روپیه هندی'] = round(1/r['INR'], 2)
        if 'CAD' in r: rates['🇨🇦 دالر کانادایی'] = round(1/r['CAD'], 2)
        if 'AUD' in r: rates['🇦🇺 دالر استرالیایی'] = round(1/r['AUD'], 2)
        if 'JPY' in r: rates['🇯🇵 ین جاپانی'] = round(1/r['JPY'], 4)
        return rates
    except Exception as e:
        print(f"خطا: {e}")
        return {}

def format_message(rates):
    now = datetime.now().strftime("%Y/%m/%d - %H:%M:%S")
    msg = "━━━━━━━━━━━━━━━━━━\n"
    msg += "💱 نرخ اسعار لحظه‌ای\n"
    msg += "🌍 بازار جهانی\n"
    msg += f"🕐 {now}\n"
    msg += "━━━━━━━━━━━━━━━━━━\n\n"
    for currency, rate in rates.items():
        msg += f"{currency}: {rate} افغانی\n"
    msg += "\n━━━━━━━━━━━━━━━━━━\n"
    msg += "📢 @KabulNarkh12"
    return msg

def check_and_post():
    global last_rates
    print(f"چک کردن - {datetime.now()}")
    rates = get_rates()
    if not rates:
        return
    if rates != last_rates:
        try:
            bot = Bot(token=BOT_TOKEN)
            message = format_message(rates)
            bot.send_message(chat_id=CHANNEL_ID, text=message)
            print("✅ نشر شد!")
            last_rates = rates.copy()
        except Exception as e:
            print(f"خطا: {e}")
    else:
        print("نرخ تغییر نکرده")

schedule.every(1).minutes.do(check_and_post)
print("🚀 ربات شروع کرد...")
check_and_post()

while True:
    schedule.run_pending()
    time.sleep(30)
