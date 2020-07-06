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

from bip39_dice.dice_mapper import dice_permutations


def test_two_two_sided():
    actual = list(dice_permutations(2, 2))

    expected = [[1, 1], [1, 2], [2, 1], [2, 2]]

    assert actual == expected


def test_two_three_sided():
    actual = list(dice_permutations(2, 3))

    expected = [
        [1, 1],
        [1, 2],
        [1, 3],
        [2, 1],
        [2, 2],
        [2, 3],
        [3, 1],
        [3, 2],
        [3, 3],
    ]

    assert actual == expected
