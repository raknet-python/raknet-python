#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

#include <raknet/RakNetTypes.h>
#include <raknet/RakPeer.h>

namespace py = pybind11;

struct StartupError : public std::runtime_error {
    using std::runtime_error::runtime_error;
};

struct ConnectionAttemptError : public std::runtime_error {
    using std::runtime_error::runtime_error;
};

PYBIND11_MODULE(raknet_python, m) {
    py::register_exception<StartupError>(m, "StartupError", PyExc_RuntimeError);
    py::register_exception<ConnectionAttemptError>(m, "ConnectionAttemptError", PyExc_RuntimeError);

    py::class_<RakNet::Packet>(m, "Packet").def_readonly("data", &RakNet::Packet::data);

    py::class_<RakNet::RakPeer>(m, "RakPeer")
        .def(py::init<>())

        .def(
            "startup",
            [](RakNet::RakPeer &a,
               const std::string &host,
               int port,
               unsigned int max_connections,
               int protocol_version,
               int max_internal_ids) {
                auto local_addr = RakNet::SocketDescriptor(port, host.c_str());
                auto result = a.Startup(max_connections, &local_addr, 1, -99999, protocol_version, max_internal_ids);
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
            [](RakNet::RakPeer &a,
               const std::string &host,
               int remote_port,
               int attempts,
               int attempt_interval_ms,
               int timeout) {
                auto result = a.Connect(
                    host.c_str(), remote_port, nullptr, 0, nullptr, 0, attempts, attempt_interval_ms, timeout);
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
            py::arg("attempts") = 6,
            py::arg("attempt_interval_ms") = 1000,
            py::arg("timeout") = 0)

        .def("receive", [](RakNet::RakPeer &a) { return std::move(std::unique_ptr<RakNet::Packet>(a.Receive())); })

        .def_property("max_incoming_connections",
                      &RakNet::RakPeer::GetMaximumIncomingConnections,
                      &RakNet::RakPeer::SetMaximumIncomingConnections);
}
