import importlib


def test_imports():
    module = importlib.import_module("raknet")
    getattr(module, "RakPeer")
