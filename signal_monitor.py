from telethon import TelegramClient, events
from twilio.rest import Client
import os

API_ID = int(os.getenv('API_ID', '34697244'))
API_HASH = os.getenv('API_HASH', '278f850d9fe8824e595bdb22863a45bb')
PHONE = os.getenv('PHONE', '+2348146530754')
CHANNEL_ID = int(os.getenv('CHANNEL_ID', '-2573424084'))

TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID', '')
TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN', '')
TWILIO_NUMBER = os.getenv('TWILIO_NUMBER', '')
YOUR_PHONE = os.getenv('YOUR_PHONE', '')

telegram_client = TelegramClient('signal_session', API_ID, API_HASH)
twilio_client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

@telegram_client.on(events.NewMessage(chats=CHANNEL_ID))
async def handler(event):
    message = event.message.text
    
    print(f"🚨 NEW MESSAGE: {message}")
    
    # Send phone call for EVERY message
    try:
        if TWILIO_ACCOUNT_SID and TWILIO_AUTH_TOKEN and TWILIO_NUMBER and YOUR_PHONE:
            twiml = f"""<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Say voice="alice">Signal update! {message[:100]}</Say>
    <Pause length="2"/>
    <Say voice="alice">Check Telegram for details.</Say>
</Response>"""
            
            call = twilio_client.calls.create(
                to=YOUR_PHONE,
                from_=TWILIO_NUMBER,
                twiml=twiml
            )
            print(f"✅ CALL sent! SID: {call.sid}")
    except Exception as e:
        print(f"❌ Call failed: {e}")
    
    try:
        await telegram_client.send_message('me', f"📊 UPDATE:\n\n{message}")
    except Exception as e:
        print(f"⚠️ Telegram save failed: {e}")

async def main():
    print("🔍 Monitoring all messages...")
    print("Ready to send PHONE CALL for EVERY message!")
    
    try:
        async with telegram_client:
            print("✅ Connected to Telegram!")
            await telegram_client.run_until_disconnected()
    except Exception as e:
        print(f"❌ Error: {e}")
        import asyncio
        await asyncio.sleep(30)
        await main()

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
