__all__ = ["RakPeer", "StartupError", "MessageIdentifiers"]

for name in __all__:
    from importlib import import_module

    module = import_module("raknet.raknet_python")
    globals()[f"_{name}"] = module.__dict__[name]
    del module

RakPeer = globals()["_RakPeer"]
StartupError = globals()["_StartupError"]
MessageIdentifiers = globals()["_MessageIdentifiers"]
