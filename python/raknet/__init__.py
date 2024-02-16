__all__ = ["RakPeer", "Packet", "MessageIdentifiers", "ConnectionAttemptError", "StartupError", ]

for name in __all__:
    from importlib import import_module

    module = import_module("raknet.raknet_python")
    globals()[f"_{name}"] = module.__dict__[name]
    del module

RakPeer = globals()["_RakPeer"]
Packet = globals()["_Packet"]
MessageIdentifiers = globals()["_MessageIdentifiers"]
ConnectionAttemptError = globals()["_ConnectionAttemptError"]
StartupError = globals()["_StartupError"]
