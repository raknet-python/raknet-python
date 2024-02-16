#include <pybind11/pybind11.h>

#include "rak_peer.h"

#include "raknet_error.h"

#include <raknet/RakNetTypes.h>
#include <raknet/RakPeer.h>

namespace py = pybind11;

void def_rak_peer(pybind11::module &m) {
    py::class_<RakNet::RakPeer>(m, "RakPeer")
        .def(py::init<>())
        .def(
            "startup",
            [](RakNet::RakPeer &a,
               const char *host,
               int port,
               unsigned int max_connections,
               int protocol_version,
               int max_internal_ids) {
                auto local_addr = RakNet::SocketDescriptor(port, host);
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
            py::arg("protocol_version") = 11,
            py::arg("max_internal_ids") = 20);
}
