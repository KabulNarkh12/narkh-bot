import asyncio
import schedule
import time
import re
from datetime import datetime
from telethon.sync import TelegramClient
from telegram import Bot

BOT_TOKEN = "8830939229:AAGC-WcUFrOw9RUiI34iGr0cyuTbfMJ-WgY"
CHANNEL_ID = "@KabulNarkh12"
API_ID = 30837946
API_HASH = "662e0ed8d8ec5772e61a73e6d400ef55"
PHONE = "+93796908504"

SOURCE_CHANNELS = [
    "rahimallahjan1",
    "KabulNarkh",
    "aqbazjgani",
]

def extract_rates(text):
    rates = {}
    patterns = {
        '🇺🇸 دالر': r'دالر[^\d]*(\d+[\.,]\d+|\d+)',
        '🇪🇺 یورو': r'یورو[^\d]*(\d+[\.,]\d+|\d+)',
        '🇬🇧 پوند': r'پوند[^\d]*(\d+[\.,]\d+|\d+)',
        '🇵🇰 روپیه': r'روپیه[^\d]*(\d+[\.,]\d+|\d+)',
        '🇮🇷 تومان': r'تومان[^\d]*(\d+[\.,]\d+|\d+)',
        '🇦🇪 درهم': r'درهم[^\d]*(\d+[\.,]\d+|\d+)',
        '🇸🇦 ریال': r'ریال[^\d]*(\d+[\.,]\d+|\d+)',
        '🇹🇷 لیره': r'لیره[^\d]*(\d+[\.,]\d+|\d+)',
        '🇨🇳 یوان': r'یوان[^\d]*(\d+[\.,]\d+|\d+)',
    }
    for currency, pattern in patterns.items():
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            rates[currency] = match.group(1).replace(',', '.')
    return rates

def format_message(rates):
    now = datetime.now().strftime("%Y/%m/%d - %H:%M")
    msg = "━━━━━━━━━━━━━━━━━━\n"
    msg += "💱 **نرخ اسعار امروز**\n"
    msg += "🏪 سرای شهزاده - کابل\n"
    msg += f"🕐 {now}\n"
    msg += "━━━━━━━━━━━━━━━━━━\n\n"
    for currency, rate in rates.items():
        msg += f"{currency}: {rate} افغانی\n"
    msg += "\n━━━━━━━━━━━━━━━━━━\n"
    msg += "📢 @KabulNarkh12"
    return msg

async def fetch_and_post():
    print(f"شروع - {datetime.now()}")
    all_rates = {}
    try:
        async with TelegramClient('bot_session', API_ID, API_HASH) as client:
            for channel in SOURCE_CHANNELS:
                try:
                    messages = await client.get_messages(channel, limit=10)
                    for msg in messages:
                        if msg.text:
                            rates = extract_rates(msg.text)
                            if len(rates) >= 1:
                                all_rates.update(rates)
                                print(f"✅ نرخ از {channel} گرفته شد")
                                break
                except Exception as e:
                    print(f"خطا در {channel}: {e}")
    except Exception as e:
        print(f"خطا: {e}")

    if all_rates:
        try:
            telegram_bot = Bot(token=BOT_TOKEN)
            message = format_message(all_rates)
            await telegram_bot.send_message(
                chat_id=CHANNEL_ID,
                text=message,
                parse_mode='Markdown'
            )
            print("✅ نشر شد!")
        except Exception as e:
            print(f"خطا در ارسال: {e}")
    else:
        print("❌ نرخی پیدا نشد")

def run():
    asyncio.run(fetch_and_post())

schedule.every(30).minutes.do(run)
print("🚀 ربات شروع کرد...")
run()

while True:
    schedule.run_pending()
    time.sleep(30)
