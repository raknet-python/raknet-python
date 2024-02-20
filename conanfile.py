from conan import ConanFile
from conan.tools.cmake import CMakeToolchain, CMake, cmake_layout, CMakeDeps

__version__ = "0.3.0"


class RakNetPythonRecipe(ConanFile):
    name = "raknet-python"
    version = __version__
    package_type = "shared-library"

    # Optional metadata
    license = "BSD-3-Clause"
    url = "https://github.com/wu-vincent/raknet-python"
    homepage = "https://github.com/wu-vincent/raknet-python"
    description = "Python bindings for the RakNet network library"
    topics = ("python", "raknet", "network")

    # Binary configuration
    settings = "os", "compiler", "build_type", "arch"
    options = {}
    default_options = {"raknet/*:shared": False}

    exports_sources = "CMakeLists.txt", "src/*", "include/*"

    def requirements(self):
        self.requires("raknet/4.081")
        self.requires("pybind11/2.11.1")
        # self.test_requires("gtest/1.14.0")

    def layout(self):
        cmake_layout(self)

    def generate(self):
        deps = CMakeDeps(self)
        deps.generate()
        tc = CMakeToolchain(self)
        tc.generate()

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def package(self):
        cmake = CMake(self)
        cmake.install()

    def package_info(self):
        self.cpp_info.requires = ["raknet::raknet", "pybind11::headers"]
