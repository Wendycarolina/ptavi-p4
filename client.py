#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Programa cliente que abre un socket a un servidor
"""

import socket
import sys

# Cliente UDP simple.

# Dirección IP del servidor.
SERVER = sys.argv[1]
PORT = int(sys.argv[2])
if PORT < 1024:
    sys.exit('ERROR: PUERTO NO VÁLIDO')

# Contenido que vamos a enviar
Linea = sys.argv[3:]
LINE = ' '.join(Linea)



# Creamos el socket, lo configuramos y lo atamos a un servidor/puerto
my_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
my_socket.connect((SERVER, PORT))

print("Enviando: " + LINE)
my_socket.send(bytes(LINE, 'utf-8') + b'\r\n')
data = my_socket.recv(1024)
if Linea[0] == 'REGISTER':
    my_socket.send(b'REGISTER sip: ' + bytes(Linea[0],'utf-8') + b'SIP/2.0\r\n\r\n')
   


print('Recibido -- ', data.decode('utf-8'))
print("Terminando socket...")

# Cerramos todo
my_socket.close()
print("Fin.")
