import serial
import serial.tools.list_ports
import json
from datetime import datetime
import ipywidgets as widgets
from IPython.display import display

# -------------------------
# Función para listar puertos
# -------------------------
def listar_puertos():
    puertos = serial.tools.list_ports.comports()
    return [p.device for p in puertos]

# -------------------------
# Widgets
# -------------------------
puertos_dropdown = widgets.Dropdown(
    options=listar_puertos(),
    description='Puerto:'
)

peso_input = widgets.FloatText(
    description='Peso (g):'
)

boton_conectar = widgets.Button(description="Conectar")
boton_guardar = widgets.Button(description="Guardar dato")

salida = widgets.Output()

display(puertos_dropdown, peso_input, boton_conectar, boton_guardar, salida)

# -------------------------
# Variables globales
# -------------------------
ser = None

# -------------------------
# Conectar serial
# -------------------------
def conectar(b):
    global ser
    with salida:
        salida.clear_output()
        try:
            ser = serial.Serial(puertos_dropdown.value, 115200, timeout=1)
            print(f"Conectado a {puertos_dropdown.value}")
        except Exception as e:
            print("Error:", e)

boton_conectar.on_click(conectar)

# -------------------------
# Guardar dato
# -------------------------
def guardar(b):
    global ser
    with salida:
        if ser is None:
            print("Primero conecta el puerto")
            return
        
        try:
            linea = ser.readline().decode().strip()
            
            if linea == "":
                print("No se recibió dato")
                return
            
            lectura = float(linea)
            peso = peso_input.value
            
            dato = {
                "Peso": peso,
                "lectura": lectura,
                "Hora": datetime.now().isoformat()
            }
            
            # Guardar en archivo
            with open("datos_celda.json", "a") as f:
                f.write(json.dumps(dato) + "\n")
            
            print("Guardado:", dato)
        
        except Exception as e:
            print("Error:", e)

boton_guardar.on_click(guardar)