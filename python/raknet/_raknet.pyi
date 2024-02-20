# @formatter:off # fmt: off
import typing


class ConnectionAttemptError(RuntimeError):
    ...


class StartupError(RuntimeError):
    ...


class MessageIdentifiers:
    ID_ADVERTISE_SYSTEM: typing.ClassVar[int] = 29
    ID_ALREADY_CONNECTED: typing.ClassVar[int] = 18
    ID_CONNECTED_PING: typing.ClassVar[int] = 0
    ID_CONNECTED_PONG: typing.ClassVar[int] = 3
    ID_CONNECTION_ATTEMPT_FAILED: typing.ClassVar[int] = 17
    ID_CONNECTION_BANNED: typing.ClassVar[int] = 23
    ID_CONNECTION_LOST: typing.ClassVar[int] = 22
    ID_CONNECTION_REQUEST: typing.ClassVar[int] = 9
    ID_CONNECTION_REQUEST_ACCEPTED: typing.ClassVar[int] = 16
    ID_DETECT_LOST_CONNECTIONS: typing.ClassVar[int] = 4
    ID_DISCONNECTION_NOTIFICATION: typing.ClassVar[int] = 21
    ID_DOWNLOAD_PROGRESS: typing.ClassVar[int] = 30
    ID_INCOMPATIBLE_PROTOCOL_VERSION: typing.ClassVar[int] = 25
    ID_INVALID_PASSWORD: typing.ClassVar[int] = 24
    ID_IP_RECENTLY_CONNECTED: typing.ClassVar[int] = 26
    ID_NEW_INCOMING_CONNECTION: typing.ClassVar[int] = 19
    ID_NO_FREE_INCOMING_CONNECTIONS: typing.ClassVar[int] = 20
    ID_OPEN_CONNECTION_REPLY_1: typing.ClassVar[int] = 6
    ID_OPEN_CONNECTION_REPLY_2: typing.ClassVar[int] = 8
    ID_OPEN_CONNECTION_REQUEST_1: typing.ClassVar[int] = 5
    ID_OPEN_CONNECTION_REQUEST_2: typing.ClassVar[int] = 7
    ID_OUR_SYSTEM_REQUIRES_SECURITY: typing.ClassVar[int] = 11
    ID_OUT_OF_BAND_INTERNAL: typing.ClassVar[int] = 13
    ID_PUBLIC_KEY_MISMATCH: typing.ClassVar[int] = 12
    ID_REMOTE_SYSTEM_REQUIRES_PUBLIC_KEY: typing.ClassVar[int] = 10
    ID_SND_RECEIPT_ACKED: typing.ClassVar[int] = 14
    ID_SND_RECEIPT_LOSS: typing.ClassVar[int] = 15
    ID_TIMESTAMP: typing.ClassVar[int] = 27
    ID_UNCONNECTED_PING: typing.ClassVar[int] = 1
    ID_UNCONNECTED_PING_OPEN_CONNECTIONS: typing.ClassVar[int] = 2
    ID_UNCONNECTED_PONG: typing.ClassVar[int] = 28
    ID_USER_PACKET_ENUM: typing.ClassVar[int] = 134


class SystemAddress:
    @property
    def host(self) -> str:
        ...
    @property
    def port(self) -> int:
        ...


class Packet:
    @property
    def data(self) -> bytes:
        ...
    @property
    def system_address(self) -> SystemAddress:
        ...


class PacketPriority:
    HIGH_PRIORITY: typing.ClassVar[PacketPriority]  # value = <PacketPriority.HIGH_PRIORITY: 1>
    IMMEDIATE_PRIORITY: typing.ClassVar[PacketPriority]  # value = <PacketPriority.IMMEDIATE_PRIORITY: 0>
    LOW_PRIORITY: typing.ClassVar[PacketPriority]  # value = <PacketPriority.LOW_PRIORITY: 3>
    MEDIUM_PRIORITY: typing.ClassVar[PacketPriority]  # value = <PacketPriority.MEDIUM_PRIORITY: 2>


class PacketReliability:
    RELIABLE: typing.ClassVar[PacketReliability]  # value = <PacketReliability.RELIABLE: 2>
    RELIABLE_ORDERED: typing.ClassVar[PacketReliability]  # value = <PacketReliability.RELIABLE_ORDERED: 3>
    RELIABLE_ORDERED_WITH_ACK_RECEIPT: typing.ClassVar[PacketReliability]  # value = <PacketReliability.RELIABLE_ORDERED_WITH_ACK_RECEIPT: 7>
    RELIABLE_SEQUENCED: typing.ClassVar[PacketReliability]  # value = <PacketReliability.RELIABLE_SEQUENCED: 4>
    RELIABLE_WITH_ACK_RECEIPT: typing.ClassVar[PacketReliability]  # value = <PacketReliability.RELIABLE_WITH_ACK_RECEIPT: 6>
    UNRELIABLE: typing.ClassVar[PacketReliability]  # value = <PacketReliability.UNRELIABLE: 0>
    UNRELIABLE_SEQUENCED: typing.ClassVar[PacketReliability]  # value = <PacketReliability.UNRELIABLE_SEQUENCED: 1>
    UNRELIABLE_WITH_ACK_RECEIPT: typing.ClassVar[PacketReliability]  # value = <PacketReliability.UNRELIABLE_WITH_ACK_RECEIPT: 5>


class RakPeer:
    max_incoming_connections: int
    offline_ping_response: bytes
    def __init__(self) -> None:
        ...
    def connect(self, host: str, port: int, num_attempts: int = 6, attempt_interval_ms: int = 1000, timeout: int = 0) -> None:
        ...
    def get_bound_address(self, index: int = 0) -> SystemAddress:
        ...
    def ping(self, host: str, port: int, only_reply_on_accepting_connections: bool = False) -> bool:
        ...
    def receive(self) -> Packet:
        ...
    def send(self, data: bytes, priority: PacketPriority, reliability: PacketReliability, ordering_channel: int, address: SystemAddress, force_receipt_num: int = 0) -> int:
        ...
    def shutdown(self, timeout_secs: float, ordering_channel: int = 0, disconnection_notification_priority: PacketPriority = ...) -> None:
        ...
    def startup(self, host: str = None, port: int = 0, max_connections: int = 1, protocol_version: int = 6, max_internal_ids: int = 10) -> None:
        ...
    @property
    def active(self) -> bool:
        ...
    @property
    def num_connections(self) -> int:
        ...

# @formatter:on # fmt: on