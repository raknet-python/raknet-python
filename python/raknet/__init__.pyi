import typing


class ConnectionAttemptError(RuntimeError):
    pass

class StartupError(RuntimeError):
    pass

class MessageIdentifiers:
    class DefaultMessageIDTypes: ...
    ID_ADVERTISE_SYSTEM: typing.ClassVar[MessageIdentifiers.DefaultMessageIDTypes]  # value = <DefaultMessageIDTypes.ID_ADVERTISE_SYSTEM: 29>
    ID_ALREADY_CONNECTED: typing.ClassVar[MessageIdentifiers.DefaultMessageIDTypes]  # value = <DefaultMessageIDTypes.ID_ALREADY_CONNECTED: 18>
    ID_CONNECTED_PING: typing.ClassVar[MessageIdentifiers.DefaultMessageIDTypes]  # value = <DefaultMessageIDTypes.ID_CONNECTED_PING: 0>
    ID_CONNECTED_PONG: typing.ClassVar[MessageIdentifiers.DefaultMessageIDTypes]  # value = <DefaultMessageIDTypes.ID_CONNECTED_PONG: 3>
    ID_CONNECTION_ATTEMPT_FAILED: typing.ClassVar[MessageIdentifiers.DefaultMessageIDTypes]  # value = <DefaultMessageIDTypes.ID_CONNECTION_ATTEMPT_FAILED: 17>
    ID_CONNECTION_BANNED: typing.ClassVar[MessageIdentifiers.DefaultMessageIDTypes]  # value = <DefaultMessageIDTypes.ID_CONNECTION_BANNED: 23>
    ID_CONNECTION_LOST: typing.ClassVar[MessageIdentifiers.DefaultMessageIDTypes]  # value = <DefaultMessageIDTypes.ID_CONNECTION_LOST: 22>
    ID_CONNECTION_REQUEST: typing.ClassVar[MessageIdentifiers.DefaultMessageIDTypes]  # value = <DefaultMessageIDTypes.ID_CONNECTION_REQUEST: 9>
    ID_CONNECTION_REQUEST_ACCEPTED: typing.ClassVar[MessageIdentifiers.DefaultMessageIDTypes]  # value = <DefaultMessageIDTypes.ID_CONNECTION_REQUEST_ACCEPTED: 16>
    ID_DETECT_LOST_CONNECTIONS: typing.ClassVar[MessageIdentifiers.DefaultMessageIDTypes]  # value = <DefaultMessageIDTypes.ID_DETECT_LOST_CONNECTIONS: 4>
    ID_DISCONNECTION_NOTIFICATION: typing.ClassVar[MessageIdentifiers.DefaultMessageIDTypes]  # value = <DefaultMessageIDTypes.ID_DISCONNECTION_NOTIFICATION: 21>
    ID_DOWNLOAD_PROGRESS: typing.ClassVar[MessageIdentifiers.DefaultMessageIDTypes]  # value = <DefaultMessageIDTypes.ID_DOWNLOAD_PROGRESS: 30>
    ID_INCOMPATIBLE_PROTOCOL_VERSION: typing.ClassVar[MessageIdentifiers.DefaultMessageIDTypes]  # value = <DefaultMessageIDTypes.ID_INCOMPATIBLE_PROTOCOL_VERSION: 25>
    ID_INVALID_PASSWORD: typing.ClassVar[MessageIdentifiers.DefaultMessageIDTypes]  # value = <DefaultMessageIDTypes.ID_INVALID_PASSWORD: 24>
    ID_IP_RECENTLY_CONNECTED: typing.ClassVar[MessageIdentifiers.DefaultMessageIDTypes]  # value = <DefaultMessageIDTypes.ID_IP_RECENTLY_CONNECTED: 26>
    ID_NEW_INCOMING_CONNECTION: typing.ClassVar[MessageIdentifiers.DefaultMessageIDTypes]  # value = <DefaultMessageIDTypes.ID_NEW_INCOMING_CONNECTION: 19>
    ID_NO_FREE_INCOMING_CONNECTIONS: typing.ClassVar[MessageIdentifiers.DefaultMessageIDTypes]  # value = <DefaultMessageIDTypes.ID_NO_FREE_INCOMING_CONNECTIONS: 20>
    ID_OPEN_CONNECTION_REPLY_1: typing.ClassVar[MessageIdentifiers.DefaultMessageIDTypes]  # value = <DefaultMessageIDTypes.ID_OPEN_CONNECTION_REPLY_1: 6>
    ID_OPEN_CONNECTION_REPLY_2: typing.ClassVar[MessageIdentifiers.DefaultMessageIDTypes]  # value = <DefaultMessageIDTypes.ID_OPEN_CONNECTION_REPLY_2: 8>
    ID_OPEN_CONNECTION_REQUEST_1: typing.ClassVar[MessageIdentifiers.DefaultMessageIDTypes]  # value = <DefaultMessageIDTypes.ID_OPEN_CONNECTION_REQUEST_1: 5>
    ID_OPEN_CONNECTION_REQUEST_2: typing.ClassVar[MessageIdentifiers.DefaultMessageIDTypes]  # value = <DefaultMessageIDTypes.ID_OPEN_CONNECTION_REQUEST_2: 7>
    ID_OUR_SYSTEM_REQUIRES_SECURITY: typing.ClassVar[MessageIdentifiers.DefaultMessageIDTypes]  # value = <DefaultMessageIDTypes.ID_OUR_SYSTEM_REQUIRES_SECURITY: 11>
    ID_OUT_OF_BAND_INTERNAL: typing.ClassVar[MessageIdentifiers.DefaultMessageIDTypes]  # value = <DefaultMessageIDTypes.ID_OUT_OF_BAND_INTERNAL: 13>
    ID_PUBLIC_KEY_MISMATCH: typing.ClassVar[MessageIdentifiers.DefaultMessageIDTypes]  # value = <DefaultMessageIDTypes.ID_PUBLIC_KEY_MISMATCH: 12>
    ID_REMOTE_SYSTEM_REQUIRES_PUBLIC_KEY: typing.ClassVar[MessageIdentifiers.DefaultMessageIDTypes]  # value = <DefaultMessageIDTypes.ID_REMOTE_SYSTEM_REQUIRES_PUBLIC_KEY: 10>
    ID_SND_RECEIPT_ACKED: typing.ClassVar[MessageIdentifiers.DefaultMessageIDTypes]  # value = <DefaultMessageIDTypes.ID_SND_RECEIPT_ACKED: 14>
    ID_SND_RECEIPT_LOSS: typing.ClassVar[MessageIdentifiers.DefaultMessageIDTypes]  # value = <DefaultMessageIDTypes.ID_SND_RECEIPT_LOSS: 15>
    ID_TIMESTAMP: typing.ClassVar[MessageIdentifiers.DefaultMessageIDTypes]  # value = <DefaultMessageIDTypes.ID_TIMESTAMP: 27>
    ID_UNCONNECTED_PING: typing.ClassVar[MessageIdentifiers.DefaultMessageIDTypes]  # value = <DefaultMessageIDTypes.ID_UNCONNECTED_PING: 1>
    ID_UNCONNECTED_PING_OPEN_CONNECTIONS: typing.ClassVar[MessageIdentifiers.DefaultMessageIDTypes]  # value = <DefaultMessageIDTypes.ID_UNCONNECTED_PING_OPEN_CONNECTIONS: 2>
    ID_UNCONNECTED_PONG: typing.ClassVar[MessageIdentifiers.DefaultMessageIDTypes]  # value = <DefaultMessageIDTypes.ID_UNCONNECTED_PONG: 28>

class Packet:
    @property
    def data(self) -> bytes:
        ...

class RakPeer:
    max_incoming_connections: int
    def __init__(self) -> None:
        ...
    def connect(self, host: str, port: int, attempts: int = 6, attempt_interval_ms: int = 1000, timeout: int = 0) -> None:
        ...
    def receive(self) -> Packet:
        ...
    def startup(self, host: str = None, port: int = 0, max_connections: int = 1, protocol_version: int = 6, max_internal_ids: int = 10) -> None:
        ...