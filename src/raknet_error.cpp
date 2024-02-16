#include <pybind11/pybind11.h>

#include "raknet_error.h"

namespace py = pybind11;

void def_raknet_error(pybind11::module &m) {
    py::register_exception<RakNetError>(m, "RakNetError");
    py::register_exception<StartupError>(m, "StartupError");
}