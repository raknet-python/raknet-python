import time
from struct import unpack

from raknet import RakPeer, MessageIdentifiers


def test_unconnected_ping():
    server = RakPeer()
    server.max_incoming_connections = 10
    server.offline_ping_response = b"Ping, Pong!"
    assert server.offline_ping_response == b"Ping, Pong!"
    server.startup()
    server_addr = server.get_bound_address()

    client = RakPeer()
    client.startup()

    timeout = time.time() + 5
    while time.time() < timeout:
        client.ping(server_addr.host, server_addr.port)

        packet = client.receive()
        if packet is None:
            continue
        if packet.data[0] == MessageIdentifiers.ID_UNCONNECTED_PONG:
            ping_time = unpack(">I", packet.data[1:5])[0]
            response = packet.data[5:]
            assert response == server.offline_ping_response
            print(ping_time, response)
            client.shutdown(1)
            return

        time.sleep(0.5)

    assert False, "Ping remote server timed out"
