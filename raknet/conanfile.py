import os

from conan import ConanFile
from conan.tools.cmake import CMake, CMakeDeps, CMakeToolchain, cmake_layout
from conan.tools.files import apply_conandata_patches, copy, export_conandata_patches, get

required_conan_version = ">=1.53.0"


class RakNetConan(ConanFile):
    name = "raknet"
    description = "RakNet is a cross platform, open source, C++ networking engine for game programmers."
    license = "BSD-2-Clause"
    url = "https://github.com/wu-vincent/raknet-python"
    homepage = "https://github.com/facebookarchive/RakNet"
    topics = ("raknet", "network", "game")
    package_type = "library"
    settings = "os", "arch", "compiler", "build_type"
    options = {
        "shared": [True, False],
        "fPIC": [True, False],
    }
    default_options = {
        "shared": False,
        "fPIC": True,
    }

    def export_sources(self):
        export_conandata_patches(self)

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    def configure(self):
        if self.options.shared:
            self.options.rm_safe("fPIC")

    def layout(self):
        cmake_layout(self, src_folder="src")

    def source(self):
        get(self, **self.conan_data["sources"][self.version], strip_root=True)

    def generate(self):
        tc = CMakeToolchain(self)
        tc.variables["RAKNET_ENABLE_SAMPLES"] = False
        tc.variables["RAKNET_ENABLE_DLL"] = self.options.shared
        tc.variables["RAKNET_ENABLE_STATIC"] = not self.options.shared
        tc.variables["RAKNET_GENERATE_INCLUDE_ONLY_DIR"] = True
        tc.generate()
        tc = CMakeDeps(self)
        tc.generate()

    def build(self):
        apply_conandata_patches(self)
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def package(self):
        copy(self, "LICENSE", self.source_folder, os.path.join(self.package_folder, "licenses"))
        cmake = CMake(self)
        cmake.install()

    def package_info(self):
        if self.options.shared:
            self.cpp_info.libs = ["raknet"]
        else:
            self.cpp_info.libs = ["raknet-static"]

        self.cpp_info.set_property("cmake_file_name", "raknet")
        self.cpp_info.set_property("cmake_target_name", "raknet::raknet")

        if self.settings.os in ["Linux", "FreeBSD"]:
            self.cpp_info.system_libs.append("pthread")
        elif self.settings.os == "Windows":
            self.cpp_info.system_libs.append("ws2_32")

        # TODO: to remove in conan v2 once cmake_find_package_* generators removed
        self.cpp_info.names["cmake_find_package"] = "raknet"
        self.cpp_info.names["cmake_find_package_multi"] = "raknet"
