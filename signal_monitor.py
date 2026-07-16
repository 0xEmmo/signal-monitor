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

def is_new_signal(message):
    message_upper = message.upper()
    signal_keywords = ['BUY NOW', 'SELL NOW', 'BUY', 'SELL', 'LONG', 'SHORT']
    ignore_keywords = ['TAKE PROFIT', 'TP1', 'TP2', 'TP3', 'TP4', 'TP5', 'STOP LOSS', 'SL:', 'CLOSED']
    
    for ignore_keyword in ignore_keywords:
        if ignore_keyword in message_upper:
            return False
    
    for signal_keyword in signal_keywords:
        if signal_keyword in message_upper:
            return True
    
    return False

@telegram_client.on(events.NewMessage(chats=CHANNEL_ID))
async def handler(event):
    message = event.message.text
    
    if not is_new_signal(message):
        print(f"📍 Update (ignored): {message[:50]}...")
        return
    
    print(f"🚨 NEW SIGNAL: {message}")
    
    try:
        if TWILIO_ACCOUNT_SID and TWILIO_AUTH_TOKEN and TWILIO_NUMBER and YOUR_PHONE:
            twiml = f"""<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Say voice="alice">New signal alert! {message[:100]}</Say>
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
        await telegram_client.send_message('me', f"📊 NEW SIGNAL:\n\n{message}")
    except Exception as e:
        print(f"⚠️ Telegram save failed: {e}")

async def main():
    print("🔍 Monitoring for NEW SIGNALS...")
    print("Ready to send PHONE CALL alerts!")
    print("(Ignoring TP/SL updates)")
    
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
