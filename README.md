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

## Generating a Passphrase

**WARNING**: BIP-39 is discouraged because the passphrases contain no version
number. This means that if the logic that converts the secret phrase into coin
root key ever changes, it may become difficult to recover your coins. Given
that hardware wallets such as Trezor use BIP-39, I personally think this is
unlikely to be a problem. However, do your own research before going ahead
with this mechanism!

Typically a hardware wallet such as a Trezor will generate a passphrase by
first generating a random sequence of bytes, calculating the checksum, and
_then_ converting it to the mnemonic phrase.

Since we want to use [diceware](https://theworld.com/~reinhold/diceware.html)
style entropy to generate our passphrase rather than relying on the hardware
RNG in our hardware wallet, we are going to be going the other way around -
we will generate the initial N-1 words in our N word passphrase and _then_
convert it back to the bytes that can be used to generate the checksum.

### Choose a Passphrase Length

The valid lengths for BIP-39 mnemonic passphrases are 12, 15, 18, 21, and 24
words. Choose one of these numbers. We will refer to this number as `N`.

### Generate or Find a Dice -> Word Mapping

This project includes a utility for generating the dice roll -> wordlist
mapping, although some other such mappings already exist on the Internet.

* <https://github.com/dnixty/BIP39-diceware>
* <https://github.com/taelfrinn/Bip39-diceware>

### Roll the Dice and Flip the Coin

We now need to choose `N - 1` words using the dice -> word mapping and some
additional bits of entropy to make up the beginning of the last word.

Roll the dice and record each word on a sheet of paper. Do not type them into
a computer, and do not take any digital photographs of them!

Once you have `N - 1` words, we need to flip a coin `M` times and record the
results. For heads, record a `1`. For tails, record a `0`. These remaining `M`
bits will be the first `M` bits of the last word in the mnemonic phrase and
the last `M` bits of the initial `ENT` bits of entropy.

```text
|  N | M |
+----+---+
| 12 | 7 |
| 15 | 6 |
| 18 | 5 |
| 21 | 4 |
| 24 | 3 |
```

For example, if you have flipped the coin three times and gotten heads, tails,
heads, your bit string should look like `"101"`.

### Run the Script

The script is designed in such a way that your passphrase never needs to be
written to disk, but since the phrase will still be typed into the computer
and written into RAM you need to be very careful where you execute it.

My personal recommendation is to get a cheap Raspberry Pi computer, install a
fresh copy of Rasbian, install all the requirements and this software, and
then completely disconnect it from the Internet before running the script.
After power cycling the Raspberry Pi, and wiping the SD card, it should be
safe to connect it to the Internet again.

Once you are on a non-networked machine, run `find_checksum.py` and follow
the prompts. The final checksum word will be printed to STDOUT. For example:

```text
% python find_checksum.py
Enter the first N - 1 words, space separated:
zoo zoo zoo zoo zoo zoo zoo zoo zoo zoo zoo
Enter the extra M bits (e.g. 011):
1100110

snap
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