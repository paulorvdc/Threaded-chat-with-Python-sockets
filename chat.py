#Autores: Paulo Ricardo V. do Carmo e Renan Mattos Nutse

import socket
import sys
import threading


def readSocketAndOutput(s):
    global byeFlag
    print("Digite 'temais' para sair")
    n = s.recv(100).decode() #decode dos bytes da String
    while True:
        if byeFlag:
            try:
                str = s.recv(100).decode()
                print('\033[92m' + "\r>>> " + n + ": " + str + "\n<<<", end="", flush=True)
            except:
                print("Conexão fechada")
                break

            if str == "temais":
                byeFlag = 0
                break

    print("Usuario remoto desconectado!!!")
    s.close()
    sys.exit()


def readSTDINandWriteSocket(s, n):
    global byeFlag
    s.send(n.encode())
    while True:
        if byeFlag:
            str = input("<<< ")
            s.send(str.encode()) #Envio da String com decode em bytes
            if str == "temais":
                print('\033[91m' + "Sinal de fim de chat enviado!!!")
                s.send(str.encode())
                byeFlag = 0
                s.close()
                sys.exit()


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #Declara socket
byeFlag = 1
ch = input('\033[94m' + "Conectar[1] com peer ou esperar[2] por conexao. Digite a escolha: ")

if ch == "1":
    host = input("Digite IP do peer:")
    nick = input("Digite seu nick: ")
    port = 2222
    s.connect((host, port)) #Socket conecta ao outro
    threading.Thread(target=readSocketAndOutput, args=(s,)).start()
    threading.Thread(target=readSTDINandWriteSocket, args=(s, nick)).start()

elif ch == "2":
    nick = input("Digite seu nick: ")
    host = ''
    port = 2222
    s.bind((host, port))
    s.listen(2)  #Socket espera conexão           
    print("Esperando conexão...")
    while True:
        c, addr = s.accept()     
        threading.Thread(target=readSocketAndOutput, args=(c, )).start()
        threading.Thread(target=readSTDINandWriteSocket, args=(c, nick)).start()

else:
    print("Incorrect choice")
    sys.exit()
