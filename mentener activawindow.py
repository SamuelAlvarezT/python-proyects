import pyautogui
import time

def click_centro_pantalla():
    # Obtener el tamaño de la pantalla
    ancho, alto = pyautogui.size()
    
    # Calcular el centro de la pantalla
    centro_x = ancho // 2
    centro_y = alto // 2
    
    # Hacer clic en el centro de la pantalla
    pyautogui.click(centro_x, centro_y)
    print("Clic en el centro de la pantalla realizado.")

# Ejecutar el clic cada 5 minutos (300 segundos)
while True:
    click_centro_pantalla()
    time.sleep(300)  # Espera 5 minutos
