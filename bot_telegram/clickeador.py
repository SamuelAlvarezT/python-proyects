import os
import webbrowser
from bs4 import BeautifulSoup
from time import sleep

# Registrar el navegador Vivaldi
vivaldi_path = "C:\\Program Files\\Vivaldi\\Application\\vivaldi.exe"  # Actualiza la ruta si es necesario
if os.path.exists(vivaldi_path):
    webbrowser.register('vivaldi', None, webbrowser.BackgroundBrowser(vivaldi_path))
else:
    raise FileNotFoundError(f"No se encontró Vivaldi en la ruta especificada: {vivaldi_path}")

# Ruta de la carpeta de archivos HTML
ruta_archivos = os.path.join("bot_telegram", "formularios_enlaces")

def abrir_enlaces_no_clickeados(archivo_html, max_enlaces=100):
    # Leer y analizar el archivo HTML
    with open(archivo_html, "r", encoding="utf-8") as file:
        soup = BeautifulSoup(file, "html.parser")
    
    # Encontrar todos los enlaces no clickeados (no tienen estilo de color rojo)
    enlaces_no_clickeados = [
        enlace for enlace in soup.find_all("a", href=True)
        if enlace.get("style") != "color:red;"
    ]
    
    # Limitar a los primeros `max_enlaces` no clickeados
    enlaces_para_abrir = enlaces_no_clickeados[:max_enlaces]
    
    if enlaces_para_abrir:
        # Abrir cada enlace en una pestaña del navegador Vivaldi y marcarlo como clickeado
        for enlace in enlaces_para_abrir:
            url = enlace["href"]
            print(f"Abriendo enlace: {url}")
            webbrowser.get("vivaldi").open_new_tab(url)
            
            # Marcar el enlace como clickeado cambiando su color a rojo
            enlace["style"] = "color:red;"
            
            # Pausa entre aperturas para evitar sobrecargar el navegador
            sleep(1)  # Ajusta el tiempo según sea necesario
        
        # Guardar los cambios en el archivo HTML
        with open(archivo_html, "w", encoding="utf-8") as file:
            file.write(str(soup))
        
        print(f"{len(enlaces_para_abrir)} enlaces abiertos y marcados como clickeados en '{archivo_html}'")
        return True
    return False

# Procesar archivos HTML en la carpeta, deteniéndose después de abrir 100 enlaces
if os.path.exists(ruta_archivos):
    archivos_html = sorted([f for f in os.listdir(ruta_archivos) if f.endswith(".html")])
    
    for archivo in archivos_html:
        archivo_path = os.path.join(ruta_archivos, archivo)
        
        # Si se abrieron 100 enlaces, finalizar el programa
        if abrir_enlaces_no_clickeados(archivo_path):
            break
else:
    print(f"La carpeta '{ruta_archivos}' no existe. Verifica la ruta.")

print("Proceso de apertura de enlaces completado.")
