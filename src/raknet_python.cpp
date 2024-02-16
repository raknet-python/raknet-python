#include <pybind11/pybind11.h>

#include "rak_peer.h"

PYBIND11_MODULE(raknet_python, m) {
    def_raknet_error(m);
    def_rak_peer(m);
}
