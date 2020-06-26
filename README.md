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

## See Also

* [BIP-39](https://github.com/bitcoin/bips/blob/master/bip-0039.mediawiki)
* [Reference Implementation](https://github.com/trezor/python-mnemonic)
* [Ian Coleman's BIP39 Tool](https://github.com/iancoleman/bip39)