import asyncio
import json
import datetime
import traceback
from telethon.network.connection.tcpabridged import ConnectionTcpAbridged
from telethon import TelegramClient, events
import pyautogui
import pyscreeze
from colorama import Fore, init
from collections import deque
import time
import os


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

#-------------------------TELEGRAM----------------------------------

# Inicializa el cliente con un mayor número de reintentos y un timeout ajustado
client = TelegramClient(
    'TelegramSession',
    api_id,
    api_hash,
    connection=ConnectionTcpAbridged,
    connection_retries=10,  # Número de reintentos
    timeout=30  # Tiempo de espera en segundos
)



# Manejo explícito de errores de conexión
async def connect_with_retry():
    while True:
        try:
            print("Connecting to Telegram...")
            await client.connect()
            if await client.is_user_authorized():
                print("Connected and authorized!")
                break
            else:
                print("Not authorized. Please log in.")
                client.disconnect()  # Elimina 'await' porque este método no es asincrónico
                raise Exception("Authorization failed.")
        except TimeoutError:
            print("Connection timed out. Retrying in 5 seconds...")
            await asyncio.sleep(5)
        except Exception as e:
            print(f"Connection error: {e}. Retrying in 5 seconds...")
            await asyncio.sleep(5)


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


#---------------------------- ESPACIO EN EL QUE EN EL CASO DE NO ENCONTRART LA IMAGEN , INTENTE OTRAS TRES VECES ANTES DE RECARGAR LA PGINA
# async def search_and_click(image_path, retries=3, delay=0.5):
#     start_time = time.time()  # Medir tiempo de búsqueda
#     for attempt in range(retries):
#         location = pyscreeze.locateCenterOnScreen(image_path)
#         if location:
#             pyautogui.click(location)
#             print(f"Image '{image_path}' found and clicked in {time.time() - start_time} seconds.")
#             return True
#         print(Fore.YELLOW + f"Attempt {attempt + 1}/{retries}: Image '{image_path}' not found.")
#         await asyncio.sleep(delay)
#     print(f"Image '{image_path}' not found after {time.time() - start_time} seconds.")
#     return False
#----------------------------------------

# Define la ruta principal para guardar las imágenes
images_dir = 'images'
first_process_dir = os.path.join(images_dir, 'first_process')
second_process_dir = os.path.join(images_dir, 'second_process')

# Crear directorios si no existen
os.makedirs(first_process_dir, exist_ok=True)
os.makedirs(second_process_dir, exist_ok=True)

# Función para guardar una captura de pantalla con el nombre basado en la fecha, hora y mensaje
def save_screenshot(process_name, message):
    current_time = datetime.datetime.now().strftime("%S_%H_%d_%m_%Y")  # Segundos, Hora, Día, Mes, Año
    sanitized_message = "".join(c for c in message if c.isalnum())  # Limpiar el mensaje para que sea válido en el nombre del archivo
    filename = f"{current_time}_{sanitized_message}.png"
    
    if process_name == 'first_process':
        save_path = os.path.join(first_process_dir, filename)
    elif process_name == 'second_process':
        save_path = os.path.join(second_process_dir, filename)
    
    # Tomar captura de pantalla y guardarla
    pyautogui.screenshot(save_path)
    print(f"Screenshot saved: {save_path}")


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
                pyautogui.click(1191, 689)
                pyautogui.click(1191, 689)
                print("Located and clicked on 'IrBinance.png'")
                pyautogui.write(message)
                print("Pasted message text")
                await asyncio.sleep(0.1)
                

                if await search_and_click(image_paths['claim_now']):
                    print("Claim Now clicked")

                    # Replacing the click on 'open' with a click on coordinates (952, 714) and pressing F5
                    await asyncio.sleep(1)
                    pyautogui.click(952, 584)
                    pyautogui.click(952, 604)
                    pyautogui.click(952, 654)
                    pyautogui.click(952, 714)
                    print(Fore.YELLOW + "Clicked on coordinates (952, 714)")
                    pyautogui.click(952, 750)
                    await asyncio.sleep(1.5)
                    
                    #recara la pagina , antes de empezar con la segunda pagina
                    pyautogui.press('f5')
                    print(Fore.GREEN + "Pressed F5 to refresh")
                    pyautogui.hotkey('alt', 'tab')
                    await asyncio.sleep(2)
                    print(f"First process finished in {time.time() - start_time} seconds")
                    
                    
                    # Inicia el segundo proceso
                    second_process_start = time.time()
                    print('Starting SECOND PROCCES')
                    # Click through the Binance UI to claim the cryptobox vibladi
                    pyautogui.click(1191, 689)
                    pyautogui.click(1191, 689)
                    print("Located and clicked on 'IrBinance.png'")
                    pyautogui.write(message)
                    print("Pasted message text")
                    await asyncio.sleep(0.1)
                            
                    if await search_and_click(image_paths['claim_now']):
                        print("Claim Now clicked")
                        # Replacing the click on 'open' with a click on coordinates (952, 714) and pressing F5
                        await asyncio.sleep(1)
                        pyautogui.click(952, 584)
                        pyautogui.click(952, 604)
                        pyautogui.click(952, 654)
                        pyautogui.click(952, 714)
                        print(Fore.YELLOW + "Clicked on coordinates (952, 714)")
                        pyautogui.click(952, 750)
                        await asyncio.sleep(1.5)
                        
                        #recarga la pagina antes de volver a la primera pagina
                        pyautogui.press('f5')
                        print(Fore.GREEN + "Pressed F5 to refresh")
                        pyautogui.hotkey('alt', 'tab')
                        await asyncio.sleep(2)
                        
                        print(f"Second process finished in {time.time() - second_process_start} seconds")
                    
                    
                    
                else:
                    print(Fore.RED + "Claim Now not found, attempting to reload.")
                    pyautogui.press('f5')
                        
                            
                            

            except Exception as e:
                pyautogui.press('f5')
                error_traceback = traceback.format_exc()
                print(Fore.RED + f"Unexpected error: {e}")
                print(Fore.RED + f"Error traceback:\n{error_traceback}")

        await asyncio.sleep(0.1)

async def main():
    await client.start()
    await asyncio.gather(
        process_messages(),
        client.run_until_disconnected()
    )

if __name__ == "__main__":
    asyncio.run(main())
