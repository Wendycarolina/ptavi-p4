#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Clase (y programa principal) para un servidor de eco en UDP simple
"""

import socketserver
import sys

class SIPRegisterHandler(socketserver.DatagramRequestHandler):
    """
    Echo server class
    """
    dicc = {} #Atributo de clase
    def handle(self):
        # Escribe dirección y puerto del cliente (de tupla client_address)
        self.wfile.write(b"Hemos recibido tu peticion ")
        print('IP: ' + self.client_address[0])
        print('Port: ' + str(self.client_address[1]))
        Lista = []
        while 1:
            # Leyendo línea a línea lo que nos envía el cliente
            line = self.rfile.read()
            metodo = line.decode('utf-8')
            if len(metodo.split()) >= 2:
                if metodo.split()[0] == 'REGISTER':
                    address_1 = metodo.split()[1].endswith('.com')
                    address_2 = metodo.split()[1].endswith('.es')
                    if  address_1 or address_2:
                        value_a = metodo.split()[1]
                        value_b = self.client_address[0]
                        dicc = {'Address': value_a ,'IP': value_b}
                        Lista.append(dicc)
                        print(Lista) 
                        print(dicc)
                        self.wfile.write(b'SIP/2.0 200 OK\r\n\r\n')   
                elif metodo.split()[0] == 'Expire':
                        value_a = metodo.split()[1]
                        
                    
                elif metodo.split()[0] != 'REGISTER':
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
