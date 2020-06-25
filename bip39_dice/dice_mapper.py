"""Dice related functionality"""

from math import ceil, floor, log
from typing import Iterator, List

# Remove type: ignore when type information is published in (?) v0.20
from mnemonic import Mnemonic  # type: ignore


class DiceMapper:
    # pylint: disable=too-few-public-methods
    """Generates the mapping from dice roll to BIP-39 word for arbitrary dice."""

    def __init__(self, sides: int = 6, language: str = "english"):
        self.mnemo = Mnemonic(language)

        self.sides = sides
        self.number_of_dice = self._number_of_dice(sides)

    def print_mapped_wordlist(self) -> None:
        """Print the word list mapped to the current type of dice to STDOUT."""

        iterator = dice_permutations(self.number_of_dice, self.sides)

        for word in self.mnemo.wordlist:
            print(f"{self._format_permutation(next(iterator))}: {word}")

    def _number_of_dice(self, sides: int) -> int:
        """Calculates how many dice are required to cover the entire word list.

        The number of permutations is (sides ** number_of_dice). Since we need to find
        the minimum number of dice which will cover the entire word list, we can use the
        log function to find the exponent value and round up.
        """

        total_words = self.mnemo.radix
        return ceil(log(total_words, sides))

    def _format_permutation(self, permutation: List[int]) -> str:
        """Turn a permutation list into a string for printing to the console."""

        # this isn't perfect because of floating point math but I don't think anybody is
        # going to need 1000 sided dice
        digits = floor(log(self.sides, 10)) + 1

        return " ".join(map(lambda n: f"{str(n):>{digits}}", permutation))


def dice_permutations(number_of_dice: int, sides: int) -> Iterator[List[int]]:
    """Generates the possible permutations of a set of dice in order.

    For example, with two six-sided dice this generator will produce lists [1, 1],
    [1, 2], [1, 3], ... [5, 6], [6, 6].
    """
    current = [1] * number_of_dice

    while True:
        yield current.copy()

        iterated = False

        # Start at the rightmost digit
        digit_index = number_of_dice - 1

        while not iterated:
            if current == [sides] * number_of_dice:
                return

            if current[digit_index] < sides:
                current[digit_index] += 1
                iterated = True
            else:
                current[digit_index] = 1
                digit_index -= 1
