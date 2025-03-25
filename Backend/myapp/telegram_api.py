from telethon import TelegramClient
import asyncio

# Replace these values with your credentials
api_id = '20375089'
api_hash = '09c34d7b95636fcb10ea1c278828fa59'
phone_number = '+919921634195'

# Initialize the Telegram client
client = TelegramClient('session_name', api_id, api_hash)

# Start the client in a background task
async def start_client():
    await client.start(phone_number)

# Ensure the client is started before making API calls
async def get_user_info(user_id):
    try:
        # Make sure the client is started
        if not client.is_user_logged_in:
            await start_client()
        user = await client.get_entity(user_id)
        return user.username or 'No Username'
    except Exception as e:
        print(f'Error fetching user info: {e}')
        return 'Unknown User'

async def get_group_info(chat_id):
    try:
        # Make sure the client is started
        if not client.is_user_logged_in:
            await start_client()
        chat = await client.get_entity(chat_id)
        return chat.title or 'No Group Name'
    except Exception as e:
        print(f'Error fetching group info: {e}')
        return 'Unknown Group'

# Ensure the client is started when the script runs
if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(start_client())
