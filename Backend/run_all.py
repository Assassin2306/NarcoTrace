#!/usr/bin/env python
"""
Helper script to run both the Django server and the Telegram bot.
Usage: python run_all.py
"""

import os
import sys
import subprocess
import threading
import time
import signal

# Flag to track if we should shut down
should_exit = False

def signal_handler(sig, frame):
    global should_exit
    print("\nShutting down gracefully...")
    should_exit = True

# Register signal handler for Ctrl+C
signal.signal(signal.SIGINT, signal_handler)

def run_django_server():
    """Run the Django development server"""
    print("Starting Django server...")
    server_process = subprocess.Popen(
        [sys.executable, "manage.py", "runserver"], 
        stdout=subprocess.PIPE, 
        stderr=subprocess.STDOUT,
        bufsize=1,
        universal_newlines=True
    )
    
    try:
        # Print output in real-time
        for line in server_process.stdout:
            print(f"[Django] {line.strip()}")
            if should_exit:
                break
    finally:
        print("Stopping Django server...")
        server_process.terminate()
        try:
            server_process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            server_process.kill()

def run_telegram_bot():
    """Run the Telegram bot"""
    print("Starting Telegram bot...")
    # Wait a bit to let Django start up first
    time.sleep(3)
    
    bot_process = subprocess.Popen(
        [sys.executable, "manage.py", "run_telegram_bot"], 
        stdout=subprocess.PIPE, 
        stderr=subprocess.STDOUT,
        bufsize=1,
        universal_newlines=True
    )
    
    try:
        # Print output in real-time
        for line in bot_process.stdout:
            print(f"[Bot] {line.strip()}")
            if should_exit:
                break
    finally:
        print("Stopping Telegram bot...")
        bot_process.terminate()
        try:
            bot_process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            bot_process.kill()

if __name__ == "__main__":
    # Make sure we're in the right directory
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    # Start each service in its own thread
    django_thread = threading.Thread(target=run_django_server)
    bot_thread = threading.Thread(target=run_telegram_bot)
    
    django_thread.start()
    bot_thread.start()
    
    try:
        # Wait for both threads to complete
        while django_thread.is_alive() or bot_thread.is_alive():
            time.sleep(1)
            if should_exit:
                break
    except KeyboardInterrupt:
        # If Ctrl+C is pressed, the signal handler will set should_exit
        pass
    
    print("All services stopped.") 