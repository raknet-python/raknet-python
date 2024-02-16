#pragma once

#include <pybind11/pybind11.h>

#include <exception>

struct RakNetError : public std::exception {
    using std::exception::exception;
};

struct StartupError : public RakNetError {
    using RakNetError::RakNetError;
};