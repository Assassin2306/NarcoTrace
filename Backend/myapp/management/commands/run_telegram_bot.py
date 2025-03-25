import telebot
import requests
import json
import logging
from datetime import datetime
from django.core.management.base import BaseCommand
from django.conf import settings

# Set up logging
logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Run the Telegram bot for message monitoring'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting Telegram bot...'))
        self.run_bot()

    def run_bot(self):
        # Initialize the bot
        TOKEN = getattr(settings, 'TELEGRAM_BOT_TOKEN', '7542364390:AAERWwMOx0gipfrlsBQ1Kga3YDfRS2BXl8I')
        bot = telebot.TeleBot(TOKEN)

        # Define the send_to_django function
        def send_to_django(message, user_id, chat_id):
            # Use settings.BASE_URL or default to localhost
            base_url = getattr(settings, 'BASE_URL', 'http://127.0.0.1:8000')
            url = f'{base_url}/flagged_message/'
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
                
                self.stdout.write(f"Received message from user {user_id} in chat {chat_id}")
                
                # Send message data to Django
                result = send_to_django(message, user_id, chat_id)
                
                # Only show response for flagged messages
                if result.get('status') == 'flagged':
                    bot.reply_to(message, "🚨 Message Flagged")
                    self.stdout.write(self.style.WARNING(f"Flagged message from user {user_id}"))
                else:
                    self.stdout.write(self.style.SUCCESS(f"Safe message from user {user_id}"))
                
            except Exception as e:
                logger.error(f"Error in handle_message: {e}")
                self.stdout.write(self.style.ERROR(f"Error handling message: {e}"))

        # Start the bot
        logger.info("Bot starting...")
        self.stdout.write(self.style.SUCCESS('Bot started and waiting for messages...'))
        
        try:
            bot.polling(none_stop=True)
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Bot error: {e}"))
            logger.error(f"Bot polling error: {e}") 