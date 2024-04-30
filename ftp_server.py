import socket
import os

def send_file(conn, filename):
    try:
        with open(filename, 'rb') as file:
            data = file.read(1024)
            while data:
                conn.send(data)
                data = file.read(1024)
        print(f"File '{filename}' sent successfully.")
    except FileNotFoundError:
        conn.send(b"File not found.")

def receive_file(conn, filename):
    try:
        with open(filename, 'wb') as file:
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                file.write(data)
        print(f"File '{filename}' received successfully.")
    except Exception as e:
        print("Error:", e)

def list_files(conn):
    files = "\n".join(os.listdir())
    conn.send(files.encode())

def handle_client(conn):
    print("Connected to client.")

    while True:
        command = conn.recv(1024).decode()
        if not command:
            break

        if command.startswith("get"):
            filename = command.split()[1]
            send_file(conn, filename)
        elif command.startswith("put"):
            filename = command.split()[1]
            receive_file(conn, filename)
        elif command == "ls":
            list_files(conn)
        elif command == "quit":
            break

    print("Connection closed.")
    conn.close()

def main():
    host = "localhost"
    port = 1234

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)

    print("Server started. Waiting for connections...")

    try:
        while True:
            conn, addr = server_socket.accept()
            handle_client(conn)
    except KeyboardInterrupt:
        print("Server stopped.")
    finally:
        server_socket.close()

if __name__ == "__main__":
    main()
