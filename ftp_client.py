import socket

def get_command():
    while True:
        command = input("ftp> ")
        if command:
            return command

def main():
    server_host = "localhost"
    server_port = 1234

    control_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        control_socket.connect((server_host, server_port))
        print("Connected to server.")
        print("Type 'quit' to exit.")

        while True:
            command = get_command()
            control_socket.send(command.encode())

            if command == "quit":
                break

            if command.startswith("get"):
                filename = command.split()[1]
                with open(filename, 'wb') as file:
                    while True:
                        data = control_socket.recv(1024)
                        if not data:
                            break
                        file.write(data)
                print(f"File '{filename}' received successfully.")
                # After receiving the file, return to the main loop
                continue
                
            elif command == "ls":
                data = control_socket.recv(4096).decode()
                print("Files on server:\n", data)
    except ConnectionRefusedError:
        print("Error: Server is not available.")
    except KeyboardInterrupt:
        print("Connection closed.")
    finally:
        control_socket.close()

if __name__ == "__main__":
    main()
