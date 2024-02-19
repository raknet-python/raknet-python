# raknet-python

[![Build](https://github.com/wu-vincent/raknet-python/actions/workflows/build.yml/badge.svg)](https://github.com/wu-vincent/raknet-python/actions/workflows/build.yml)
[![Read the Docs](https://img.shields.io/readthedocs/raknet-python)](https://raknet-python.readthedocs.io/en/latest/)
[![PyPI - Version](https://img.shields.io/pypi/v/raknet?logo=python&logoColor=white)](https://pypi.org/project/raknet/)
![GitHub License](https://img.shields.io/github/license/raknet-python/raknet-python)
![Python](https://img.shields.io/badge/Python-3-blue)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

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
