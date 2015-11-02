#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Clase (y programa principal) para un servidor de eco en UDP simple
"""

import socketserver
import sys
import time
import json

class SIPRegisterHandler(socketserver.DatagramRequestHandler):
    """
    Echo server class
    """
    dicc = {}
    def register2json(self):
        fich = json.dumps(self.dicc)
        with open('register.json', 'w') as fich:
            json.dump(self.dicc, fich, sort_keys=True, indent=4)

    def handle(self):
        # Escribe dirección y puerto del cliente (de tupla client_address)
        self.wfile.write(b"Hemos recibido tu peticion ")
        print('IP: ' + self.client_address[0])
        print('Port: ' + str(self.client_address[1]))
        while 1:
            # Leyendo línea a línea lo que nos envía el cliente
            line = self.rfile.read()
            
            if len(line.split()) >= 2:
              
                if line.split()[0] == 'REGISTER':
                    self.dicc[line[2]] = self.client_address[0]
                    self.register2json()
                    Time = line.split()[5]
                    if  Time == '0':
                        del self.dicc[line[2]]
                        self.register2json()
                        self.wfile.write(b'SIP/2.0 200 OK\r\n\r\n')
                elif line.split()[0] != 'REGISTER':
                    print("El cliente nos manda " + line.decode('utf-8'))

            
            # Si no hay más líneas salimos del bucle infinito
            if not line:
                break

if __name__ == "__main__":
    # Creamos servidor de eco y escuchamos
    PORT = int(sys.argv[1])
    serv = socketserver.UDPServer(('',PORT), SIPRegisterHandler)
    print("Lanzando servidor UDP de eco...")
    serv.serve_forever()
