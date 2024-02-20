#include <pybind11/pybind11.h>

#include <string>
#include <utility>

#include <raknet/MessageIdentifiers.h>
#include <raknet/RakNetTypes.h>
#include <raknet/RakPeerInterface.h>

namespace raknet {
namespace python {

namespace py = pybind11;

struct StartupError : public std::runtime_error {
    using std::runtime_error::runtime_error;
};

struct ConnectionAttemptError : public std::runtime_error {
    using std::runtime_error::runtime_error;
};

struct Packet {
    Packet(py::bytes payload, const RakNet::SystemAddress &address)
        : data(std::move(payload)), system_address(address) {}

    py::bytes data;
    RakNet::SystemAddress system_address;
};

struct RakPeerDeleter {
    void operator()(RakNet::RakPeerInterface *p) { RakNet::RakPeerInterface::DestroyInstance(p); }
};

class MessageIdentifiers {};
#define DEF_DEFAULT_MESSAGE_ID(name)                                                                                   \
    def_property_readonly_static(#name, [](const py::object &) -> unsigned char { return DefaultMessageIDTypes::name; })

PYBIND11_MODULE(_raknet, m) {
    py::register_exception<StartupError>(m, "StartupError", PyExc_RuntimeError);
    py::register_exception<ConnectionAttemptError>(m, "ConnectionAttemptError", PyExc_RuntimeError);

    py::class_<MessageIdentifiers>(m, "MessageIdentifiers")
        .DEF_DEFAULT_MESSAGE_ID(ID_CONNECTED_PING)
        .DEF_DEFAULT_MESSAGE_ID(ID_UNCONNECTED_PING)
        .DEF_DEFAULT_MESSAGE_ID(ID_UNCONNECTED_PING_OPEN_CONNECTIONS)
        .DEF_DEFAULT_MESSAGE_ID(ID_CONNECTED_PONG)
        .DEF_DEFAULT_MESSAGE_ID(ID_DETECT_LOST_CONNECTIONS)
        .DEF_DEFAULT_MESSAGE_ID(ID_OPEN_CONNECTION_REQUEST_1)
        .DEF_DEFAULT_MESSAGE_ID(ID_OPEN_CONNECTION_REPLY_1)
        .DEF_DEFAULT_MESSAGE_ID(ID_OPEN_CONNECTION_REQUEST_2)
        .DEF_DEFAULT_MESSAGE_ID(ID_OPEN_CONNECTION_REPLY_2)
        .DEF_DEFAULT_MESSAGE_ID(ID_CONNECTION_REQUEST)
        .DEF_DEFAULT_MESSAGE_ID(ID_REMOTE_SYSTEM_REQUIRES_PUBLIC_KEY)
        .DEF_DEFAULT_MESSAGE_ID(ID_OUR_SYSTEM_REQUIRES_SECURITY)
        .DEF_DEFAULT_MESSAGE_ID(ID_PUBLIC_KEY_MISMATCH)
        .DEF_DEFAULT_MESSAGE_ID(ID_OUT_OF_BAND_INTERNAL)
        .DEF_DEFAULT_MESSAGE_ID(ID_SND_RECEIPT_ACKED)
        .DEF_DEFAULT_MESSAGE_ID(ID_SND_RECEIPT_LOSS)
        .DEF_DEFAULT_MESSAGE_ID(ID_CONNECTION_REQUEST_ACCEPTED)
        .DEF_DEFAULT_MESSAGE_ID(ID_CONNECTION_ATTEMPT_FAILED)
        .DEF_DEFAULT_MESSAGE_ID(ID_ALREADY_CONNECTED)
        .DEF_DEFAULT_MESSAGE_ID(ID_NEW_INCOMING_CONNECTION)
        .DEF_DEFAULT_MESSAGE_ID(ID_NO_FREE_INCOMING_CONNECTIONS)
        .DEF_DEFAULT_MESSAGE_ID(ID_DISCONNECTION_NOTIFICATION)
        .DEF_DEFAULT_MESSAGE_ID(ID_CONNECTION_LOST)
        .DEF_DEFAULT_MESSAGE_ID(ID_CONNECTION_BANNED)
        .DEF_DEFAULT_MESSAGE_ID(ID_INVALID_PASSWORD)
        .DEF_DEFAULT_MESSAGE_ID(ID_INCOMPATIBLE_PROTOCOL_VERSION)
        .DEF_DEFAULT_MESSAGE_ID(ID_IP_RECENTLY_CONNECTED)
        .DEF_DEFAULT_MESSAGE_ID(ID_TIMESTAMP)
        .DEF_DEFAULT_MESSAGE_ID(ID_UNCONNECTED_PONG)
        .DEF_DEFAULT_MESSAGE_ID(ID_ADVERTISE_SYSTEM)
        .DEF_DEFAULT_MESSAGE_ID(ID_DOWNLOAD_PROGRESS)
        .DEF_DEFAULT_MESSAGE_ID(ID_USER_PACKET_ENUM);

    py::enum_<PacketPriority>(m, "PacketPriority")
        .value("IMMEDIATE_PRIORITY", PacketPriority::IMMEDIATE_PRIORITY)
        .value("HIGH_PRIORITY", PacketPriority::HIGH_PRIORITY)
        .value("MEDIUM_PRIORITY", PacketPriority::MEDIUM_PRIORITY)
        .value("LOW_PRIORITY", PacketPriority::LOW_PRIORITY)
        .export_values();

    py::enum_<PacketReliability>(m, "PacketReliability")
        .value("UNRELIABLE", PacketReliability::UNRELIABLE)
        .value("UNRELIABLE_SEQUENCED", PacketReliability::UNRELIABLE_SEQUENCED)
        .value("RELIABLE", PacketReliability::RELIABLE)
        .value("RELIABLE_ORDERED", PacketReliability::RELIABLE_ORDERED)
        .value("RELIABLE_SEQUENCED", PacketReliability::RELIABLE_SEQUENCED)
        .value("UNRELIABLE_WITH_ACK_RECEIPT", PacketReliability::UNRELIABLE_WITH_ACK_RECEIPT)
        .value("RELIABLE_WITH_ACK_RECEIPT", PacketReliability::RELIABLE_WITH_ACK_RECEIPT)
        .value("RELIABLE_ORDERED_WITH_ACK_RECEIPT", PacketReliability::RELIABLE_ORDERED_WITH_ACK_RECEIPT)
        .export_values();

    py::class_<Packet>(m, "Packet")
        .def_readonly("data", &Packet::data)
        .def_readonly("system_address", &Packet::system_address);

    py::class_<RakNet::SystemAddress>(m, "SystemAddress")
        .def_property_readonly("host", [](RakNet::SystemAddress &self) { return self.ToString(false); })
        .def_property_readonly("port", &RakNet::SystemAddress::GetPort);

    py::class_<RakNet::RakPeerInterface, std::unique_ptr<RakNet::RakPeerInterface, RakPeerDeleter>>(m, "RakPeer")
        .def(py::init([]() {
            return std::unique_ptr<RakNet::RakPeerInterface, RakPeerDeleter>(RakNet::RakPeerInterface::GetInstance());
        }))

        .def(
            "startup",
            [](RakNet::RakPeerInterface &self,
               const char *host,
               unsigned short port,
               unsigned int max_connections,
               unsigned int protocol_version,
               unsigned int max_internal_ids) {
                auto local_addr = RakNet::SocketDescriptor(port, host);
                auto result = self.Startup(max_connections,
                                           &local_addr,
                                           1,
                                           -99999,
                                           static_cast<unsigned char>(protocol_version & 0xff),
                                           max_internal_ids);
                switch (result) {
                    case RakNet::RAKNET_STARTED:
                        break;
                    case RakNet::RAKNET_ALREADY_STARTED:
                        throw StartupError("RakNet is already started!");
                    case RakNet::INVALID_SOCKET_DESCRIPTORS:
                        throw StartupError("Invalid socket descriptors");
                    case RakNet::INVALID_MAX_CONNECTIONS:
                        throw StartupError("Invalid maximum connections");
                    case RakNet::SOCKET_FAMILY_NOT_SUPPORTED:
                        throw StartupError("Socket family not supported");
                    case RakNet::SOCKET_PORT_ALREADY_IN_USE:
                        throw StartupError("Socket port already in use");
                    case RakNet::SOCKET_FAILED_TO_BIND:
                        throw StartupError("Socket failed to bind");
                    case RakNet::SOCKET_FAILED_TEST_SEND:
                        throw StartupError("Socket failed on the test send");
                    case RakNet::PORT_CANNOT_BE_ZERO:
                        throw StartupError("Port number cannot be zero");
                    case RakNet::FAILED_TO_CREATE_NETWORK_THREAD:
                        throw StartupError("Failed to create network thread");
                    case RakNet::COULD_NOT_GENERATE_GUID:
                        throw StartupError("Could not generate GUID");
                    case RakNet::STARTUP_OTHER_FAILURE:
                        throw StartupError("Other startup failure");
                    default:
                        throw StartupError("Unknown error");
                }
            },
            py::arg("host") = py::none(),
            py::arg("port") = 0,
            py::arg("max_connections") = 1,
            py::arg("protocol_version") = 6,
            py::arg("max_internal_ids") = 10)

        .def(
            "connect",
            [](RakNet::RakPeerInterface &self,
               const std::string &host,
               unsigned short port,
               unsigned int num_attempts,
               unsigned int attempt_interval_ms,
               RakNet::TimeMS timeout) {
                auto result = self.Connect(
                    host.c_str(), port, nullptr, 0, nullptr, 0, num_attempts, attempt_interval_ms, timeout);
                switch (result) {
                    case RakNet::CONNECTION_ATTEMPT_STARTED:
                        break;
                    case RakNet::INVALID_PARAMETER:
                        throw ConnectionAttemptError("Invalid parameter");
                    case RakNet::CANNOT_RESOLVE_DOMAIN_NAME:
                        throw ConnectionAttemptError("Cannot resolve domain name");
                    case RakNet::ALREADY_CONNECTED_TO_ENDPOINT:
                        throw ConnectionAttemptError("Already connected to endpoint");
                    case RakNet::CONNECTION_ATTEMPT_ALREADY_IN_PROGRESS:
                        throw ConnectionAttemptError("Connection attempt already in progress");
                    case RakNet::SECURITY_INITIALIZATION_FAILED:
                        throw ConnectionAttemptError("Security initialization failed");
                    default:
                        throw ConnectionAttemptError("Unknown error");
                }
            },
            py::arg("host"),
            py::arg("port"),
            py::arg("num_attempts") = 6,
            py::arg("attempt_interval_ms") = 1000,
            py::arg("timeout") = 0)

        .def("receive",
             [](RakNet::RakPeerInterface &self) -> std::unique_ptr<Packet> {
                 auto *p = self.Receive();
                 if (!p) {
                     return nullptr;
                 }
                 auto packet = std::make_unique<Packet>(py::bytes(reinterpret_cast<const char *>(p->data), p->length),
                                                        p->systemAddress);
                 self.DeallocatePacket(p);
                 return packet;
             })

        .def(
            "send",
            [](RakNet::RakPeerInterface &self,
               const py::bytes &data,
               PacketPriority priority,
               PacketReliability reliability,
               unsigned int ordering_channel,
               RakNet::SystemAddress address,
               uint32_t force_receipt_num) {
                char *buffer = nullptr;
                py::ssize_t length = 0;
                if (PYBIND11_BYTES_AS_STRING_AND_SIZE(data.ptr(), &buffer, &length) != 0) {
                    throw py::error_already_set();
                }
                return self.Send(buffer,
                                 static_cast<int>(length),
                                 priority,
                                 reliability,
                                 static_cast<char>(ordering_channel & 0xff),
                                 address,
                                 false,
                                 force_receipt_num);
            },
            py::arg("data"),
            py::arg("priority"),
            py::arg("reliability"),
            py::arg("ordering_channel"),
            py::arg("address"),
            py::arg("force_receipt_num") = 0)

        .def(
            "shutdown",
            [](RakNet::RakPeerInterface &self,
               float timeout_secs,
               unsigned int ordering_channel,
               PacketPriority notification_priority) {
                if (timeout_secs < 0) {
                    throw std::invalid_argument("Invalid argument: timeout_secs cannot be less than 0.");
                }
                auto block_duration = static_cast<unsigned int>(timeout_secs * 1000);
                self.Shutdown(block_duration, static_cast<char>(ordering_channel & 0xff), notification_priority);
            },
            py::arg("timeout_secs"),
            py::arg("ordering_channel") = 0,
            py::arg("disconnection_notification_priority") = PacketPriority::LOW_PRIORITY)

        .def(
            "ping",
            [](RakNet::RakPeerInterface &self, const std::string &host, unsigned short port, bool flag) {
                return self.Ping(host.c_str(), port, flag);
            },
            py::arg("host"),
            py::arg("port"),
            py::arg("only_reply_on_accepting_connections") = false)

        .def("get_bound_address", &RakNet::RakPeerInterface::GetMyBoundAddress, py::arg("index") = 0)

        .def_property_readonly("active", &RakNet::RakPeerInterface::IsActive)
        .def_property_readonly("num_connections", &RakNet::RakPeerInterface::NumberOfConnections)
        .def_property("max_incoming_connections",
                      &RakNet::RakPeerInterface::GetMaximumIncomingConnections,
                      &RakNet::RakPeerInterface::SetMaximumIncomingConnections)
        .def_property(
            "offline_ping_response",
            [](RakNet::RakPeerInterface &self) {
                char *data;
                unsigned int length;
                self.GetOfflinePingResponse(&data, &length);
                return py::bytes(data, length);
            },
            [](RakNet::RakPeerInterface &self, py::bytes data) {
                char *buffer = nullptr;
                py::ssize_t length = 0;
                if (PYBIND11_BYTES_AS_STRING_AND_SIZE(data.ptr(), &buffer, &length) != 0) {
                    throw py::error_already_set();
                }
                self.SetOfflinePingResponse(buffer, length);
            });
}
} // namespace python
} // namespace raknet
