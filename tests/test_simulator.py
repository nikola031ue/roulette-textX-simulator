import pytest
from roulette.interpreter import Roulet


class MockNumberBet:
    def __init__(self, n):
        self.number = n
        self.__class__.__name__ = 'NumberBet'


class MockColorBet:
    def __init__(self, c):
        self.color = c
        self.__class__.__name__ = 'ColorBet'


class MockParityBet:
    def __init__(self, p):
        self.parity = p
        self.__class__.__name__ = 'ParityBet'


class MockRangeBet:
    def __init__(self, r):
        self.range = r
        self.__class__.__name__ = 'RangeBet'


class MockDozenBet:
    def __init__(self, d):
        self.dozen = d
        self.__class__.__name__ = 'DozenBet'


class MockColumnBet:
    def __init__(self, c):
        self.column = c
        self.__class__.__name__ = 'ColumnBet'


class MockSplitBet:
    def __init__(self, nums):
        self.numbers = nums
        self.__class__.__name__ = 'SplitBet'


class MockStreetBet:
    def __init__(self, nums):
        self.numbers = nums
        self.__class__.__name__ = 'StreetBet'


class MockCornerBet:
    def __init__(self, nums):
        self.numbers = nums
        self.__class__.__name__ = 'CornerBet'


class MockSixLineBet:
    def __init__(self, nums):
        self.numbers = nums
        self.__class__.__name__ = 'SixLineBet'


class MockBasketBet:
    def __init__(self):
        self.__class__.__name__ = 'BasketBet'


@pytest.fixture
def roulet():
    return Roulet()


# ==========================
# NUMBER BET TESTS
# ==========================


def test_number_bet_win(roulet):
    bet = MockNumberBet(7)
    result = roulet.calculate_payout(bet, 10, 7)
    assert result == 360


def test_number_bet_loss(roulet):
    bet = MockNumberBet(7)
    result = roulet.calculate_payout(bet, 10, 8)
    assert result == 0


def test_number_bet_zero_win(roulet):
    bet = MockNumberBet(0)
    result = roulet.calculate_payout(bet, 5, 0)
    assert result == 180


# ==========================
# COLOR BET TESTS
# ==========================


def test_color_bet_red_win(roulet):
    bet = MockColorBet('red')
    result = roulet.calculate_payout(bet, 20, 1)  # 1 is red
    assert result == 40


def test_color_bet_red_loss_on_black(roulet):
    bet = MockColorBet('red')
    result = roulet.calculate_payout(bet, 20, 2)  # 2 is black
    assert result == 0


def test_color_bet_red_loss_on_zero(roulet):
    bet = MockColorBet('red')
    result = roulet.calculate_payout(bet, 20, 0)
    assert result == 0


def test_color_bet_black_win(roulet):
    bet = MockColorBet('black')
    result = roulet.calculate_payout(bet, 25, 2)  # 2 is black
    assert result == 50


def test_color_bet_black_loss_on_red(roulet):
    bet = MockColorBet('black')
    result = roulet.calculate_payout(bet, 25, 1)  # 1 is red
    assert result == 0


def test_color_bet_black_loss_on_zero(roulet):
    bet = MockColorBet('black')
    result = roulet.calculate_payout(bet, 25, 0)
    assert result == 0


# ==========================
# PARITY BET TESTS
# ==========================


def test_parity_bet_even_win(roulet):
    bet = MockParityBet('even')
    result = roulet.calculate_payout(bet, 15, 4)
    assert result == 30


def test_parity_bet_even_loss_on_odd(roulet):
    bet = MockParityBet('even')
    result = roulet.calculate_payout(bet, 15, 3)
    assert result == 0


def test_parity_bet_even_loss_on_zero(roulet):
    bet = MockParityBet('even')
    result = roulet.calculate_payout(bet, 15, 0)
    assert result == 0


def test_parity_bet_odd_win(roulet):
    bet = MockParityBet('odd')
    result = roulet.calculate_payout(bet, 20, 5)
    assert result == 40


def test_parity_bet_odd_loss_on_even(roulet):
    bet = MockParityBet('odd')
    result = roulet.calculate_payout(bet, 20, 6)
    assert result == 0


def test_parity_bet_odd_loss_on_zero(roulet):
    bet = MockParityBet('odd')
    result = roulet.calculate_payout(bet, 20, 0)
    assert result == 0


# ==========================
# RANGE BET TESTS
# ==========================


def test_range_bet_low_win(roulet):
    bet = MockRangeBet('low')
    result = roulet.calculate_payout(bet, 30, 18)
    assert result == 60


def test_range_bet_low_loss_on_high(roulet):
    bet = MockRangeBet('low')
    result = roulet.calculate_payout(bet, 30, 19)
    assert result == 0


def test_range_bet_low_loss_on_zero(roulet):
    bet = MockRangeBet('low')
    result = roulet.calculate_payout(bet, 30, 0)
    assert result == 0


def test_range_bet_high_win(roulet):
    bet = MockRangeBet('high')
    result = roulet.calculate_payout(bet, 40, 36)
    assert result == 80


def test_range_bet_high_loss_on_low(roulet):
    bet = MockRangeBet('high')
    result = roulet.calculate_payout(bet, 40, 1)
    assert result == 0


def test_range_bet_high_loss_on_zero(roulet):
    bet = MockRangeBet('high')
    result = roulet.calculate_payout(bet, 40, 0)
    assert result == 0


# ==========================
# DOZEN BET TESTS
# ==========================


def test_dozen_bet_1_win(roulet):
    bet = MockDozenBet(1)
    result = roulet.calculate_payout(bet, 10, 12)
    assert result == 30


def test_dozen_bet_1_loss(roulet):
    bet = MockDozenBet(1)
    result = roulet.calculate_payout(bet, 10, 13)
    assert result == 0


def test_dozen_bet_2_win(roulet):
    bet = MockDozenBet(2)
    result = roulet.calculate_payout(bet, 15, 18)
    assert result == 45


def test_dozen_bet_2_loss(roulet):
    bet = MockDozenBet(2)
    result = roulet.calculate_payout(bet, 15, 25)
    assert result == 0


def test_dozen_bet_3_win(roulet):
    bet = MockDozenBet(3)
    result = roulet.calculate_payout(bet, 20, 36)
    assert result == 60


def test_dozen_bet_3_loss(roulet):
    bet = MockDozenBet(3)
    result = roulet.calculate_payout(bet, 20, 24)
    assert result == 0


def test_dozen_bet_loss_on_zero(roulet):
    bet = MockDozenBet(1)
    result = roulet.calculate_payout(bet, 10, 0)
    assert result == 0


# ==========================
# COLUMN BET TESTS
# ==========================


def test_column_bet_1_win(roulet):
    bet = MockColumnBet(1)
    result = roulet.calculate_payout(bet, 10, 1)
    assert result == 30


def test_column_bet_1_loss(roulet):
    bet = MockColumnBet(1)
    result = roulet.calculate_payout(bet, 10, 2)
    assert result == 0


def test_column_bet_2_win(roulet):
    bet = MockColumnBet(2)
    result = roulet.calculate_payout(bet, 15, 2)
    assert result == 45


def test_column_bet_2_loss(roulet):
    bet = MockColumnBet(2)
    result = roulet.calculate_payout(bet, 15, 3)
    assert result == 0


def test_column_bet_3_win(roulet):
    bet = MockColumnBet(3)
    result = roulet.calculate_payout(bet, 20, 3)
    assert result == 60


def test_column_bet_3_loss(roulet):
    bet = MockColumnBet(3)
    result = roulet.calculate_payout(bet, 20, 1)
    assert result == 0


def test_column_bet_loss_on_zero(roulet):
    bet = MockColumnBet(1)
    result = roulet.calculate_payout(bet, 10, 0)
    assert result == 0


# ==========================
# SPLIT BET TESTS
# ==========================


def test_split_bet_win(roulet):
    bet = MockSplitBet([1, 2])
    result = roulet.calculate_payout(bet, 10, 2)
    assert result == 180


def test_split_bet_loss(roulet):
    bet = MockSplitBet([1, 2])
    result = roulet.calculate_payout(bet, 10, 3)
    assert result == 0


# ==========================
# STREET BET TESTS
# ==========================


def test_street_bet_win(roulet):
    bet = MockStreetBet([1, 2, 3])
    result = roulet.calculate_payout(bet, 10, 2)
    assert result == 120


def test_street_bet_loss(roulet):
    bet = MockStreetBet([1, 2, 3])
    result = roulet.calculate_payout(bet, 10, 4)
    assert result == 0


# ==========================
# CORNER BET TESTS
# ==========================


def test_corner_bet_win(roulet):
    bet = MockCornerBet([1, 2, 4, 5])
    result = roulet.calculate_payout(bet, 10, 5)
    assert result == 90


def test_corner_bet_loss(roulet):
    bet = MockCornerBet([1, 2, 4, 5])
    result = roulet.calculate_payout(bet, 10, 3)
    assert result == 0


# ==========================
# SIX LINE BET TESTS
# ==========================


def test_sixline_bet_win(roulet):
    bet = MockSixLineBet([1, 2, 3, 4, 5, 6])
    result = roulet.calculate_payout(bet, 10, 4)
    assert result == 60


def test_sixline_bet_loss(roulet):
    bet = MockSixLineBet([1, 2, 3, 4, 5, 6])
    result = roulet.calculate_payout(bet, 10, 7)
    assert result == 0


# ==========================
# BASKET BET TESTS
# ==========================


def test_basket_bet_win_on_zero(roulet):
    bet = MockBasketBet()
    result = roulet.calculate_payout(bet, 10, 0)
    assert result == 70


def test_basket_bet_win_on_one(roulet):
    bet = MockBasketBet()
    result = roulet.calculate_payout(bet, 10, 1)
    assert result == 70


def test_basket_bet_win_on_two(roulet):
    bet = MockBasketBet()
    result = roulet.calculate_payout(bet, 10, 2)
    assert result == 70


def test_basket_bet_win_on_three(roulet):
    bet = MockBasketBet()
    result = roulet.calculate_payout(bet, 10, 3)
    assert result == 70


def test_basket_bet_loss(roulet):
    bet = MockBasketBet()
    result = roulet.calculate_payout(bet, 10, 4)
    assert result == 0
