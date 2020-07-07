#!/usr/bin/env python
import sys

from mnemonic import Mnemonic  # type: ignore

from bip39_dice.checksum_generator import ChecksumGenerator


def main():
    phrase = input("Enter the first N - 1 words, space separated:\n")
    extra_bits = input("Enter the extra M bits (e.g. 011):\n")

    mnemo = Mnemonic("english")

    csg = ChecksumGenerator(ent_phrase=phrase, coin_flips=extra_bits, mnemo=mnemo)

    print("\n" + csg.last_word)


if __name__ == "__main__":
    main()
