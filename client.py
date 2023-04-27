import socket
import random
from threading import Thread
from datetime import datetime
from colorama import Fore, init, Back 
import rsa


with open("/home/munch/Projects/David/Messnger/Messenger-/publickey.pem", 'rb') as filekey: 
    publickey = rsa.PublicKey.load_pkcs1(filekey.read())
with open("/home/munch/Projects/David/Messnger/Messenger-/privatekey.pem", 'rb') as filekey: 
    privatekey = rsa.PrivateKey.load_pkcs1(filekey.read())

init()

colors = [Fore.BLUE, Fore.CYAN, Fore.GREEN, Fore.LIGHTBLACK_EX, 
    Fore.LIGHTBLUE_EX, Fore.LIGHTCYAN_EX, Fore.LIGHTGREEN_EX, 
    Fore.LIGHTMAGENTA_EX, Fore.LIGHTRED_EX, Fore.LIGHTWHITE_EX, 
    Fore.LIGHTYELLOW_EX, Fore.MAGENTA, Fore.RED, Fore.WHITE, Fore.YELLOW
]

client_color = random.choice(colors)

SERVER_HOST = "127.0.0.1"
SERVER_PORT = 5002 
separator_token = "<SEP>" 


s = socket.socket()
print(f"[*] Connecting to {SERVER_HOST}:{SERVER_PORT}...")

s.connect((SERVER_HOST, SERVER_PORT))
print("[+] Connected.")

name = input('What is your name: ') 

def listen_for_messages():
    while True:
        message = s.recv(1024)
        message = rsa.decrypt(message, privatekey).decode('cp1252') 
        message = message.replace(separator_token, ': ')
        print("\n" + message)

t = Thread(target=listen_for_messages, daemon=True).start()

while True:
    to_send =  input()
    if to_send.lower() == 'q':
        break
    
    date_now = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
    to_send = f"{client_color}[{date_now}] {name}{separator_token}{to_send}{Fore.RESET}"
    to_send = rsa.encrypt(bytes(to_send, 'cp1252'), publickey)
    s.send(to_send)

s.close()
