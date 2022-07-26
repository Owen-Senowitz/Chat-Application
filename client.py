import re
import socket
import errno
import sys

HEADER_LENGTH = 10

# Prompts the user for IP, PORT and username
print("Press Enter For Localhost")
ip = input("IP: ")
if (len(ip) == 0):
    ip = "127.0.0.1"
print(ip)
print("Press Enter For Port 6969")
port = input("PORT: ")
if (len(port) == 0):
    port = 6969
print(port)
my_username = input("Username: ")

# Create a socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Connect to a server with the given ip and port
client_socket.connect((ip, int(port)))
client_socket.setblocking(False)

# Send the username to the server
username = my_username.encode('utf-8')
username_header = f"{len(username):<{HEADER_LENGTH}}".encode('utf-8')
client_socket.send(username_header + username)

while True:
    # Receive the message from the console
    message = input(f'{my_username}: ')
    # If message is "exit" or "end" the client will close the connection
    if (message == "exit" or message == "end"):
        client_socket.close()
        sys.exit()
    # If there is a message then we send it to the server
    if message:

        message = message.encode('utf-8')
        message_header = f"{len(message):<{HEADER_LENGTH}}".encode('utf-8')
        client_socket.send(message_header + message)

    try:
        while True:
            # Receive the username_header from the server
            username_header = client_socket.recv(HEADER_LENGTH)
            # If the username_header is empty then the server has closed the connection
            if not len(username_header):
                print('Connection closed by the server')
                sys.exit()

            username_length = int(username_header.decode('utf-8').strip())

            username = client_socket.recv(username_length).decode('utf-8')

            message_header = client_socket.recv(HEADER_LENGTH)
            message_length = int(message_header.decode('utf-8').strip())
            message = client_socket.recv(message_length).decode('utf-8')

            print(f'{username} > {message}')
    # Catches a reading error
    except IOError as e:
        if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
            print('Reading error: {}'.format(str(e)))
            sys.exit()

        continue
    
    except Exception as e:
        print('Reading error: '.format(str(e)))
        sys.exit()