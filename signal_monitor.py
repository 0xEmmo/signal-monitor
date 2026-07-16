from telethon import TelegramClient, events
from twilio.rest import Client
import os

# Telegram credentials
API_ID = 34697244
API_HASH = '278f850d9fe8824e595bdb22863a45bb'
PHONE = '+2348146530754'
CHANNEL_ID = -2573424084

# Twilio credentials
TWILIO_ACCOUNT_SID = 'ACfdf234f17d3fa426ae8c8152ea440093'
TWILIO_AUTH_TOKEN = '79eacfaf6b2cf7e50d96973f289449a4'
TWILIO_NUMBER = '+1 478 778 9981'
YOUR_PHONE = '+2347074099721'

# Create Telegram client
telegram_client = TelegramClient('session', API_ID, API_HASH)

# Create Twilio client
twilio_client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

@telegram_client.on(events.NewMessage(chats=CHANNEL_ID))
async def handler(event):
    message = event.message.text
    print(f"🚨 SIGNAL RECEIVED: {message}")
    
    # Send SMS alert
    try:
        sms = twilio_client.messages.create(
            body=f"📊 SIGNAL ALERT:\n\n{message[:160]}",
            from_=TWILIO_NUMBER,
            to=YOUR_PHONE
        )
        print(f"✅ SMS sent! Message ID: {sms.sid}")
    except Exception as e:
        print(f"❌ SMS failed: {e}")
    
    # Also save to Telegram
    await telegram_client.send_message('me', f"📊 SIGNAL ALERT:\n\n{message}")

print("🔍 Monitoring your Telegram channel...")
print("Ready to send SMS alerts!")
with telegram_client:
    telegram_client.run_until_disconnected()
