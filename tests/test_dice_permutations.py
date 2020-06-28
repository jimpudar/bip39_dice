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
