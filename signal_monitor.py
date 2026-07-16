from telethon import TelegramClient, events

API_ID = 34697244
API_HASH = '278f850d9fe8824e595bdb22863a45bb'
PHONE = '+2348146530754'
CHANNEL_ID = -2573424084

client = TelegramClient('session', API_ID, API_HASH)

@client.on(events.NewMessage(chats=CHANNEL_ID))
async def handler(event):
    message = event.message.text
    print(f"🚨 SIGNAL RECEIVED: {message}")
    await client.send_message('me', f"📊 SIGNAL ALERT:\n\n{message}")

print("🔍 Monitoring your Telegram channel...")
with client:
    client.run_until_disconnected()
