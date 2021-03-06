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
        """
        Registra o da de baja aun usuario
        """
        fich = json.dumps(self.dicc)
        with open('registered.json', 'w') as fich:
            json.dump(self.dicc, fich, sort_keys=True, indent=4)

    def json2registered(self):
        """
        Comprueba si existe un archivo
        """
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
            if len(linea.split()) >= 2:
                if linea.split()[0] == 'REGISTER':
                    #Creo y guardo datos usuario
                    Usuario = linea.split()[2]
                    IP = self.client_address[0]
                    Expires = float(linea.split(':')[-1])
                    Time = time.time()
                    Time_exp = Time + Expires
                    fecha = '%Y-%m-%d %H:%M:%S'
                    Time_user = time.strftime(fecha, time.gmtime(Time_exp))
                    Datos_User = [IP, Time_user]
                    self.dicc[Usuario] = Datos_User
                    #Compruebo si el usuario se ha expiradoo se da de baja
                    if Expires == 0:
                        del self.dicc[Usuario]
                    for User in self.dicc:
                        Time = time.time()
                        if Time >= Time_exp:
                            if Usuario in self.dicc:
                                del self.dicc[Usuario]
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
    serv = socketserver.UDPServer(('', PORT), SIPRegisterHandler)
    print("Lanzando servidor UDP de eco...")
    serv.serve_forever()
