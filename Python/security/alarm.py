#!/usr/bin/python
"""
This Raspberry Pi code was developed by newbiely.com
This Raspberry Pi code is made available for public use without any restriction
For comprehensive instructions and wiring diagrams, please visit:
https://newbiely.com/tutorials/raspberry-pi/raspberry-pi-door-sensor
"""
import RPi.GPIO as GPIO
import time
import os
import asyncio
import secrets_precios
from telegram import Bot

DOOR_FILE_TO_CHECK = "/tmp/main_door_alarm.open"
KITCHEN_FILE_TO_CHECK = "/tmp/kitchen_door_alarm.open"
GARAGE_FILE_TO_CHECK = "/tmp/garage_door_alarm.open"

# Set the GPIO mode to BCM
GPIO.setmode(GPIO.BCM)

# Define the GPIO pin number to which the sensor is connected
DOOR_SENSOR_PIN = 20
KITCHEN_DOOR_SENSOR_PIN = 16
GARAGE_DOOR_SENSOR_PIN = 26


BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN', secrets_precios.TELEGRAM_TOKEN)
TARGET_USER_CHAT_ID = "8168231240" # Make sure this is the correct numeric chat ID!

# Setup the GPIO pin as an input
GPIO.setup(DOOR_SENSOR_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(KITCHEN_DOOR_SENSOR_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(GARAGE_DOOR_SENSOR_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

async def send_one_off_message(chat_id: str, message_text: str):
    """Sends a single message to a specified chat ID."""
    bot = Bot(token=BOT_TOKEN)
    try:
        async with bot:
            await bot.send_message(chat_id=chat_id, text=message_text)
        print(f"Message sent successfully to chat ID {chat_id}")
    except Exception as e:
        print(f"Error sending message to {chat_id}: {e}")


if os.path.exists(DOOR_FILE_TO_CHECK):
    os.remove(DOOR_FILE_TO_CHECK)

if os.path.exists(KITCHEN_FILE_TO_CHECK):
    os.remove(KITCHEN_FILE_TO_CHECK)

if os.path.exists(GARAGE_FILE_TO_CHECK):
    os.remove(GARAGE_FILE_TO_CHECK)

try:
    while True:
        # Read the state of the door sensor (HIGH when open, LOW when closed)
        door_state = GPIO.input(DOOR_SENSOR_PIN)
        if door_state == GPIO.HIGH:
            print("Main Door is OPEN")
            if not os.path.exists(DOOR_FILE_TO_CHECK):
                with open(DOOR_FILE_TO_CHECK, "w") as f:
                    f.write("This is some content for the new file.")
                    message = "La puerta principal ha sido abierta."
                    asyncio.run(send_one_off_message(TARGET_USER_CHAT_ID, message))
        else:
            print("Main Door is CLOSED")
            if os.path.exists(DOOR_FILE_TO_CHECK):
                os.remove(DOOR_FILE_TO_CHECK)
                message = "La puerta principal fue cerrada"
                asyncio.run(send_one_off_message(TARGET_USER_CHAT_ID, message))

        door_state = GPIO.input(KITCHEN_DOOR_SENSOR_PIN)
        if door_state == GPIO.HIGH:
            print("Kitchen Door is OPEN")
            if not os.path.exists(KITCHEN_FILE_TO_CHECK):
                with open(KITCHEN_FILE_TO_CHECK, "w") as f:
                    f.write("This is some content for the new file.")
                    message = "La puerta Cocina ha sido abierta."
                    asyncio.run(send_one_off_message(TARGET_USER_CHAT_ID, message))
        else:
            print("Kitchen Door is CLOSED")
            if os.path.exists(KITCHEN_FILE_TO_CHECK):
                os.remove(KITCHEN_FILE_TO_CHECK)
                message = "La puerta Cocina fue cerrada"
                asyncio.run(send_one_off_message(TARGET_USER_CHAT_ID, message))

        door_state = GPIO.input(GARAGE_DOOR_SENSOR_PIN)
        if door_state == GPIO.HIGH:
            print("Garage Door is OPEN")
            if not os.path.exists(GARAGE_FILE_TO_CHECK):
                with open(GARAGE_FILE_TO_CHECK, "w") as f:
                    f.write("This is some content for the new file.")
                    message = "La puerta Garage ha sido abierta."
                    asyncio.run(send_one_off_message(TARGET_USER_CHAT_ID, message))
        else:
            print("Garage Door is CLOSED")
            if os.path.exists(GARAGE_FILE_TO_CHECK):
                os.remove(GARAGE_FILE_TO_CHECK)
                message = "La puerta Garage fue cerrada"
                asyncio.run(send_one_off_message(TARGET_USER_CHAT_ID, message))

        time.sleep(0.6)  # Add a small delay to avoid excessive reads

except KeyboardInterrupt:
    print("Exiting...")
    GPIO.cleanup()


