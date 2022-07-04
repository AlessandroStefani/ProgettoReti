

import socket as sk
import sys
import time
import threading

client_ip = "10.10.10.1"
gateway_ip = "10.10.10.254"
gateway_port="8000"

drone1_ip = "192.168.1.1"
drone2_ip = "192.168.1.2"
drone3_ip = "192.168.1.3"

droneDict={"1":drone1_ip, "2":drone2_ip, "3":drone3_ip}

clientsocket = sk.socket(sk.AF_INET, sk.SOCK_STREAM)

#contatta e attende la risposta del gateway
def contactGateway(drone_ip, del_address):
    request = drone_ip + "->" + del_address
    print("\n\r sending request for drone [" + drone_ip + "] to gateway")
    try:
        clientsocket.send(request.encode())
        print("\n\r waiting gateway response...")
        response = clientsocket.recv(1024)
        print("\n\r "+response.decode())
    except Exception as e:
        print(e)

#si simula la connessione del client al gateway con ip indicato
ip=""
port=""
print("\n\r connnect to gateway: ip: "+gateway_ip+" port: %s" % gateway_port)
while ip != gateway_ip or port != gateway_port:
    ip=input("gateway ip: ")
    port=input("gateway port: ")
    if ip != gateway_ip or port != gateway_port:
        print("\n\r wrong input")

try:
    clientsocket.connect(("localhost", 8000))
    print("\n\r connected to gateway")
except Exception as e:
    print (Exception,":",e)
    print("\n\r can't connect to gateway")
    print("\n\r exiting in 5 seconds, restart and try again")
    time.sleep(5)
    sys.exit(0)

#si prepara la richiesta e la si invia usando un nuovo thread così da poter
#inviare nuove richieste ad altri droni
while True:
    delivery_addr=input("\n\r Enter delivery address: ")
    destination_ip = input("\n\r Enter the IP or the number of the drone to send the delivery address to:\n1. 192.168.1.1\n2. 192.168.1.2\n3. 192.168.1.3\n")

    if len(destination_ip) == 1:
        destination_ip=droneDict[destination_ip]

    if len(delivery_addr) == 0:
        print("\n\r invalid address")
    elif(destination_ip == drone1_ip or destination_ip == drone2_ip or destination_ip == drone3_ip):        
        t= threading.Thread(None, contactGateway, None, (destination_ip,delivery_addr,), None)
        t.start()
    else:
        print("\n\r Wrong input")

    time.sleep(1)
