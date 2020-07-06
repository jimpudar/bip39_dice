# bip39_dice

Tools for generating secure BIP-39 compliant seeds using dice as an entropy source

## Getting Started

First install the requirements:

* Python 3.8 or higher (I recommend the use of
[pyenv](https://github.com/pyenv/pyenv) for managing multiple versions of
Python)
* [Poetry](https://python-poetry.org/)

Next, install the Python dependencies:

```shell script
cd bip39_dice
poetry install
```

## Running Tests

```shell script
cd bip39_dice
poetry run pytest
```

## License

bip39_dice - tools for generating secure BIP-39 compliant seeds using dice
Copyright (C) 2020 Jim Pudar

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as
published by the Free Software Foundation, either version 3 of the
License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.

## OOS Notice

Test vectors have been borrowed from
[python-mnemonic](https://github.com/trezor/python-mnemonic/blob/master/vectors.json)
which is available under the MIT license. These are used only in the unit
tests.

## See Also

* [BIP-39](https://github.com/bitcoin/bips/blob/master/bip-0039.mediawiki)
* [Reference Implementation](https://github.com/trezor/python-mnemonic)
* [Ian Coleman's BIP39 Tool](https://github.com/iancoleman/bip39)