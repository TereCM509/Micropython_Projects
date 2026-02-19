import machine # Para controlar el hardware (pines, leds)
import network # Para manejar el WiFi
import socket  # Para crear el servidor web
import time    # Para pausas (sleep)

# --- 1. CONFIGURACIÓN DEL HARDWARE ---
on = False  # Variable lógica para saber el estado del LED (memoria)
led = machine.Pin(4, machine.Pin.OUT) # Definimos el pin 4 como salida
led.value(0) # Empezamos con el LED apagado

# --- 2. CONFIGURACIÓN DE LA RED WIFI ---
sta_if = network.WLAN(network.WLAN.IF_STA) # Modo 'Estación' (se conecta a un router)

# Reinicio preventivo de la interfaz WiFi para evitar errores previos
sta_if.active(False)
time.sleep(0.5) 
sta_if.active(True)

# Intentamos conectar
if not sta_if.isconnected():
    print('Conectando a la red...')
    # Identificador del internet y contrasena
    sta_if.connect('TeresaWifi', '150V4k9T') 
    
    intentos = 0
    # Esperamos hasta conectar o hasta que pasen 50 segundos
    while not sta_if.isconnected() and intentos < 50:
        print("Esperando conexión...")
        time.sleep(1)
        intentos += 1

# Verificación final de conexión
if sta_if.isconnected():
    # ifconfig() nos da la IP asignada (ej: 192.168.1.50)
    print('¡Conectado! Datos de red:', sta_if.ifconfig())
    ip = sta_if.ifconfig()[0] # Guardamos la dirección IP
else:
    print('No se pudo conectar. Revisa la contraseña.')
    ip = '0.0.0.0' # Evita que el código falle abajo si no hay IP

# --- 3. CREACIÓN DEL SERVIDOR (SOCKET) ---
# AF_INET = Protocolo de Internet (IP)
# SOCK_STREAM = Protocolo TCP (fiable)
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# "bind" asocia el socket a tu IP y al puerto 80 (estándar web)
server_socket.bind((ip, 80)) 
server_socket.listen(5) # Escucha hasta 5 conexiones simultáneas
print(f"Servidor escuchando en: http://{ip}")

# --- 4. CICLO PRINCIPAL 
while True:
    try:
        # Aceptamos una conexión entrante (navegador del celular/PC)
        conn, addr = server_socket.accept()
        print("Cliente conectado desde:", addr)
        
        # Recibimos la petición (lo que el navegador pide)
        request = conn.recv(1024) 
        
        # --- PARSEO (ANÁLISIS) DE LA PETICIÓN ---
        # Convertimos los bytes a string y buscamos qué pide el navegador.
        # Una petición se ve así: "GET /led HTTP/1.1..."
        # El split corta el texto para quedarnos solo con "/led" o "/"
        request_str = str(request).split("GET /")[1].split(" ")[0]
        print("Recurso solicitado:", request_str)
        
        # CASO A: El usuario entra a la página principal (IP sola)
        if request_str == "":
            # Creamos el HTML con JavaScript incrustado
            response = """HTTP/1.1 200 OK
Content-Type: text/html

<!DOCTYPE html>
<html>
<head>
    <title>ESP32 Teresa Server</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        /* Un poco de estilo para que el botón se vea bien */
        body { font-family: Arial; text-align: center; margin-top: 50px; }
        button { font-size: 20px; padding: 20px; border-radius: 10px; color: white; background-color: red; }
    </style>
</head>
<body>
    <h1>Control LED ESP32</h1>
    
    <button id="boton" onclick="turnonoff()">OFF</button>

    <script>
    // --- LÓGICA JAVASCRIPT (Corre en el navegador) ---
    function turnonoff() {
        var r = new XMLHttpRequest();
        r.open("GET", "led", true); // Pide la ruta /led al ESP32
        
        r.onload = function() {
            console.log("Respuesta del ESP32:", r.responseText);
            // Si el ESP32 dice que prendió...
            if(r.responseText.includes("ON")) {
                document.getElementById("boton").innerHTML = "ENCENDIDO";
                document.getElementById("boton").style.backgroundColor = "green";
            }
            // Si el ESP32 dice que apagó...
            else if(r.responseText.includes("OFF")) {
                document.getElementById("boton").innerHTML = "APAGADO";
                document.getElementById("boton").style.backgroundColor = "red";
            }
        };
        r.send(); // Envía la petición
    }
    </script>
</body>
</html>
"""
            conn.send(response.encode()) # Enviamos el HTML al navegador
            conn.close() # Cerramos conexión (muy importante en HTTP)

        # CASO B: El JavaScript pide cambiar el LED (ruta "led")
        elif "led" in request_str:
            print("Solicitud de cambio de LED recibida")
            
            # Invertimos el estado
            if on:
                led.value(0) # Apagar físico
                on = False   # Actualizar variable
                resp_data = "OFF"
            else:
                led.value(1) # Prender físico
                on = True    # Actualizar variable
                resp_data = "ON"
            
            # Respondemos solo con texto plano (no HTML completo)
            response = "HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\n\r\n" + resp_data
            conn.send(response.encode())
            conn.close()

    except Exception as e:
        print("Error en el bucle:", e)
        # Si algo falla, intenta cerrar la conexión para no bloquear el ESP32
        try: conn.close()
        except: pass
    