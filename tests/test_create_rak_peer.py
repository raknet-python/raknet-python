import pytest

from raknet import RakPeer, StartupError


def test_server_startup():
    server = RakPeer()
    server.startup(port=60000, max_connections=10)


def test_client_startup():
    client = RakPeer()
    client.startup()


def test_duplicate_port():
    alice = RakPeer()
    alice.startup(port=2000)
    with pytest.raises(StartupError):
        bob = RakPeer()
        bob.startup(port=2000)


def test_negative_max_connections():
    with pytest.raises(StartupError):
        peer = RakPeer()
        peer.startup(max_connections=0)


# def test_bad_hostname():
#     with pytest.raises(StartupError):
#         peer = RakPeer()
#         peer.startup(host="bad-host-name")


def test_invalid_max_internal_ids():
    with pytest.raises(StartupError):
        peer = RakPeer()
        peer.startup(max_internal_ids=21)
    with pytest.raises(StartupError):
        peer = RakPeer()
        peer.startup(max_internal_ids=0)
