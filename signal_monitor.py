from telethon import TelegramClient, events
from telethon.errors import SessionPasswordNeededError
from twilio.rest import Client
import os

# Telegram credentials from environment variables
API_ID = int(os.getenv('API_ID', '34697244'))
API_HASH = os.getenv('API_HASH', '278f850d9fe8824e595bdb22863a45bb')
PHONE = os.getenv('PHONE', '+2348146530754')
CHANNEL_ID = int(os.getenv('CHANNEL_ID', '-2573424084'))

# Twilio credentials from environment variables
TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID', '')
TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN', '')
TWILIO_NUMBER = os.getenv('TWILIO_NUMBER', '')
YOUR_PHONE = os.getenv('YOUR_PHONE', '')

# Create Telegram client with phone parameter
telegram_client = TelegramClient('signal_session', API_ID, API_HASH)

# Create Twilio client
twilio_client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

@telegram_client.on(events.NewMessage(chats=CHANNEL_ID))
async def handler(event):
    message = event.message.text
    print(f"🚨 SIGNAL RECEIVED: {message}")
    
    # Send SMS alert
    try:
        if TWILIO_ACCOUNT_SID and TWILIO_AUTH_TOKEN and TWILIO_NUMBER and YOUR_PHONE:
            sms = twilio_client.messages.create(
                body=f"📊 SIGNAL ALERT:\n\n{message[:160]}",
                from_=TWILIO_NUMBER,
                to=YOUR_PHONE
            )
            print(f"✅ SMS sent! Message ID: {sms.sid}")
        else:
            print("⚠️ Twilio credentials missing")
    except Exception as e:
        print(f"❌ SMS failed: {e}")
    
    # Also save to Telegram Saved Messages
    try:
        await telegram_client.send_message('me', f"📊 SIGNAL ALERT:\n\n{message}")
    except Exception as e:
        print(f"❌ Saved message failed: {e}")

async def main():
    print("🔍 Monitoring your Telegram channel...")
    print("Ready to send SMS alerts!")
    print(f"Connecting to channel: {CHANNEL_ID}")
    
    try:
        async with telegram_client:
            print("✅ Connected to Telegram!")
            await telegram_client.run_until_disconnected()
    except Exception as e:
        print(f"❌ Connection error: {e}")
        print("Retrying in 30 seconds...")
        import asyncio
        await asyncio.sleep(30)
        await main()

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
