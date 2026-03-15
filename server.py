import socket
import threading
import os

HOST = "0.0.0.0"
PORT = 9000


def port_scan(ip):
    open_ports = []
    for port in range(20, 200):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(0.3)

        if s.connect_ex((ip, port)) == 0:
            open_ports.append(port)

        s.close()

    return open_ports


def handle_client(conn, addr):
    print(f"Connected: {addr}")

    cmd = conn.recv(1024).decode()

    if cmd.startswith("SCAN"):
        ip = cmd.split()[1]
        ports = port_scan(ip)
        response = "Open ports: " + str(ports)
        conn.send(response.encode())

    elif cmd.startswith("UPLOAD"):
        filename = cmd.split()[1]
        data = conn.recv(4096)

        with open(filename, "wb") as f:
            f.write(data)

        conn.send(b"File uploaded successfully")

    elif cmd.startswith("DOWNLOAD"):
        filename = cmd.split()[1]

        if os.path.exists(filename):
            with open(filename, "rb") as f:
                conn.send(f.read())
        else:
            conn.send(b"File not found")

    conn.close()


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

print(f"Server running on port {PORT}...")

while True:
    conn, addr = server.accept()
    thread = threading.Thread(target=handle_client, args=(conn, addr))
    thread.start()
