from raknet import RakPeer


def test_create_server():
    server = RakPeer()
    server.startup(port=60000, max_connections=10)


def test_create_client():
    client = RakPeer()
    client.startup()
