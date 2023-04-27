import socket
import random
from threading import Thread
from datetime import datetime
from colorama import Fore, init, Back 
import rsa

with open("./publickey.pem", rb) as filekey: 
    publickey = rsa.PublicKey.load_pkcs1(filekey.read())
with open("./privatekey.pem", rb) as filekey: 
    privatekey = rsa.PrivateKey.load_pkcs1(filekey.read())
    

# init colors
init()

# set the available colors
colors = [Fore.BLUE, Fore.CYAN, Fore.GREEN, Fore.LIGHTBLACK_EX, 
    Fore.LIGHTBLUE_EX, Fore.LIGHTCYAN_EX, Fore.LIGHTGREEN_EX, 
    Fore.LIGHTMAGENTA_EX, Fore.LIGHTRED_EX, Fore.LIGHTWHITE_EX, 
    Fore.LIGHTYELLOW_EX, Fore.MAGENTA, Fore.RED, Fore.WHITE, Fore.YELLOW
]

# choose a random color for the client
client_color = random.choice(colors)

# server's IP address
# if the server is not on this machine, 
# put the private (network) IP address (e.g 192.168.1.2)
SERVER_HOST = "127.0.0.1"
SERVER_PORT = 5002 # server's port
separator_token = "<SEP>" # we will use this to separate the client name & message

# initialize TCP socket
s = socket.socket()
print(f"[*] Connecting to {SERVER_HOST}:{SERVER_PORT}...")
# connect to the server
s.connect((SERVER_HOST, SERVER_PORT))
print("[+] Connected.")

name = input('What is your name: ') 

def listen_for_messages():
    while True:
        message = s.recv(1024).decode() 
        message = rsa.decrypt(message, privatekey).decode('ascii') 
        print("\n" + message)

# make a thread that listens for messages to this client & print them
t = Thread(target=listen_for_messages, daemon=True).start()

while True:
    # input message we want to send to the server
    to_send =  input()
    # a way to exit the program
    if to_send.lower() == 'q':
        break
    # add the datetime, name & the color of the sender
    date_now = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
    to_send = f"{client_color}[{date_now}] {name}{separator_token}{to_send}{Fore.RESET}"
    # finally, send the message
    to_send = rsa.encrypt(str(to_send).encode('ascii'), publickey)
    s.send(to_send.encode())

# close the socket
s.close()
