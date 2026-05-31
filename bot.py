import asyncio
import os
from datetime import datetime, timezone, timedelta
from telethon import TelegramClient, events
from telethon.sessions import StringSession
import telegram

BOT_TOKEN = "8830939229:AAGC-WcUFrOw9RUiI34iGr0cyuTbfMJ-WgY"
CHANNEL_ID = "@KabulNarkh12"
API_ID = 30837946
API_HASH = "662e0ed8d8ec5772e61a73e6d400ef55"
SESSION_STRING = os.environ.get('SESSION_STRING', '')

SOURCE_CHANNELS = [
    'aqbazjgani',
    'KabulNarkh',
    'rahimallahjan1',
]

def format_message(text, source):
    kabul_time = datetime.now(timezone.utc) + timedelta(hours=4, minutes=30)
    now = kabul_time.strftime("%Y/%m/%d - %H:%M:%S")
    msg = "━━━━━━━━━━━━━━━━━━\n"
    msg += "💱 نرخ اسعار لحظه‌ای\n"
    msg += "🏪 سرای شهزاده کابل\n"
    msg += f"🕐 {now}\n"
    msg += "━━━━━━━━━━━━━━━━━━\n\n"
    msg += text
    msg += "\n\n━━━━━━━━━━━━━━━━━━\n"
    msg += f"📡 منبع: @{source}\n"
    msg += "📢 @KabulNarkh12"
    return msg

async def main():
    print("🚀 ربات شروع کرد...")
    client = TelegramClient(StringSession(SESSION_STRING), API_ID, API_HASH)
    await client.connect()
    print("✅ به تلگرام وصل شد!")

    @client.on(events.NewMessage(chats=SOURCE_CHANNELS))
    async def handler(event):
        try:
            text = event.message.text
            if not text:
                return
            source = event.chat.username
            print(f"✅ پیام جدید از @{source}")
            message = format_message(text, source)
            await client.send_message(CHANNEL_ID, message)
            print("✅ نشر شد!")
        except Exception as e:
            print(f"خطا: {e}")

    print("👂 منتظر پیام‌های جدید...")
    await client.run_until_disconnected()

asyncio.run(main())
