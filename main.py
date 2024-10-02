import asyncio
import json
import datetime
import traceback
from telethon import TelegramClient, events
import pyautogui
import pyscreeze
from colorama import Fore, init
from collections import deque
import time

# Initialize colorama
init(autoreset=True)

# Load configuration from a JSON file
with open('config.json') as config_file:
    config = json.load(config_file)

api_id = config['api_id']
api_hash = config['api_hash']
channels = config['channels']
output_chat = config['output_chat']
json_file_path = config['json_file_path']
image_paths = config['image_paths']

# Initialize Telegram client
client = TelegramClient('TelegramSession', api_id, api_hash)

# Initialize message queue and sets
message_queue = deque()  # Using deque for thread-safe and efficient operations
processed_messages = set()

# Load previously filtered messages from JSON file
try:
    with open(json_file_path, 'r') as file:
        filtered_messages = json.load(file)
except FileNotFoundError:
    filtered_messages = []

# Helper function to save messages to a JSON file
def save_messages():
    with open(json_file_path, 'w') as file:
        json.dump(filtered_messages, file, indent=4)

# Helper function to search and click on an image with retry logic
async def search_and_click(image_path, retries=3, delay=0.5):
    for attempt in range(retries):
        location = pyscreeze.locateCenterOnScreen(image_path)
        if location:
            pyautogui.click(location)
            return True
        print(Fore.YELLOW + f"Attempt {attempt + 1}/{retries}: Image '{image_path}' not found.")
        await asyncio.sleep(delay)
    return False

@client.on(events.NewMessage(chats=channels))
async def new_message_handler(event):
    message = event.message.message.strip()
    reception_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    sender = event.sender.username if event.sender and event.sender.username else 'Unknown'

    # Filter messages
    if len(message) != 8 or '/' in message or '.'in message or ' ' in message or message in processed_messages :
        return

    message_info = {
        "message": message,
        "reception_time": reception_time,
        "sender": sender
    }

    # Queue the message for processing
    message_queue.append(message_info)
    processed_messages.add(message)
    filtered_messages.append(message_info)
    save_messages()

    print(Fore.GREEN + f"Message approved: {message}")

    # Send the formatted message to the output chat
    monospaced_message = f"`\n{message}\n`"
    try:
        await client.send_message(output_chat, monospaced_message, parse_mode='markdown')
    except Exception as e:
        print(Fore.RED + f"Error sending message: {e}")
        


image_cache = {}

async def search_and_click(image_path, retries=3, delay=0.5):
    if image_path in image_cache:
        location = image_cache[image_path]
        pyautogui.click(location)
        return True

    for attempt in range(retries):
        location = pyscreeze.locateCenterOnScreen(image_path)
        if location:
            image_cache[image_path] = location  # Guardar ubicación
            pyautogui.click(location)
            return True
        print(Fore.YELLOW + f"Attempt {attempt + 1}/{retries}: Image '{image_path}' not found.")
        await asyncio.sleep(delay)
    return False

#funcion para medir el tiempo  

import time

async def search_and_click(image_path, retries=3, delay=0.5):
    start_time = time.time()  # Medir tiempo de búsqueda
    for attempt in range(retries):
        location = pyscreeze.locateCenterOnScreen(image_path)
        if location:
            pyautogui.click(location)
            print(f"Image '{image_path}' found and clicked in {time.time() - start_time} seconds.")
            return True
        print(Fore.YELLOW + f"Attempt {attempt + 1}/{retries}: Image '{image_path}' not found.")
        await asyncio.sleep(delay)
    print(f"Image '{image_path}' not found after {time.time() - start_time} seconds.")
    return False


#funcion principal 

async def process_messages():
    while True:
        if message_queue:
            message_info = message_queue.popleft()  # Using popleft for better efficiency with deque
            message = message_info["message"]
            
            
            start_time = time.time()  # Empieza a medir tiempo
            try:
                print('Starting message processing')

                # Click through the Binance UI to claim the cryptobox
                if await search_and_click(image_paths['ir_binance']):
                    print("Located and clicked on 'IrBinance.png'")
                    if await search_and_click(image_paths['paste_binance']):
                        pyautogui.write(message)
                        print("Pasted message text")
                        await asyncio.sleep(0.1)
                        

                        if await search_and_click(image_paths['claim_now']):
                            print("Claim Now clicked")

                            # Replacing the click on 'open' with a click on coordinates (952, 714) and pressing F5
                            await asyncio.sleep(1)
                            pyautogui.click(952, 674)
                            pyautogui.click(952, 714)
                            print(Fore.YELLOW + "Clicked on coordinates (952, 714)")
                            pyautogui.click(952, 750)
                            await asyncio.sleep(1.5)
                            pyautogui.press('f5')
                            print(Fore.GREEN + "Pressed F5 to refresh")
                            # pyautogui.hotkey('alt', 'tab')
                            print(f"First process finished in {time.time() - start_time} seconds")
                            
                            
                            """  # Inicia el segundo proceso
                            second_process_start = time.time()
                            print('Starting SECOND PROCCES')
                            # Click through the Binance UI to claim the cryptobox vibladi
                            if await search_and_click(image_paths['ir_binance']):
                                
                                if await search_and_click(image_paths['paste_binance']):
                                    pyautogui.write(message)
                                    print("Pasted message text")
                                    await asyncio.sleep(0.1)
                                    
                                    if await search_and_click(image_paths['claim_now']):
                                        print("Claim Now clicked")
                                        # Replacing the click on 'open' with a click on coordinates (952, 714) and pressing F5
                                        await asyncio.sleep(1)
                                        pyautogui.click(952, 674)
                                        pyautogui.click(952, 714)
                                        print(Fore.YELLOW + "Clicked on coordinates (952, 714)")
                                        pyautogui.click(952, 750)
                                        await asyncio.sleep(1.5)
                                        pyautogui.press('f5')
                                        print(Fore.GREEN + "Pressed F5 to refresh")
                                        pyautogui.hotkey('alt', 'tab')
                                        
                                        print(f"Second process finished in {time.time() - second_process_start} seconds")
                            """
                            
                            
                        else:
                            print(Fore.RED + "Claim Now not found, attempting to reload.")
                            pyautogui.press('f5')
                            
                            
                            

            except Exception as e:
                pyautogui.press('f5')
                error_traceback = traceback.format_exc()
                print(Fore.RED + f"Unexpected error: {e}")
                print(Fore.RED + f"Error traceback:\n{error_traceback}")

        await asyncio.sleep(0.001)

async def main():
    await client.start()
    await asyncio.gather(
        process_messages(),
        client.run_until_disconnected()
    )

if __name__ == "__main__":
    asyncio.run(main())
