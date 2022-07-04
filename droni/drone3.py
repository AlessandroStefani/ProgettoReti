
import socket as sk
import time
from random import randint

drone3_ip = "192.168.1.3"
gateway_ip = "192.168.1.254"

#creazione del sochet per ricevere le richieste
sock = sk.socket(sk.AF_INET, sk.SOCK_DGRAM)
drone3_address=("localhost", 10300)    
print ("\n\r drone3 starting up on "+drone3_ip+" port 10300")
sock.bind(drone3_address)

#una volta ricevuto l'ordine si attende un tempo a scelta e si invia la risposta di avvenuta consegna
while True:
    print("\n\r drone3 waiting for delivery order ...")
    data,address = sock.recvfrom(1024)

    data=data.decode()

    sender=data.split("||")[0]
    delivery_addr=data.split("||")[1]

    print("\n\r order received from gateway ["+sender+"]")

    print ("\n\r delivering package to: " + delivery_addr + " ...")
    time.sleep(randint(10,15))
    print("\n\r delivery complete!")
    reply = "drone3: FREE"
    sock.sendto(reply.encode(),address)
