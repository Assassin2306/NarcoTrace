import telebot
import requests
import django
import os
import json
from datetime import datetime
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Set up Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')  
django.setup()

# Initialize the bot
TOKEN = '7542364390:AAERWwMOx0gipfrlsBQ1Kga3YDfRS2BXl8I'  
bot = telebot.TeleBot(TOKEN)

def send_to_django(message, user_id, chat_id):
    url = 'http://127.0.0.1:8000/flagged_message/'  # Make sure this matches the Django URL pattern
    timestamp = datetime.utcfromtimestamp(message.date).isoformat()
    
    payload = {
        'message': message.text,
        'user_id': str(user_id),
        'chat_id': str(chat_id),
        'timestamp': timestamp
    }
    
    try:
        logger.debug(f"Sending payload: {payload}")
        
        response = requests.post(
            url,
            json=payload,
            headers={'Content-Type': 'application/json'},
            timeout=10
        )
        
        response_text = response.text
        logger.debug(f"Response status: {response.status_code}")
        logger.debug(f"Response content: {response_text}")
        
        if response.status_code == 200:
            return response.json()
        else:
            try:
                error_data = response.json()
                error_msg = error_data.get('message', f"Server error: {response.status_code}")
            except json.JSONDecodeError:
                error_msg = f"Server error: {response.status_code} - {response_text}"
            logger.error(error_msg)
            return {'status': 'error', 'message': error_msg}
            
    except requests.exceptions.RequestException as e:
        error_msg = f"Connection error: {str(e)}"
        logger.error(error_msg)
        return {'status': 'error', 'message': error_msg}
    except Exception as e:
        error_msg = f"Unexpected error: {str(e)}"
        logger.error(error_msg)
        return {'status': 'error', 'message': error_msg}

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    try:
        user_id = message.from_user.id
        chat_id = message.chat.id
        
        # Send message data to Django
        result = send_to_django(message, user_id, chat_id)
        
        # Only show response for flagged messages
        if result.get('status') == 'flagged':
            bot.reply_to(message, "🚨 Message Flagged")
        
    except Exception as e:
        logger.error(f"Error in handle_message: {e}")

if __name__ == '__main__':
    logger.info("Bot starting...")
    bot.polling(none_stop=True)
