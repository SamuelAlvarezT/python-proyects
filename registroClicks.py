from pynput import mouse

def on_click(x, y, button, pressed):
    if pressed:
        print(f"Click at ({x}, {y})")

# Crear un listener para los eventos del mouse
with mouse.Listener(on_click=on_click) as listener:
    listener.join()

