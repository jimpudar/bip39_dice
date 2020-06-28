"""Module dealing with BIP-39 logic at the bit level"""
import hashlib

from mnemonic import Mnemonic


def word_to_bitstring(mnemo: Mnemonic, word: str) -> str:
    """Given a BIP-39 word, find it's index and return that as an eleven bit width
    bitstring."""
    index = mnemo.wordlist.index(word)
    if index < 0:
        raise LookupError('Unable to find "%s" in word list.' % word)

    # The format string "011b" means "print number in binary with eleven digits, left
    # padded with zeros".
    eleven_bit_string = format(index, "011b")

    return eleven_bit_string


class ChecksumGenerator:
    # pylint: disable=too-many-instance-attributes
    """An object which can convert entropy from diceware words and coin flips into a
    valid BIP-39 phrase."""

    def __init__(self, ent_phrase: str, coin_flips: str, mnemo: Mnemonic):
        """
        :param ent_phrase: the initial entropy phrase (ENT), space separated. For
        example, when generating a 24 word phrase you need to supply the first 23 words.

        :param coin_flips: a bit string generated by coin flips to represent the
        first N bits of the last word. The last (11 - N) bits is the checksum value.
        All these bits together determine the last word. For example, when generating a
        24 word phrase, the checksum is 8 bits, so the bit string needs to contain 3
        bits.
        """

        self.mnemo = mnemo

        # The phrase should be space separated
        number_of_words = len(ent_phrase.split(" "))

        # See the BIP-39 specification for the allowed lengths (12, 15, 18, 21, 24).
        # Since we are generating the words using dice, the last word is not included
        # in our initial input.
        if number_of_words not in [11, 14, 17, 20, 23]:
            raise ValueError("The entropy phrase isn't the right length")

        # Each word in the phrase is represented by eleven bits. Here we find the total
        # number of bits in the final phrase.
        desired_bits_entropy_plus_checksum = (number_of_words + 1) * 11

        # The initial entropy of a standard BIP-39 phrase is a multiple of 32 bits. The
        # number of checksum bits is however many extra bits on top of that which will
        # bring the total to be divisible by eleven. Thus, we can use integer division
        # to ignore the checksum bits to work backwards and find how many checksum bits
        # there should be.
        self.number_of_checksum_bits = desired_bits_entropy_plus_checksum // 32

        # Logically, the following relations should also hold.
        assert self.number_of_checksum_bits == desired_bits_entropy_plus_checksum % 32
        assert (
            self.number_of_checksum_bits + self.number_of_checksum_bits * 32
            == desired_bits_entropy_plus_checksum
        )

        number_of_coin_flip_bits = 11 - self.number_of_checksum_bits
        if len(coin_flips) != number_of_coin_flip_bits:
            raise ValueError(
                f"The coin flip bitstring isn't the right length"
                f" (expected {number_of_coin_flip_bits})"
            )

        self.ent_phrase = ent_phrase
        self.coin_flips = coin_flips
        self.ent = self.ent_phrase_and_coin_flips_to_bytes()
        self.checksum_bitstring = self.calculate_checksum_bitstring()
        self.last_word = self.calculate_last_word()

        self.phrase = self.ent_phrase + " " + self.last_word

        # As a double check, we can make sure that Mnemonic also came to the same last
        # word as we did.
        assert self.phrase == mnemo.to_mnemonic(self.ent)

    def ent_phrase_and_coin_flips_to_bytes(self) -> bytes:
        """The reverse of what Mnemonic normally does - convert the words (and extra
        bits) into the entropy bytes."""
        bits = ""

        for word in self.ent_phrase.split(" "):
            bits += word_to_bitstring(self.mnemo, word)

        bits += self.coin_flips

        return int(bits, 2).to_bytes(len(bits) // 8, "big")

    def calculate_checksum_bitstring(self) -> str:
        """Use the BIP-39 logic to calculate the checksum bits."""
        # Get the digest of the SHA256 hash as a hexadecimal string
        hex_hash = hashlib.sha256(self.ent).hexdigest()

        # Convert the digest into an integer
        int_hash = int(hex_hash, 16)

        # Convert the digest into a binary bitstring and take the checksum bits from the
        # beginning of the string
        return format(int_hash, "0256b")[: self.number_of_checksum_bits]

    def calculate_last_word(self) -> str:
        """Using the "extra" bits and checksum bits, look up the last word of the
        phrase."""
        # The index of the last word is found by concatenating the coin flips with the
        # checksum. See BIP-39 for the details.
        last_word_index_binary = self.coin_flips + self.checksum_bitstring

        last_word_index = int(last_word_index_binary, 2)

        return self.mnemo.wordlist[last_word_index]
