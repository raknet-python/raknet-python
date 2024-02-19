__all__ = [
    "RakPeer",
    "SystemAddress",
    "Packet",
    "PacketPriority",
    "PacketReliability",
    "MessageIdentifiers",
    "ConnectionAttemptError",
    "StartupError",
]

for name in __all__:
    from importlib import import_module

    module = import_module("raknet.raknet_python")
    globals()[f"_{name}"] = module.__dict__[name]
    del module

RakPeer = globals()["_RakPeer"]
SystemAddress = globals()["_SystemAddress"]
Packet = globals()["_Packet"]
PacketPriority = globals()["_PacketPriority"]
PacketReliability = globals()["_PacketReliability"]
MessageIdentifiers = globals()["_MessageIdentifiers"]
ConnectionAttemptError = globals()["_ConnectionAttemptError"]
StartupError = globals()["_StartupError"]
