import concurrent.futures
import time

from raknet import RakPeer, MessageIdentifiers, PacketPriority, PacketReliability

ID_GAME_MESSAGE_1 = MessageIdentifiers.ID_USER_PACKET_ENUM + 1


def run_server(server: RakPeer):
    timeout = time.time() + 5
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
            print(packet.data[1:], packet.system_address)
            assert packet.data[1:] == b"Hello, World"
            return

    assert False, "Game message was not received"


def run_client(client: RakPeer):
    timeout = time.time() + 5
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
            client.send(
                bytes([ID_GAME_MESSAGE_1]) + b"Hello, World",
                PacketPriority.HIGH_PRIORITY,
                PacketReliability.RELIABLE_ORDERED,
                0,
                packet.system_address
            )
            client.shutdown(1)
            return

    assert False, "Connection timed out"


def test_echo():
    server = RakPeer()
    server.max_incoming_connections = 10
    server.startup()
    server_addr = server.get_bound_address()

    client = RakPeer()
    client.startup()
    client.connect(server_addr.host, server_addr.port)

    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        futures = [executor.submit(run_server, server), executor.submit(run_client, client)]
        for future in futures:
            future.result()
