from telethon import TelegramClient, events
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

# Create Telegram client
telegram_client = TelegramClient('signal_session', API_ID, API_HASH)

# Create Twilio client
twilio_client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

def is_new_signal(message):
    """Check if message is a NEW TRADE SIGNAL (not TP/SL update)"""
    message_upper = message.upper()
    
    # Keywords that indicate a NEW SIGNAL
    signal_keywords = ['BUY NOW', 'SELL NOW', 'BUY', 'SELL', 'LONG', 'SHORT']
    
    # Keywords that indicate TP/SL updates (ignore these)
    ignore_keywords = ['TAKE PROFIT', 'TP1', 'TP2', 'TP3', 'TP4', 'TP5', 'STOP LOSS', 'SL:', 'CLOSED']
    
    # If message contains ignore keywords, it's probably just an update
    for ignore_keyword in ignore_keywords:
        if ignore_keyword in message_upper:
            return False
    
    # Check if it contains signal keywords
    for signal_keyword in signal_keywords:
        if signal_keyword in message_upper:
            return True
    
    return False

@telegram_client.on(events.NewMessage(chats=CHANNEL_ID))
async def handler(event):
    message = event.message.text
    
    # Check if this is a NEW SIGNAL (not TP/SL update)
    if not is_new_signal(message):
        print(f"📍 Update received (not a new signal): {message[:50]}...")
        return
    
    print(f"🚨 NEW SIGNAL DETECTED: {message}")
    
    # Send PHONE CALL alert
    try:
        if TWILIO_ACCOUNT_SID and TWILIO_AUTH_TOKEN and TWILIO_NUMBER and YOUR_PHONE:
            # Extract key info from message
            signal_text = message[:100]
            
            # Create TwiML for the call
            twiml = f"""<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Say voice="alice">New signal alert! {signal_text}</Say>
    <Pause length="2"/>
    <Say voice="alice">Check your Telegram immediately.</Say>
</Response>"""
            
            call = twilio_client.calls.create(
                to=YOUR_PHONE,
                from_=TWILIO_NUMBER,
                twiml=twiml
            )
            print(f"✅ CALL SENT! Call SID: {call.sid}")
        else:
            print("⚠️ Twilio credentials missing")
    except Exception as e:
        print(f"❌ Call failed: {e}")
    
    # Also save to Telegram Saved Messages
    try:
        await telegram_client.send_message('me', f"📊 NEW SIGNAL:\n\n{message}")
    except Exception as e:
        print(f"❌ Saved message failed: {e}")

async def main():
    print("🔍 Monitoring your Telegram channel for NEW SIGNALS...")
    print("Ready to send PHONE CALL alerts!")
    print("(Ignoring TP/SL updates)")
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
