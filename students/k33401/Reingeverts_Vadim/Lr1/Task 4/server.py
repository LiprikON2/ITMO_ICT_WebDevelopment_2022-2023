import socket
from threading import Thread


class SocketServer(socket.socket):
    clients = []

    def __init__(self):
        # TCP
        socket.socket.__init__(self, socket.AF_INET, socket.SOCK_STREAM)
        # Ensures that port is always ready to be used again
        self.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        self.bind(('localhost', 12344))
        self.listen(10)
        # Makes keyboard interrupt possible at all times
        self.settimeout(1.0)

    def run(self):
        print(
            f"Started server at tcp://{self.getsockname()[0]}:{self.getsockname()[1]}")
        try:
            self.accept_clients()
        except KeyboardInterrupt:
            pass
        finally:
            self.stop()

    def stop(self):
        print("Stopping server...")
        for client in self.clients:
            client.close()
        self.close()

    def accept_clients(self):
        while True:
            print("LOOP accept_clients")
            try:
                connection, client_address = self.accept()
            # Handle timeout
            except IOError:
                continue
            # Adding client to clients list
            self.clients.append(connection)
            # Client Connected
            self.on_open(connection)
            # Receiving data from client
            thread = Thread(target=self.recieve, args=(connection,))
            thread.start()
            thread.join()

    def recieve(self, connection):
        while True:
            print("LOOP recieve")

            try:
                data = connection.recv(2048)
            # Handle timeout
            except IOError:
                print("break")
                # continue
                break
            if data == b"":
                break
            # Message Received
            self.on_message(connection, data)
        # Removing client from clients list
        self.clients.remove(connection)
        # Client Disconnected
        self.on_close(connection)
        # Closing connection with client
        connection.close()

        print(self.clients)
        return

    def broadcast(self, message):
        # Sending message to all clients
        for client in self.clients:
            print("Sending client a message...")
            client.send(message)

    def on_open(self, connection):
        pass

    def on_message(self, connection, message):
        pass

    def on_close(self, connection):
        pass


class ChatServer(SocketServer):

    def __init__(self):
        SocketServer.__init__(self)

    def on_message(self, connection, message):
        print(message.decode("utf-8"))
        # Sending message to all clients
        self.broadcast(message)

    def on_open(self, connection):
        print("Client Connected")
        # connection.settimeout(5.0)

    def on_close(self, connection):
        print("Client Disconnected")


if __name__ == "__main__":
    server = ChatServer()
    server.run()
