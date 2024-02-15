#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

#include "rak_peer.h"

#include <raknet/RakPeer.h>
#include <raknet/RakPeerInterface.h>

namespace py = pybind11;

void def_rak_peer(pybind11::module &m) {
    py::class_<RakNet::RakPeer>(m, "RakPeer")
        .def(py::init<>())
        .def(
            "start",
            [](RakNet::RakPeerInterface &a, const char *host, int port, int max_connections) {
                auto local_addr = RakNet::SocketDescriptor(port, host);
                a.Startup(max_connections, &local_addr, 1);
            },
            py::arg("host") = py::none(),
            py::arg("port") = 0,
            py::arg("max_connections") = 1);
}
