import os
from bs4 import BeautifulSoup

# Definir la ruta de los archivos HTML
ruta_archivos = os.path.join("bot_telegram", "formularios_enlaces")

def hacer_enlaces_clickeables(archivo_html):
    # Leer el archivo HTML
    with open(archivo_html, "r", encoding="utf-8") as file:
        soup = BeautifulSoup(file, "html.parser")
    
    # Buscar todos los enlaces que comienzan con "https://"
    enlaces = soup.find_all(string=lambda text: isinstance(text, str) and text.startswith("https://"))
    
    for enlace in enlaces:
        # Crear un nuevo elemento <a>
        nuevo_enlace = soup.new_tag("a", href=enlace, target="_blank")
        nuevo_enlace.string = enlace
        
        # Agregar un evento onclick para cambiar el color
        nuevo_enlace['onclick'] = "this.style.color='red';"
        
        # Reemplazar el texto original por el nuevo enlace
        enlace.replace_with(nuevo_enlace)
    
    # Agregar un script de JavaScript para cambiar el color del enlace
    script = soup.new_tag('script')
    script.string = """
    document.querySelectorAll('a').forEach(link => {
        link.addEventListener('click', function() {
            this.style.color = 'red';  // Cambiar el color del enlace a rojo
        });
    });
    """
    soup.head.append(script)  # Agregar el script en la sección <head> del HTML

    # Guardar el archivo HTML modificado
    with open(archivo_html, "w", encoding="utf-8") as file:
        file.write(str(soup))
    
    # Imprimir mensaje en consola al finalizar la modificación del archivo
    print(f"Archivo modificado: {archivo_html}")

# Procesar cada archivo HTML en la carpeta
if os.path.exists(ruta_archivos):
    archivos_html = sorted([f for f in os.listdir(ruta_archivos) if f.endswith(".html")])
    
    for archivo in archivos_html:
        archivo_path = os.path.join(ruta_archivos, archivo)
        hacer_enlaces_clickeables(archivo_path)
else:
    print(f"La carpeta '{ruta_archivos}' no existe. Verifica la ruta.")

print("Proceso de modificación de enlaces completado.")
