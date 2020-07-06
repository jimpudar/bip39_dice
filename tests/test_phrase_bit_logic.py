# bip39_dice - tools for generating secure BIP-39 compliant seeds using dice
# Copyright (C) 2020 Jim Pudar
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import json
import pathlib
from typing import Iterable, List

import pytest  # type: ignore
from mnemonic import Mnemonic  # type: ignore

from bip39_dice.checksum_generator import ChecksumGenerator, word_to_bitstring


class MnemonicVector:
    def __init__(self, vector: List[str]):
        self.input_entropy_hex = vector[0]
        self.mnemonic_phrase = vector[1]

    def input_entropy_bytes(self) -> bytes:
        return bytes.fromhex(self.input_entropy_hex)

    def phrase_without_checksum_word(self) -> str:
        words = self.mnemonic_phrase.split(" ")

        return " ".join(words[0:-1])

    def last_word(self) -> str:
        words = self.mnemonic_phrase.split(" ")

        return words[-1]

    def coin_flips_bitstring(self) -> str:
        """Finds the bits of the last word which belong to the initial entropy"""

        number_of_coin_flip_bits_by_number_of_entropy_bits = {
            128: 11 - 4,
            160: 11 - 5,
            192: 11 - 6,
            224: 11 - 7,
            256: 11 - 8,
        }

        number_of_entropy_bits = len(self.input_entropy_bytes()) * 8

        number_of_coin_flip_bits = number_of_coin_flip_bits_by_number_of_entropy_bits[
            number_of_entropy_bits
        ]

        ent_bits = format(
            int(self.input_entropy_hex, 16), f"0{number_of_entropy_bits}b"
        )

        coin_flip_bitsring = ent_bits[-number_of_coin_flip_bits:]

        return coin_flip_bitsring


@pytest.fixture()
def mnemo() -> Mnemonic:
    return Mnemonic("english")


@pytest.fixture()
def english_vectors() -> Iterable[MnemonicVector]:
    filename = pathlib.Path(__file__).resolve().parent / "test_data" / "vectors.json"

    with open(filename) as file:
        vectors_by_language = json.loads(file.read())

    raw_vectors = vectors_by_language["english"]

    vectors = []
    for raw_vector in raw_vectors:
        vectors.append(MnemonicVector(raw_vector))

    return vectors


def test_english_word_to_bitstring(mnemo):
    test_words = [
        ["abandon", "00000000000"],
        ["ability", "00000000001"],
        ["agent", "00000100111"],
    ]

    for test_word in test_words:
        actual = word_to_bitstring(mnemo, test_word[0])
        expected = test_word[1]
        assert actual == expected


def test_english_phrase_to_bytearray(mnemo, english_vectors):
    for vector in english_vectors:
        csg = ChecksumGenerator(
            vector.phrase_without_checksum_word(), vector.coin_flips_bitstring(), mnemo
        )

        actual = csg.ent
        expected = vector.input_entropy_bytes()
        assert actual == expected


def test_last_word(mnemo, english_vectors):
    for vector in english_vectors:
        csg = ChecksumGenerator(
            vector.phrase_without_checksum_word(), vector.coin_flips_bitstring(), mnemo
        )

        actual = csg.last_word
        expected = vector.last_word()
        # bip39_dice - tools for generating secure BIP-39 compliant seeds using dice
        # Copyright (C) 2020 Jim Pudar
        #
        # This program is free software: you can redistribute it and/or modify
        # it under the terms of the GNU Affero General Public License as
        # published by the Free Software Foundation, either version 3 of the
        # License, or (at your option) any later version.
        #
        # This program is distributed in the hope that it will be useful,
        # but WITHOUT ANY WARRANTY; without even the implied warranty of
        # MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
        # GNU Affero General Public License for more details.
        #
        # You should have received a copy of the GNU Affero General Public License
        # along with this program.  If not, see <https://www.gnu.org/licenses/>.

        assert actual == expected
