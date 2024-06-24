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

#Inicia el cliente de Telegram
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
    if num_caracteres > 8 or num_caracteres < 8 or mensaje in mensajes_filtrados or '/' in mensaje or ' ' in mensaje:
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

    try:
        await client.send_message('@CryptotribuTeam', mensaje)
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
                print("Texto pegado de protapales")

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
                print(Fore.RED + f"imagen no encontrada, finalizando ")
        
        await asyncio.sleep(0.1)


# Inicia el cliente y el procesador de mensajes
with client:
    loop = asyncio.get_event_loop()
    loop.create_task(procesar_mensajes())
    client.run_until_disconnected()
"""Para abordar el problema que estás experimentando en tu código, donde después de omitir un mensaje por un error inesperado no se ejecuta el procesamiento de nuevos mensajes, es importante revisar el manejo de excepciones en tu código. Aquí hay algunas posibles causas y soluciones:

Manejo de excepciones: Asegúrate de que estás manejando adecuadamente las excepciones dentro de tu bucle de procesamiento de mensajes. Si ocurre un error inesperado al procesar un mensaje, captura la excepción para evitar que detenga por completo el procesamiento de mensajes.

Reinicio del procesamiento: Después de manejar una excepción al procesar un mensaje, asegúrate de que tu código esté configurado para continuar con el procesamiento del siguiente mensaje en la cola, en lugar de detenerse por completo.

Revisar la lógica del bucle: Verifica que la lógica dentro del bucle de procesamiento de mensajes esté diseñada para continuar con el siguiente mensaje en la cola si ocurre un error al procesar un mensaje en particular.

Manejo de errores específicos: Considera capturar excepciones específicas que puedan ocurrir durante el procesamiento de mensajes y manejarlas de manera apropiada para que el bucle pueda continuar ejecutándose sin interrupciones.

Revisando y ajustando el manejo de excepciones en tu código, así como asegurándote de que esté diseñado para continuar con el procesamiento de mensajes después de enfrentar un error inesperado, debería ayudarte a corregir la situación donde no se ejecuta el procesamiento de nuevos mensajes después de omitir uno por un error."""