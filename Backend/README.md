# NarcoTrace Backend

Backend server for the NarcoTrace application including a Django API for message monitoring and a Telegram bot for receiving messages.

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run migrations:
```bash
python manage.py migrate
```

## Running the Application

There are multiple ways to run the application:

### Option 1: Run Everything Together

Use the helper script to run both the Django server and the Telegram bot:

```bash
python run_all.py
```

### Option 2: Run Components Separately

Run the Django server:
```bash
python manage.py runserver
```

Run the Telegram bot (in a separate terminal):
```bash
python manage.py run_telegram_bot
```

## Configuration

Configuration settings are in `myproject/settings.py`:

- `TELEGRAM_BOT_TOKEN`: Your Telegram bot token
- `BASE_URL`: URL where the Django server is running

## API Endpoints

- `/flagged_message/`: Get all messages or post a new message
- `/status/`: Check if the API is running
- `/all-messages/`: Get all messages (including non-flagged ones)
- `/batch_delete_messages/`: Delete multiple messages by ID

## Telegram Bot

The Telegram bot is integrated with the Django backend. It receives messages from Telegram users and sends them to the Django API for analysis. If a message is flagged, the bot replies to the user.

### Bot Functionality

1. Listens for messages from Telegram users
2. Sends messages to the Django API for analysis
3. Replies to users when a message is flagged 