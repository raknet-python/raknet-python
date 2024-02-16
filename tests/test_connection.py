import time

import pytest
from raknet import RakPeer, MessageIdentifiers


@pytest.fixture
def server():
    server = RakPeer()
    server.startup(port=60000, max_connections=10)
    server.max_incoming_connections = 10
    return server


@pytest.fixture
def client():
    client = RakPeer()
    client.startup()
    return client


def test_connection(server, client):
    client.connect("127.0.0.1", 60000)
    timeout = time.time() + 5

    while time.time() < timeout:
        packet = client.receive()
        if packet is None:
            continue

        if packet.data[0] == MessageIdentifiers.ID_CONNECTION_REQUEST_ACCEPTED:
            return

    assert False, "Connection has not been accepted after 5 seconds"
