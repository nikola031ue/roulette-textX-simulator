import pytest
from roulette.interpreter import Roulet


class MockBalanceCondition:
    def __init__(self, operator, amount):
        self.operator = operator
        self.amount = amount
        self.__class__.__name__ = 'BalanceCondition'


class MockConsecutiveWins:
    def __init__(self, operator, count):
        self.operator = operator
        self.count = count
        self.__class__.__name__ = 'ConsecutiveWins'


class MockConsecutiveLosses:
    def __init__(self, operator, count):
        self.operator = operator
        self.count = count
        self.__class__.__name__ = 'ConsecutiveLosses'


class MockRoundProfitCondition:
    def __init__(self, operator, amount):
        self.operator = operator
        self.amount = amount
        self.__class__.__name__ = 'RoundProfitCondition'


class MockCompoundCondition:
    def __init__(self, left, logic_op, right):
        self.left = left
        self.logic_op = logic_op
        self.right = right
        self.__class__.__name__ = 'CompoundCondition'


@pytest.fixture
def roulet():
    return Roulet()


# ==========================
# BALANCE CONDITION TESTS
# ==========================


def test_balance_greater_than_true(roulet):
    roulet.balance = 200
    cond = MockBalanceCondition('>', 100)
    assert roulet.evaluate_condition(cond) is True


def test_balance_greater_than_false(roulet):
    roulet.balance = 50
    cond = MockBalanceCondition('>', 100)
    assert roulet.evaluate_condition(cond) is False


def test_balance_less_than_true(roulet):
    roulet.balance = 50
    cond = MockBalanceCondition('<', 100)
    assert roulet.evaluate_condition(cond) is True


def test_balance_less_than_false(roulet):
    roulet.balance = 200
    cond = MockBalanceCondition('<', 100)
    assert roulet.evaluate_condition(cond) is False


def test_balance_greater_equal_true_greater(roulet):
    roulet.balance = 200
    cond = MockBalanceCondition('>=', 100)
    assert roulet.evaluate_condition(cond) is True


def test_balance_greater_equal_true_equal(roulet):
    roulet.balance = 100
    cond = MockBalanceCondition('>=', 100)
    assert roulet.evaluate_condition(cond) is True


def test_balance_greater_equal_false(roulet):
    roulet.balance = 50
    cond = MockBalanceCondition('>=', 100)
    assert roulet.evaluate_condition(cond) is False


def test_balance_less_equal_true_less(roulet):
    roulet.balance = 50
    cond = MockBalanceCondition('<=', 100)
    assert roulet.evaluate_condition(cond) is True


def test_balance_less_equal_true_equal(roulet):
    roulet.balance = 100
    cond = MockBalanceCondition('<=', 100)
    assert roulet.evaluate_condition(cond) is True


def test_balance_less_equal_false(roulet):
    roulet.balance = 200
    cond = MockBalanceCondition('<=', 100)
    assert roulet.evaluate_condition(cond) is False


def test_balance_equal_true(roulet):
    roulet.balance = 100
    cond = MockBalanceCondition('==', 100)
    assert roulet.evaluate_condition(cond) is True


def test_balance_equal_false(roulet):
    roulet.balance = 50
    cond = MockBalanceCondition('==', 100)
    assert roulet.evaluate_condition(cond) is False


def test_balance_not_equal_true(roulet):
    roulet.balance = 50
    cond = MockBalanceCondition('!=', 100)
    assert roulet.evaluate_condition(cond) is True


def test_balance_not_equal_false(roulet):
    roulet.balance = 100
    cond = MockBalanceCondition('!=', 100)
    assert roulet.evaluate_condition(cond) is False


def test_balance_zero(roulet):
    roulet.balance = 0
    cond = MockBalanceCondition('==', 0)
    assert roulet.evaluate_condition(cond) is True


# ==========================
# CONSECUTIVE WINS TESTS
# ==========================


def test_consecutive_wins_greater_true(roulet):
    roulet.consecutive_wins = 5
    cond = MockConsecutiveWins('>', 3)
    assert roulet.evaluate_condition(cond) is True


def test_consecutive_wins_greater_false(roulet):
    roulet.consecutive_wins = 2
    cond = MockConsecutiveWins('>', 3)
    assert roulet.evaluate_condition(cond) is False


def test_consecutive_wins_equal_true(roulet):
    roulet.consecutive_wins = 3
    cond = MockConsecutiveWins('==', 3)
    assert roulet.evaluate_condition(cond) is True


def test_consecutive_wins_zero(roulet):
    roulet.consecutive_wins = 0
    cond = MockConsecutiveWins('==', 0)
    assert roulet.evaluate_condition(cond) is True


# ==========================
# CONSECUTIVE LOSSES TESTS
# ==========================


def test_consecutive_losses_greater_true(roulet):
    roulet.consecutive_losses = 5
    cond = MockConsecutiveLosses('>', 3)
    assert roulet.evaluate_condition(cond) is True


def test_consecutive_losses_greater_false(roulet):
    roulet.consecutive_losses = 2
    cond = MockConsecutiveLosses('>', 3)
    assert roulet.evaluate_condition(cond) is False


def test_consecutive_losses_equal_true(roulet):
    roulet.consecutive_losses = 3
    cond = MockConsecutiveLosses('==', 3)
    assert roulet.evaluate_condition(cond) is True


def test_consecutive_losses_zero(roulet):
    roulet.consecutive_losses = 0
    cond = MockConsecutiveLosses('==', 0)
    assert roulet.evaluate_condition(cond) is True


# ==========================
# ROUND PROFIT CONDITION TESTS
# ==========================


def test_round_profit_greater_true(roulet):
    roulet.round_profit = 50
    cond = MockRoundProfitCondition('>', 0)
    assert roulet.evaluate_condition(cond) is True


def test_round_profit_less_true(roulet):
    roulet.round_profit = -20
    cond = MockRoundProfitCondition('<', 0)
    assert roulet.evaluate_condition(cond) is True


def test_round_profit_equal_zero(roulet):
    roulet.round_profit = 0
    cond = MockRoundProfitCondition('==', 0)
    assert roulet.evaluate_condition(cond) is True


def test_round_profit_not_equal(roulet):
    roulet.round_profit = 100
    cond = MockRoundProfitCondition('!=', 0)
    assert roulet.evaluate_condition(cond) is True


def test_round_profit_greater_equal(roulet):
    roulet.round_profit = 0
    cond = MockRoundProfitCondition('>=', 0)
    assert roulet.evaluate_condition(cond) is True


def test_round_profit_less_equal(roulet):
    roulet.round_profit = -10
    cond = MockRoundProfitCondition('<=', 0)
    assert roulet.evaluate_condition(cond) is True


# ==========================
# COMPOUND CONDITION TESTS
# ==========================


def test_compound_and_both_true(roulet):
    roulet.balance = 200
    roulet.consecutive_wins = 5
    left = MockBalanceCondition('>', 100)
    right = MockConsecutiveWins('>', 3)
    cond = MockCompoundCondition(left, 'and', right)
    assert roulet.evaluate_condition(cond) is True


def test_compound_and_left_false(roulet):
    roulet.balance = 50
    roulet.consecutive_wins = 5
    left = MockBalanceCondition('>', 100)
    right = MockConsecutiveWins('>', 3)
    cond = MockCompoundCondition(left, 'and', right)
    assert roulet.evaluate_condition(cond) is False


def test_compound_and_right_false(roulet):
    roulet.balance = 200
    roulet.consecutive_wins = 1
    left = MockBalanceCondition('>', 100)
    right = MockConsecutiveWins('>', 3)
    cond = MockCompoundCondition(left, 'and', right)
    assert roulet.evaluate_condition(cond) is False


def test_compound_and_both_false(roulet):
    roulet.balance = 50
    roulet.consecutive_wins = 1
    left = MockBalanceCondition('>', 100)
    right = MockConsecutiveWins('>', 3)
    cond = MockCompoundCondition(left, 'and', right)
    assert roulet.evaluate_condition(cond) is False


def test_compound_or_both_true(roulet):
    roulet.balance = 200
    roulet.consecutive_losses = 5
    left = MockBalanceCondition('>', 100)
    right = MockConsecutiveLosses('>', 3)
    cond = MockCompoundCondition(left, 'or', right)
    assert roulet.evaluate_condition(cond) is True


def test_compound_or_left_true(roulet):
    roulet.balance = 200
    roulet.consecutive_losses = 1
    left = MockBalanceCondition('>', 100)
    right = MockConsecutiveLosses('>', 3)
    cond = MockCompoundCondition(left, 'or', right)
    assert roulet.evaluate_condition(cond) is True


def test_compound_or_right_true(roulet):
    roulet.balance = 50
    roulet.consecutive_losses = 5
    left = MockBalanceCondition('>', 100)
    right = MockConsecutiveLosses('>', 3)
    cond = MockCompoundCondition(left, 'or', right)
    assert roulet.evaluate_condition(cond) is True


def test_compound_or_both_false(roulet):
    roulet.balance = 50
    roulet.consecutive_losses = 1
    left = MockBalanceCondition('>', 100)
    right = MockConsecutiveLosses('>', 3)
    cond = MockCompoundCondition(left, 'or', right)
    assert roulet.evaluate_condition(cond) is False


def test_compound_nested_and_or(roulet):
    roulet.balance = 200
    roulet.consecutive_wins = 2
    roulet.consecutive_losses = 5
    inner_left = MockBalanceCondition('>', 100)
    inner_right = MockConsecutiveWins('>', 3)
    inner = MockCompoundCondition(inner_left, 'and', inner_right)
    outer_right = MockConsecutiveLosses('>', 3)
    cond = MockCompoundCondition(inner, 'or', outer_right)
    assert roulet.evaluate_condition(cond) is True


def test_compound_nested_or_and(roulet):
    roulet.balance = 50
    roulet.consecutive_wins = 5
    roulet.consecutive_losses = 1
    inner_left = MockBalanceCondition('>', 100)
    inner_right = MockConsecutiveWins('>', 3)
    inner = MockCompoundCondition(inner_left, 'or', inner_right)
    outer_right = MockConsecutiveLosses('>', 3)
    cond = MockCompoundCondition(inner, 'and', outer_right)
    assert roulet.evaluate_condition(cond) is False


# ==========================
# EDGE CASE TESTS
# ==========================


def test_boundary_balance_equal(roulet):
    roulet.balance = 100
    cond = MockBalanceCondition('==', 100)
    assert roulet.evaluate_condition(cond) is True


def test_boundary_balance_greater_equal(roulet):
    roulet.balance = 100
    cond = MockBalanceCondition('>=', 100)
    assert roulet.evaluate_condition(cond) is True


def test_boundary_balance_less_equal(roulet):
    roulet.balance = 100
    cond = MockBalanceCondition('<=', 100)
    assert roulet.evaluate_condition(cond) is True


def test_negative_round_profit(roulet):
    roulet.round_profit = -50
    cond = MockRoundProfitCondition('<', -10)
    assert roulet.evaluate_condition(cond) is True


def test_large_values(roulet):
    roulet.balance = 1000000
    cond = MockBalanceCondition('>', 999999)
    assert roulet.evaluate_condition(cond) is True


def test_zero_consecutive_wins_not_equal(roulet):
    roulet.consecutive_wins = 0
    cond = MockConsecutiveWins('!=', 0)
    assert roulet.evaluate_condition(cond) is False


def test_zero_consecutive_losses_not_equal(roulet):
    roulet.consecutive_losses = 0
    cond = MockConsecutiveLosses('!=', 0)
    assert roulet.evaluate_condition(cond) is False


def test_balance_less_than_zero(roulet):
    roulet.balance = -10
    cond = MockBalanceCondition('<', 0)
    assert roulet.evaluate_condition(cond) is True


def test_round_profit_exact_boundary(roulet):
    roulet.round_profit = 100
    cond = MockRoundProfitCondition('>=', 100)
    assert roulet.evaluate_condition(cond) is True
    cond2 = MockRoundProfitCondition('<=', 100)
    assert roulet.evaluate_condition(cond2) is True
