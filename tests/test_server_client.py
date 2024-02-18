import concurrent.futures
import time

from raknet import RakPeer, MessageIdentifiers, PacketPriority, PacketReliability

ID_GAME_MESSAGE_1 = MessageIdentifiers.ID_USER_PACKET_ENUM + 1


def run_server():
    server = RakPeer()
    server.max_incoming_connections = 10
    server.startup(port=60000, max_connections=10)

    timeout = time.time() + 2
    success = False
    while time.time() < timeout:
        packet = server.receive()
        if packet is None:
            continue
        if packet.data[0] == MessageIdentifiers.ID_NEW_INCOMING_CONNECTION:
            print("A connection is incoming.")
        elif packet.data[0] == MessageIdentifiers.ID_DISCONNECTION_NOTIFICATION:
            print("A client has disconnected.")
        elif packet.data[0] == MessageIdentifiers.ID_CONNECTION_LOST:
            print("A client lost the connection.")
        elif packet.data[0] == ID_GAME_MESSAGE_1:
            print(packet.data[1:].decode())
            success = True

    assert success, "Game message was not received after 2 seconds"


def run_client():
    client = RakPeer()
    client.startup()
    client.connect("127.0.0.1", 60000)

    timeout = time.time() + 2
    success = False
    while time.time() < timeout:
        packet = client.receive()
        if packet is None:
            continue
        if packet.data[0] == MessageIdentifiers.ID_NO_FREE_INCOMING_CONNECTIONS:
            print("The server is full.")
        elif packet.data[0] == MessageIdentifiers.ID_DISCONNECTION_NOTIFICATION:
            print("We have been disconnected.")
        elif packet.data[0] == MessageIdentifiers.ID_CONNECTION_LOST:
            print("Connection lost.")
        if packet.data[0] == MessageIdentifiers.ID_CONNECTION_REQUEST_ACCEPTED:
            print("Our connection request has been accepted.")
            host, port = packet.system_address
            client.send(
                bytes([ID_GAME_MESSAGE_1]) + b"Hello, World",
                PacketPriority.HIGH_PRIORITY,
                PacketReliability.RELIABLE_ORDERED,
                0,
                host,
                port,
            )
            success = True

    assert success, "Connection has not been accepted after 2 seconds"


def test_echo():
    with concurrent.futures.ProcessPoolExecutor(max_workers=2) as executor:
        futures = [executor.submit(run_server), executor.submit(run_client)]
        for future in futures:
            future.result()
