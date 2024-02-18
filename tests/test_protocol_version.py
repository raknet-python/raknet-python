import time

from raknet import RakPeer, MessageIdentifiers

ID_GAME_MESSAGE_1 = MessageIdentifiers.ID_USER_PACKET_ENUM + 1


def do_test(server_ver: int, client_ver: int):
    server = RakPeer()
    server.max_incoming_connections = 10
    server.startup(port=60000 + server_ver, max_connections=10, protocol_version=server_ver)

    client = RakPeer()
    client.startup(protocol_version=client_ver)
    client.connect("127.0.0.1", 60000 + server_ver)

    timeout = time.time() + 2
    success = False
    while time.time() < timeout:
        packet = client.receive()
        if packet is None:
            continue

        if packet.data[0] == MessageIdentifiers.ID_CONNECTION_REQUEST_ACCEPTED:
            assert server_ver == client_ver
            success = True
        elif packet.data[0] == MessageIdentifiers.ID_INCOMPATIBLE_PROTOCOL_VERSION:
            assert server_ver != client_ver
            success = True

    assert success


def test_compatible_1():
    do_test(6, 6)


def test_compatible_2():
    do_test(11, 11)


def test_incompatible_1():
    do_test(6, 11)


def test_incompatible_2():
    do_test(11, 6)
