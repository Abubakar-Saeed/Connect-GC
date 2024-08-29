import socket
import threading

HOST = "127.0.0.1"
PORT = 1234  # We can use any port between 0 to 65535
LISTENER_LIMIT = 35
active_clients = []  # List of all currently connected users

# Function to listen for upcoming messages from a client


def listen_for_messages(client, username):
    while True:
        try:
            message = client.recv(2048).decode('utf-8')
            if not message:
                # If the message is empty, it means the client has disconnected
                handle_user_disconnection(username, client)
                break

            final_msg = username + '~' + message
            send_messages_to_all(final_msg)

        except ConnectionResetError:
            # Handle disconnection due to ConnectionResetError
            handle_user_disconnection(username, client)
            break

# Function to send message to a single client


def send_message_to_client(client, message):
    client.sendall(message.encode())

# Function to send any new message to all the clients that
# are currently connected to this server


def send_messages_to_all(message):
    for user in active_clients:
        if user[1].fileno() != -1:
            send_message_to_client(user[1], message)

# Function to handle user disconnection


def handle_user_disconnection(username, client):
    active_clients.remove((username, client))
    disconnection_message = "Connect GC~" + f"{username} left the chat 😪😪"
    send_messages_to_all(disconnection_message)

# Function to handle each client connection


def client_handler(client):
    while True:
        try:
            username = client.recv(2048).decode('utf-8')
            if username:
                active_clients.append((username, client))
                prompt_message = "Connect GC~" + f"{username} added to the chat 😮😉"
                send_messages_to_all(prompt_message)
                break

        except ConnectionResetError:
            # Handle disconnection due to ConnectionResetError
            break

        except:
            print("Client username is empty or another error occurred")

    threading.Thread(target=listen_for_messages, args=(client, username)).start()

# Main function


def main():
    # Creating the socket class object
    # AF_INET: we are going to use IPv4 addresses
    # SOCK_STREAM: we are using TCP packets for communication
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Creating a try-except block
    try:
        # Provide the server with an address in the form of
        # host IP and port
        server.bind((HOST, PORT))
        print(f"Running the server on {HOST} {PORT}")
    except OSError as e:
        print(f"Unable to bind to host {HOST} and port {PORT}: {e}")
        return

    # Set server limit
    server.listen(LISTENER_LIMIT)

    # This while loop will keep listening to client connections
    try:
        while True:
            client, address = server.accept()
            print(f"Successfully connected to client {address[0]} {address[1]}")
            threading.Thread(target=client_handler, args=(client,)).start()

    except KeyboardInterrupt:
        print("Server shutting down.")
        server.close()


if __name__ == '__main__':
    main()
