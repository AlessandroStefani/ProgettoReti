
import socket as sk
import time
import threading

FREE=True
OCCUPIED=False

drone1_status=FREE
drone2_status=FREE
drone3_status=FREE

droneSide_ip = "192.168.1.254"
clientSide_ip = "10.10.10.254"
client_ip = "10.10.10.1"
drone1_ip = "192.168.1.1"
drone2_ip = "192.168.1.2"
drone3_ip = "192.168.1.3"

drones={10100:"drone1", 10200:"drone2", 10300:"drone3"}
ports={drone1_ip:10100, drone2_ip:10200, drone3_ip:10300}

#controlla che il drone specificato sia libero
def isDroneFree(drone_ip):
    match drone_ip:
        case "192.168.1.1":
            return drone1_status
        case "192.168.1.2":
            return drone2_status
        case "192.168.1.3":
            return drone3_status
        case _:
            return False

#cambia lo stato del drone specficato
def changeDroneStatus(drone):
    match drone:
        case "drone1":
            global drone1_status
            drone1_status = not drone1_status
        case "drone2":
            global drone2_status
            drone2_status = not drone2_status
        case "drone3":
            global drone3_status
            drone3_status = not drone3_status
        case _:
            return 0

#contatta e attende la risposta del drone 
def contactDrone(port, delivery_addr):
    drone=drones[port]
    udp_sock=sk.socket(sk.AF_INET,sk.SOCK_DGRAM)
    drone_addr=("localhost",port)
    data=droneSide_ip+"||"+delivery_addr
    print("\n\r sending request to "+drone)
    try:
        changeDroneStatus(drone)
        udp_sock.sendto(data.encode(), drone_addr)
        print("\n\r waiting "+drone+" response...")
        reply, addr = udp_sock.recvfrom(1024)
        print(reply.decode())
        connectionSocket.send(reply)
        changeDroneStatus(drone)
    except Exception as info:
        changeDroneStatus(drone)
        print(info)
        connectionSocket.send(("\n\r "+drone+" is offline").encode())


#creazione socket per ricevere il client
while True:
    rcv_client = sk.socket(sk.AF_INET, sk.SOCK_STREAM)
    rcv_client_address=("localhost",8000)
    rcv_client.bind(rcv_client_address)

    rcv_client.listen(1)

    print("\n\r waiting for operator to connect...")
    connectionSocket, addr = rcv_client.accept()
    print("\n\r operator "+client_ip+" connected!")

    #si attende l'ordine originato dal client, una volta ricevuto si controlla che il drone richiesto sia libero.
    #Se è libero si procede ad inoltrare la richiesta al drone su un nuovo thread, così da poter gestire altre richieste.
    #Se non è libero si invia al client un messaggo indicando lo stato del drone.
    while True:

        print("\n\r waiting delivery order...")
        
        try:
            order = connectionSocket.recv(1024)
        except Exception as e:
            print(e)
            time.sleep(2)
            break

        order = order.decode("utf-8")
        print("\n\r order: "+order)
        drone_ip = order.split("->")[0]
        delivery_addr = order.split("->")[1]
        if isDroneFree(drone_ip) == True:
            t = threading.Thread(None, contactDrone, None,(ports[drone_ip],delivery_addr,), None)
            t.start()
        else:
            print("\n\r order dismissed: drone occupied")
            order_refusal="drone "+drone_ip+" is occupied"
            connectionSocket.send(order_refusal.encode())
       