import socket

SERVER_IP = "127.0.0.1"
PORT = 9000

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((SERVER_IP, PORT))

command = input("Enter command (SCAN IP / UPLOAD file / DOWNLOAD file): ")

client.send(command.encode())

if command.startswith("UPLOAD"):
    filename = command.split()[1]

    with open(filename, "rb") as f:
        data = f.read()
        client.send(data)

response = client.recv(4096)

if command.startswith("DOWNLOAD"):
    filename = command.split()[1]

    with open("downloaded_" + filename, "wb") as f:
        f.write(response)

    print("File downloaded")

else:
    print(response.decode())

client.close()
