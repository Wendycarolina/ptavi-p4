#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Clase (y programa principal) para un servidor de eco en UDP simple
"""

import socketserver
import sys
import time
import json
import os.path

class SIPRegisterHandler(socketserver.DatagramRequestHandler):
    """
    Echo server class
    """
    dicc = {}
    def register2json(self):
        fich = json.dumps(self.dicc)
        with open('registered.json', 'w') as fich:
            json.dump(self.dicc, fich, sort_keys=True, indent=4)

    def json2registered(self):
        if os.path.exists('registered.json'):
            self.dicc = json.loads(open('registered.json').read())
        else:
            self.dicc = {}

    def handle(self):
        # Escribe dirección y puerto del cliente (de tupla client_address)
        self.json2registered()
        print('IP: ' + self.client_address[0])
        print('Port: ' + str(self.client_address[1]))
        while 1:
            # Leyendo línea a línea lo que nos envía el cliente
            line = self.rfile.read()
            linea = line.decode('utf-8')
            #print(linea)
            if len(linea.split()) >= 2:
                if linea.split()[0] == 'REGISTER':
                    #Creo y guardo datos usuario
                    Usuario = linea.split()[2]
                    IP = self.client_address[0]
                    Expires = float(linea.split(':')[-1])
                    Time = time.time()
                    Time_expire = Time + Expires 
                    Time_user = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(Time_expire))
                    Datos_User = [IP, Time_user]
                    #Compruebo si el usuario se ha expiradoo se da de baja
                    for Usuario in self.dicc:
                        Time = time.time()
                        if Time >= Time_expire or Expires == 0:
                            del self.dicc[Usuario]
                        else:
                            self.dicc[Usuario] = Datos_User
                    self.register2json()
                    self.wfile.write(b'SIP/2.0 200 OK\r\n\r\n')
                elif line.split()[0] != 'REGISTER':
                    print("El cliente nos manda " + linea)
            
            # Si no hay más líneas salimos del bucle infinito
            if not line:
                break

    
if __name__ == "__main__":
    # Creamos servidor de eco y escuchamos
    PORT = int(sys.argv[1])
    serv = socketserver.UDPServer(('',PORT), SIPRegisterHandler)
    print("Lanzando servidor UDP de eco...")
    serv.serve_forever()
