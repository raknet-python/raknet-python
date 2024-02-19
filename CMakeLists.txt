cmake_minimum_required(VERSION 3.15)
project(raknet_python)


add_compile_definitions(PYBIND11_DETAILED_ERROR_MESSAGES)


find_package(Python COMPONENTS Interpreter Development.Module REQUIRED)
find_package(pybind11 CONFIG REQUIRED)
find_package(raknet CONFIG REQUIRED)


file(GLOB_RECURSE RAKNET_PYTHON_SOURCE_FILES CONFIGURE_DEPENDS "src/*.cpp")
pybind11_add_module(raknet_python MODULE ${RAKNET_PYTHON_SOURCE_FILES})
target_include_directories(raknet_python PUBLIC include)
target_link_libraries(raknet_python PRIVATE raknet::raknet)
set_target_properties(raknet_python PROPERTIES OUTPUT_NAME _raknet)
include(GNUInstallDirs)
install(TARGETS raknet_python DESTINATION raknet/ COMPONENT python OPTIONAL)
