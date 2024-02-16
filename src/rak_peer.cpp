#include <pybind11/pybind11.h>

#include "rak_peer.h"

#include <raknet/RakNetTypes.h>
#include <raknet/RakPeer.h>
#include <raknet/RakPeerInterface.h>

namespace py = pybind11;

void def_rak_peer(pybind11::module &m) {
    py::class_<RakNet::RakPeer>(m, "RakPeer")
        .def(py::init<>())
        .def(
            "startup",
            [](RakNet::RakPeer &a,
               const char *host,
               int port,
               int max_connections,
               int protocol_version,
               int max_internal_ids) {
                auto local_addr = RakNet::SocketDescriptor(port, host);
                a.Startup(max_connections, &local_addr, 1, -99999, protocol_version, max_internal_ids);
            },
            py::arg("host") = py::none(),
            py::arg("port") = 0,
            py::arg("max_connections") = 1,
            py::arg("protocol_version") = 11,
            py::arg("max_internal_ids") = 20);
}
