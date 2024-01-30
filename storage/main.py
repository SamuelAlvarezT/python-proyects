from telethon import TelegramClient, events
import pyautogui
import pyscreeze
import asyncio
import queue

# 'tu_api_id' y 'tu_api_hash'
api_id = '28089555'
api_hash = '1ebe2cac78e82f0bbcb3cb78f6248229'

# Lista para almacenar los mensajes filtrados
mensajes_filtrados = []

# Crea una cola para almacenar los mensajes
cola_de_mensajes = queue.Queue()

#Inicia el cliente de Telegram
client = TelegramClient('24Intento', api_id, api_hash)

@client.on(events.NewMessage(chats=['@Crypto_Box_Code_Binance']))
async def nuevo_mensaje(event):
    # This code will run each time a new message arrives in the group
    mensaje = event.message.message
    print(f'Mensaje recibido: {mensaje}')
    # Filtra los mensajes basándote en la cantidad de caracteres y si ya ha sido procesado
    num_caracteres = len(mensaje)
    if num_caracteres > 8:  # Cambia este número a la cantidad de caracteres que desees
        print('El mensaje es demasiado largo, ignorándolo...')
        return
    elif num_caracteres < 8:  # Asegura que el mensaje tenga al menos 8 caracteres
        print('El mensaje es demasiado corto, ignorándolo...')
        return
    elif mensaje in mensajes_filtrados:
        print('El mensaje ya ha sido procesado, ignorándolo.')
        return
    # Si el mensaje pasa los filtros, añádelo a la cola
    cola_de_mensajes.put(mensaje)
    await asyncio.sleep(1)
    print('finalizando...')
    

async def procesar_mensajes():
    while True:
        if not cola_de_mensajes.empty():
            mensaje = cola_de_mensajes.get()
            print('Arrancando')
            x, y = pyscreeze.locateCenterOnScreen('storage/IrBinance.png')
            pyautogui.click(x, y)
            print("UBICADO EN BINANCE")
            pyautogui.click('storage/NewPaste.png')
            pyautogui.write (mensaje)
            print("Texto pegado de protapales")

            try:
                x, y = pyscreeze.locateCenterOnScreen('storage/ClaimNow.png')
                pyautogui.click(x, y)
            except pyscreeze.ImageNotFoundException:
                x, y = pyscreeze.locateCenterOnScreen('storage/CapturaRecargar.png')
                pyautogui.click(x, y)

            for _ in range(3):  # Intenta hacer clic tres veces en 'AbrirCaja.png'
                try:
                    pyautogui.click('storage/Open.png')
                    print("crytptobox abierta")  # Sale del bucle si el clic es exitoso
                except pyscreeze.ImageNotFoundException:
                    print("Imagen 'AbrirCaja.png' no encontrada. Intentando de nuevo.")
                    x, y = pyscreeze.locateCenterOnScreen('storage/CapturaRecargar.png')
                    pyautogui.click(x, y)
                    print("Imagen 'AbrirCaja.png' no encontrada. Intentando de nuevo.")
                    x, y = pyscreeze.locateCenterOnScreen('storage/ClosePacketDetails.png')
                    pyautogui.click(x, y)    
        await asyncio.sleep(1)    
        print('finalizando...')

# Inicia el cliente y el procesador de mensajes
with client:
    loop = asyncio.get_event_loop()
    loop.create_task(procesar_mensajes())
    client.run_until_disconnected()
