#Server for the client-server architecture
import socket
import threading

# Intialize host ipv4 address and port number
HOST = '192.168.2.17' #OR socket.gethostbyname(socket.gethostname())
PORT = 22222

# Initialize the socket as an Internet TCP Socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#Bind the server to our host and port
server.bind((HOST, PORT))

#Start listening to incoming connections
server.listen()

#
clients = []
usernames = []

# Function to send a certain message to each client in the server
def broadcast(message):
    for client in clients:
        client.send(message)

def handle(client):
    while True:
            #Receive client message from communication socket and decode it
            message = client.recv(1024)
            broadcast(message)


def receive():
    while True:
        # Each connection will have a communication socket and an address
        client, address = server.accept()
        print("Connected to ", address)

        client.send('NAME'.encode('utf-8'))
        username = client.recv(1024).decode('utf-8')
        usernames.append(username)
        clients.append(client)

        print("Nickname of the client is ", username)
        broadcast(f'{username} joined the chat\n'.encode('utf-8'))
        client.send("Connected to the server".encode('utf-8'))

        # Run a thread for each client
        thread = threading.Thread(target=handle, args= (client,))
        thread.start()


receive()   