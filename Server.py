from socket import *
from threading import *

clients = set()
nicknames = []

def clientThread(clientSocket, clientAddress,nickname):
    while True:

        try:
            message = clientSocket.recv(1024).decode("utf-8")
            # print(clientAddress[0] + ":" + str(clientAddress[1]) +" says: "+ message)
            print(f"{nickname} : {message}")
            if ":signal number" in message:
                print("yes")
                for client in clients:
                    if client is not clientSocket:
                        client.send((f'{nickname}:'+message).encode("utf-8"))
            else:
                for client in clients:
                    if client is not clientSocket:
                        # client.send((clientAddress[0] + ":" + str(clientAddress[1]) +" says: "+ message).encode("utf-8"))
                        client.send((f"{nickname} : " + message).encode("utf-8"))

            if not message:
                clients.remove(clientSocket)
                print(clientAddress[0] + ":" + str(clientAddress[1]) +" disconnected")
                break
        except ConnectionResetError:
            pass

    clientSocket.close()

hostSocket = socket(AF_INET, SOCK_STREAM)
hostSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR,1)

hostIp = "127.0.0.1"
portNumber = 7500
hostSocket.bind((hostIp, portNumber))
hostSocket.listen()
print ("Waiting for connection...")



if __name__=='__main__':
    while True:
        clientSocket, clientAddress = hostSocket.accept()
        clients.add(clientSocket)
        nickname = clientSocket.recv(1024).decode('utf-8')
        # print("Nickname",nickname)
        # nicknames.append(nickname)
        print ("Connection established with: ", clientAddress[0] + ":" + str(clientAddress[1]))
        thread = Thread(target=clientThread, args=(clientSocket, clientAddress,nickname ))
        thread.start()

