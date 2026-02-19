import network
import socket
import time

sta_if = network.WLAN(network.WLAN.IF_STA)

# 1. Aseguramos que esté desactivado antes de empezar
sta_if.active(False)
time.sleep(0.5) # Pausa breve para que el chip respire

sta_if.active(True)

# 2. Intentamos conectar
if not sta_if.isconnected():
    print('Conectando a la red...')
    sta_if.connect('TeresaWifi', '150V4k9T')
    
    # Un bucle con timeout para no quedar atrapados
    intentos = 0
    while not sta_if.isconnected() and intentos < 50:
        print("Esperando...")
        time.sleep(1)
        intentos += 1

if sta_if.isconnected():
    print('¡Conectado!', sta_if.ifconfig())
else:
    print('No se pudo conectar.')

ip = sta_if.ifconfig()[0]

#Create a socket #banda a 2.4
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((ip, 80))  # Bind to port 80 (HTTP)
server_socket.listen(5)  # Listen for connections
   
while True:
    conn, addr = server_socket.accept()
    print("Client connected from:", addr)
    
    request = conn.recv(1024)  # Read request from client
    print("Request:", str(request).split("GET /")[1].split(" ")[0])
    # Create an HTML response
    response = """\
HTTP/1.1 200 OK
Content-Type: text/html

<!DOCTYPE html>
<html>
<head><title>ESP32 Web Server</title></head>
<body>
    <h1>Welcome to ESP32 Web Server!</h1>
    <p>Your ESP32 is running a simple web server.</p>
</body>
</html>
"""
    
    conn.send(response.encode())  # Send response
    conn.close()  # Close connection
    

