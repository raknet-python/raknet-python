# raknet-python

[![Build](https://github.com/wu-vincent/raknet-python/actions/workflows/build.yml/badge.svg)](https://github.com/wu-vincent/raknet-python/actions/workflows/build.yml)
![PyPI - Version](https://img.shields.io/pypi/v/raknet)
![PyPI - License](https://img.shields.io/pypi/l/raknet)

Python bindings for the [RakNet](https://github.com/facebookarchive/RakNet) networking library

## 🛠 Installation

### 📦 From PyPi

```bash
pip install raknet
```

or

### 🎯 Build locally

```shell
git clone https://github.com/wu-vincent/raknet-python.git
cd raknet-python
pip install conan
conan export raknet --version 4.081
conan install . --build=missing -c tools.cmake.cmaketoolchain:generator=Ninja
pip install .
```

## 🚀 Usage

We are working on making this project ready and will drop the usage documentation soon. Stay tuned! ⏳