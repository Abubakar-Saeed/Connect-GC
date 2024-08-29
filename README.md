**Project Overview**
This project is a simple implementation of socket programming for a computer network course. It demonstrates a basic client-server communication using sockets in Python.
The project involves two main components:

**Server:** Listens for incoming client connections and processes requests.
**Client:** Connects to the server and sends/receives messages.

**Features**
- Establishes a connection between a client and a server using sockets.
- Sends and receives data over the network.
- Demonstrates basic network communication protocols.

**Files**
- server.py: Python script that starts a server, listens for incoming connections, and handles client requests.
- client.py: Python script that connects to the server and sends/receives messages.

**Requirements**
- Python 3.x installed on your machine.
- Basic understanding of Python and socket programming concepts.
- Both server.py and client.py need to be on the same network or configured for remote access.

**How to Run**

**Running the Server**
1. Open a terminal.
2. Navigate to the directory where server.py is located.
3. Run the server using the following command:
4. python3 server.py
5. The server will start listening on the specified IP address and port number.

**Running the Client**
1. Open another terminal.
2. Navigate to the directory where client.py is located.
3. Run the client using the following command:
4. python3 client.py
5. The client will connect to the server and you can start sending messages.

**Configuration**
- Ensure both client and server scripts are configured with the correct IP address and port numbers.
- Modify the host and port variables in both server.py and client.py if needed to match your network configuration.

**Usage**
- After running the server, run the client script to establish a connection.
- Follow the prompts to send messages from the client to the server.
- The server will process and respond to the client messages accordingly.

**Troubleshooting**
- If the client cannot connect to the server, check that the server is running and listening on the correct port.
- Ensure there are no firewall restrictions blocking the connection.
- Verify that both client and server are on the same network.


