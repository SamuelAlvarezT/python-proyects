from telethon import TelegramClient, events
import pyautogui
import pyscreeze
import asyncio
import queue
import json
from colorama import Fore
import datetime

# 'tu_api_id' y 'tu_api_hash'
api_id = '28089555'
api_hash = '1ebe2cac78e82f0bbcb3cb78f6248229'

# Lista para almacenar los mensajes filtrados
mensajes_filtrados = []

# Inicia el cliente de Telegram
client = TelegramClient('54Intento', api_id, api_hash)

# Crea una cola y un set para almacenar los mensajes
cola_de_mensajes = queue.Queue()
mensajes_set = set()

# Ruta del archivo JSON para almacenar los mensajes
json_file_path = 'data/mensajes.json'
# Verifica si el archivo JSON ya existe
try:
    with open(json_file_path, 'r') as file:
        mensajes_filtrados = json.load(file)
except FileNotFoundError:
    # Si el archivo no existe, inicializa mensajes_filtrados como una lista vacía
    mensajes_filtrados = []

@client.on(events.NewMessage(chats=['@Crypto_Box_Code_Binance', '@UnlimitedBinanceBoxes', 'KingBX', 'Token_Boxes']))
async def nuevo_mensaje(event):
    mensaje = event.message.message
    # Obtiene la hora de recepción del mensaje
    hora_recepcion = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # Obtiene el remitente del mensaje
    remitente = event.sender.username if event.sender and event.sender.username else event.sender.first_name if event.sender else 'Desconocido'

    num_caracteres = len(mensaje)
    if num_caracteres != 8 or mensaje in mensajes_filtrados or '/' in mensaje or ' ' in mensaje:
        return

    mensaje_info = {
        "mensaje": mensaje,
        "hora_recepcion": hora_recepcion,
        "remitente": remitente
    }

    cola_de_mensajes.put(mensaje_info)
    mensajes_set.add(mensaje)
    mensajes_filtrados.append(mensaje_info)

    with open(json_file_path, 'w') as file:
        json.dump(mensajes_filtrados, file)

    print(Fore.GREEN + f'Mensaje aprobado: {mensaje}')

    mensaje_monoespaciado = f"`\n{mensaje}\n`"

    try:
        await client.send_message('@CryptotribuTeam', mensaje_monoespaciado, parse_mode='markdown')
    except ChatWriteForbiddenError:
        print("You don't have permission to write in this chat.")
    except Exception as e:
        print(f"Unexpected error: {e}")

    await asyncio.sleep(0.1)

async def procesar_mensajes():
    while True:
        if not cola_de_mensajes.empty():
            mensaje_info = cola_de_mensajes.get()
            mensaje = mensaje_info["mensaje"]

            try:
                print('Arrancando')
                x, y = pyscreeze.locateCenterOnScreen('images/IrBinance.png')
                pyautogui.click(x, y)
                print("UBICADO EN BINANCE")
                pyautogui.click('images/PasteBinance.png')
                pyautogui.write(mensaje)
                print("Texto pegado de portapapeles")

                try:
                    x, y = pyscreeze.locateCenterOnScreen('images/ClaimNow.png')
                    pyautogui.click(x, y)
                except pyscreeze.ImageNotFoundException:
                    x, y = pyscreeze.locateCenterOnScreen('images/CapturaRecargar.png')
                    pyautogui.click(x, y)

                for _ in range(3):
                    try:
                        pyautogui.click('images/Open.png')
                        print("Crytptobox abierta")
                        break
                    except pyscreeze.ImageNotFoundException:
                        print("Imagen 'AbrirCaja.png' no encontrada. Intentando de nuevo.")
                        x, y = pyscreeze.locateCenterOnScreen('images/CapturaRecargar.png')
                        pyautogui.click(x, y)
                        print("Imagen 'AbrirCaja.png' no encontrada. Intentando de nuevo.")
                        x, y = pyscreeze.locateCenterOnScreen('images/ClosePacketDetails.png')
                        pyautogui.click(x, y)
            except pyscreeze.ImageNotFoundException:
                print(Fore.RED + "Imagen no encontrada, finalizando.")
            except Exception as e:
                print(Fore.RED + f"Error inesperado: {e}")
        
        await asyncio.sleep(0.1)

# Inicia el cliente y el procesador de mensajes
with client:
    loop = asyncio.get_event_loop()
    loop.create_task(procesar_mensajes())
    client.run_until_disconnected()
