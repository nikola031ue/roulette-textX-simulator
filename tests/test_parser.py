import pytest
import os
from textx import metamodel_from_file, TextXSyntaxError
from roulette.interpreter import Roulet

GRAMMAR = os.path.join(os.path.dirname(__file__), '..', 'roulette', 'grammar.tx')


@pytest.fixture
def mm():
    return metamodel_from_file(GRAMMAR)


# ==========================
# VALID PARSING TESTS
# ==========================


def test_basic_bankroll(mm):
    model = mm.model_from_str("bankroll 500")
    assert model.statements[0].amount == 500


def test_bet_number(mm):
    model = mm.model_from_str("bankroll 100\nbet number 17 25\nspin")
    bet = model.statements[1]
    assert bet.bet_type.__class__.__name__ == 'NumberBet'
    assert bet.bet_type.number == 17
    assert bet.amount == 25


def test_bet_color_red(mm):
    model = mm.model_from_str("bankroll 100\nbet red 10\nspin")
    bet = model.statements[1]
    assert bet.bet_type.__class__.__name__ == 'ColorBet'
    assert bet.bet_type.color == 'red'
    assert bet.amount == 10


def test_bet_color_black(mm):
    model = mm.model_from_str("bankroll 100\nbet black 20\nspin")
    bet = model.statements[1]
    assert bet.bet_type.__class__.__name__ == 'ColorBet'
    assert bet.bet_type.color == 'black'
    assert bet.amount == 20


def test_bet_parity_even(mm):
    model = mm.model_from_str("bankroll 100\nbet even 15\nspin")
    bet = model.statements[1]
    assert bet.bet_type.__class__.__name__ == 'ParityBet'
    assert bet.bet_type.parity == 'even'
    assert bet.amount == 15


def test_bet_parity_odd(mm):
    model = mm.model_from_str("bankroll 100\nbet odd 30\nspin")
    bet = model.statements[1]
    assert bet.bet_type.__class__.__name__ == 'ParityBet'
    assert bet.bet_type.parity == 'odd'
    assert bet.amount == 30


def test_bet_range_low(mm):
    model = mm.model_from_str("bankroll 100\nbet low 40\nspin")
    bet = model.statements[1]
    assert bet.bet_type.__class__.__name__ == 'RangeBet'
    assert bet.bet_type.range == 'low'
    assert bet.amount == 40


def test_bet_range_high(mm):
    model = mm.model_from_str("bankroll 100\nbet high 50\nspin")
    bet = model.statements[1]
    assert bet.bet_type.__class__.__name__ == 'RangeBet'
    assert bet.bet_type.range == 'high'
    assert bet.amount == 50


def test_bet_dozen(mm):
    model = mm.model_from_str("bankroll 100\nbet dozen 2 60\nspin")
    bet = model.statements[1]
    assert bet.bet_type.__class__.__name__ == 'DozenBet'
    assert bet.bet_type.dozen == 2
    assert bet.amount == 60


def test_bet_column(mm):
    model = mm.model_from_str("bankroll 100\nbet column 3 35\nspin")
    bet = model.statements[1]
    assert bet.bet_type.__class__.__name__ == 'ColumnBet'
    assert bet.bet_type.column == 3
    assert bet.amount == 35


def test_bet_split(mm):
    model = mm.model_from_str("bankroll 100\nbet split 1,2 10\nspin")
    bet = model.statements[1]
    assert bet.bet_type.__class__.__name__ == 'SplitBet'
    assert list(bet.bet_type.numbers) == [1, 2]
    assert bet.amount == 10


def test_bet_street(mm):
    model = mm.model_from_str("bankroll 100\nbet street 1,2,3 15\nspin")
    bet = model.statements[1]
    assert bet.bet_type.__class__.__name__ == 'StreetBet'
    assert list(bet.bet_type.numbers) == [1, 2, 3]
    assert bet.amount == 15


def test_bet_corner(mm):
    model = mm.model_from_str("bankroll 100\nbet corner 1,2,4,5 20\nspin")
    bet = model.statements[1]
    assert bet.bet_type.__class__.__name__ == 'CornerBet'
    assert list(bet.bet_type.numbers) == [1, 2, 4, 5]
    assert bet.amount == 20


def test_bet_sixline(mm):
    model = mm.model_from_str("bankroll 100\nbet sixline 1,2,3,4,5,6 25\nspin")
    bet = model.statements[1]
    assert bet.bet_type.__class__.__name__ == 'SixLineBet'
    assert list(bet.bet_type.numbers) == [1, 2, 3, 4, 5, 6]
    assert bet.amount == 25


def test_bet_basket(mm):
    model = mm.model_from_str("bankroll 100\nbet basket 10\nspin")
    bet = model.statements[1]
    assert bet.bet_type.__class__.__name__ == 'BasketBet'
    assert bet.amount == 10


def test_spin(mm):
    model = mm.model_from_str("spin")
    assert model.statements[0].__class__.__name__ == 'Spin'


def test_show_balance(mm):
    model = mm.model_from_str("show_balance")
    assert model.statements[0].__class__.__name__ == 'ShowBalance'


def test_show_stats(mm):
    model = mm.model_from_str("show_stats")
    assert model.statements[0].__class__.__name__ == 'ShowStats'


def test_show_history(mm):
    model = mm.model_from_str("show_history")
    assert model.statements[0].__class__.__name__ == 'ShowHistory'


def test_clear_bets(mm):
    model = mm.model_from_str("clear_bets")
    assert model.statements[0].__class__.__name__ == 'ClearBets'


def test_cash_out(mm):
    model = mm.model_from_str("cash_out")
    assert model.statements[0].__class__.__name__ == 'CashOut'


def test_double_bet_inside_round(mm):
    src = "round { bet red 50\ndouble_bet\nspin }"
    model = mm.model_from_str(src)
    round_block = model.statements[0]
    assert round_block.statements[1].__class__.__name__ == 'DoubleBet'


def test_reset_bet_inside_round(mm):
    src = "round { bet red 50\nreset_bet\nspin }"
    model = mm.model_from_str(src)
    round_block = model.statements[0]
    assert round_block.statements[1].__class__.__name__ == 'ResetBet'


def test_stop_on_win_inside_round(mm):
    src = "round { bet red 20\nspin\nstop_on_win 600 }"
    model = mm.model_from_str(src)
    round_block = model.statements[0]
    assert round_block.statements[2].__class__.__name__ == 'StopOnWin'
    assert round_block.statements[2].amount == 600


def test_stop_on_loss_inside_round(mm):
    src = "round { bet red 20\nspin\nstop_on_loss 200 }"
    model = mm.model_from_str(src)
    round_block = model.statements[0]
    assert round_block.statements[2].__class__.__name__ == 'StopOnLoss'
    assert round_block.statements[2].amount == 200


def test_break(mm):
    model = mm.model_from_str("break")
    assert model.statements[0].__class__.__name__ == 'BreakCommand'


def test_continue(mm):
    model = mm.model_from_str("continue")
    assert model.statements[0].__class__.__name__ == 'ContinueCommand'


def test_skip_round(mm):
    model = mm.model_from_str("skip_round")
    assert model.statements[0].__class__.__name__ == 'SkipRoundCommand'


def test_repeat_block(mm):
    src = "bankroll 100\nrepeat 5 { bet black 10\nspin }"
    model = mm.model_from_str(src)
    repeat = model.statements[1]
    assert repeat.__class__.__name__ == 'RepeatBlock'
    assert repeat.times == 5
    assert len(repeat.statements) == 2


def test_while_block(mm):
    src = "bankroll 500\nwhile (balance > 100) { bet red 10\nspin }"
    model = mm.model_from_str(src)
    while_block = model.statements[1]
    assert while_block.__class__.__name__ == 'WhileBlock'
    assert while_block.condition.__class__.__name__ == 'BalanceCondition'
    assert while_block.condition.operator == '>'
    assert while_block.condition.amount == 100
    assert len(while_block.statements) == 2


def test_if_win(mm):
    src = "bankroll 100\nbet black 10\nspin\nif_win { show_balance }"
    model = mm.model_from_str(src)
    if_win = model.statements[3]
    assert if_win.__class__.__name__ == 'IfWin'
    assert len(if_win.statements) == 1


def test_if_lose(mm):
    src = "bankroll 100\nbet black 10\nspin\nif_lose { show_stats }"
    model = mm.model_from_str(src)
    if_lose = model.statements[3]
    assert if_lose.__class__.__name__ == 'IfLose'
    assert len(if_lose.statements) == 1


def test_if_win_with_else(mm):
    src = "bankroll 100\nbet black 10\nspin\nif_win { show_balance } else { show_stats }"
    model = mm.model_from_str(src)
    if_win = model.statements[3]
    assert if_win.__class__.__name__ == 'IfWin'
    assert if_win.else_part is not None
    assert len(if_win.else_part.statements) == 1


def test_if_lose_with_else(mm):
    src = "bankroll 100\nbet black 10\nspin\nif_lose { show_balance } else { show_stats }"
    model = mm.model_from_str(src)
    if_lose = model.statements[3]
    assert if_lose.__class__.__name__ == 'IfLose'
    assert if_lose.else_part is not None
    assert len(if_lose.else_part.statements) == 1


def test_conditional_if(mm):
    src = "bankroll 100\nif (balance > 50) { bet red 10\nspin }"
    model = mm.model_from_str(src)
    cond_if = model.statements[1]
    assert cond_if.__class__.__name__ == 'ConditionalIfBlock'
    assert cond_if.condition.__class__.__name__ == 'BalanceCondition'
    assert cond_if.condition.operator == '>'
    assert cond_if.condition.amount == 50
    assert len(cond_if.statements) == 2


def test_conditional_if_with_else(mm):
    src = "bankroll 100\nif (balance > 50) { bet red 10 } else { bet black 10 }"
    model = mm.model_from_str(src)
    cond_if = model.statements[1]
    assert cond_if.__class__.__name__ == 'ConditionalIfBlock'
    assert cond_if.else_part is not None
    assert len(cond_if.else_part.statements) == 1


def test_compound_condition_and(mm):
    src = "bankroll 100\nwhile (balance >= 800 and consecutive_wins >= 1) { bet red 10\nspin }"
    model = mm.model_from_str(src)
    while_block = model.statements[1]
    cond = while_block.condition
    assert cond.__class__.__name__ == 'CompoundCondition'
    assert cond.logic_op == 'and'
    assert cond.left.__class__.__name__ == 'BalanceCondition'
    assert cond.right.__class__.__name__ == 'ConsecutiveWins'


def test_compound_condition_or(mm):
    src = "bankroll 100\nwhile (balance < 50 or consecutive_losses >= 3) { bet red 10\nspin }"
    model = mm.model_from_str(src)
    while_block = model.statements[1]
    cond = while_block.condition
    assert cond.__class__.__name__ == 'CompoundCondition'
    assert cond.logic_op == 'or'
    assert cond.left.__class__.__name__ == 'BalanceCondition'
    assert cond.right.__class__.__name__ == 'ConsecutiveLosses'


def test_round_block(mm):
    src = "round { bet red 10\nspin\nshow_balance }"
    model = mm.model_from_str(src)
    round_block = model.statements[0]
    assert round_block.__class__.__name__ == 'Round'
    assert len(round_block.statements) == 3


def test_strategy_block(mm):
    src = "strategy my_strategy { bankroll 100\nbet red 10\nspin }"
    model = mm.model_from_str(src)
    strategy = model.statements[0]
    assert strategy.__class__.__name__ == 'Strategy'
    assert strategy.name == 'my_strategy'
    assert len(strategy.statements) == 3


def test_consecutive_wins_condition(mm):
    src = "while (consecutive_wins > 2) { bet red 10\nspin }"
    model = mm.model_from_str(src)
    while_block = model.statements[0]
    assert while_block.condition.__class__.__name__ == 'ConsecutiveWins'
    assert while_block.condition.operator == '>'
    assert while_block.condition.count == 2


def test_consecutive_losses_condition(mm):
    src = "while (consecutive_losses <= 5) { bet red 10\nspin }"
    model = mm.model_from_str(src)
    while_block = model.statements[0]
    assert while_block.condition.__class__.__name__ == 'ConsecutiveLosses'
    assert while_block.condition.operator == '<='
    assert while_block.condition.count == 5


def test_round_profit_condition(mm):
    src = "while (round_profit == 0) { bet red 10\nspin }"
    model = mm.model_from_str(src)
    while_block = model.statements[0]
    assert while_block.condition.__class__.__name__ == 'RoundProfitCondition'
    assert while_block.condition.operator == '=='
    assert while_block.condition.amount == 0


def test_comments_ignored(mm):
    src = "// This is a comment\nbankroll 100\n// Another comment\nspin"
    model = mm.model_from_str(src)
    assert len(model.statements) == 2
    assert model.statements[0].__class__.__name__ == 'Bankroll'
    assert model.statements[1].__class__.__name__ == 'Spin'


def test_model_from_file(mm):
    test_file = os.path.join(os.path.dirname(__file__), 'fixtures', 'test.rul')
    model = mm.model_from_file(test_file)
    assert len(model.statements) > 0
    assert model.statements[0].__class__.__name__ == 'Bankroll'


# ==========================
# SEMANTIC VALIDATION TESTS
# ==========================


def test_semantic_invalid_bet_number_37(mm):
    model = mm.model_from_str("bet number 37 10")
    roulet = Roulet()
    assert roulet.is_model_semantically_valid(model) is False


def test_semantic_invalid_bet_number_negative(mm):
    model = mm.model_from_str("bet number -1 10")
    roulet = Roulet()
    assert roulet.is_model_semantically_valid(model) is False


def test_semantic_invalid_dozen_zero(mm):
    model = mm.model_from_str("bet dozen 0 10")
    roulet = Roulet()
    assert roulet.is_model_semantically_valid(model) is False


def test_semantic_invalid_dozen_four(mm):
    model = mm.model_from_str("bet dozen 4 10")
    roulet = Roulet()
    assert roulet.is_model_semantically_valid(model) is False


def test_semantic_invalid_column_zero(mm):
    model = mm.model_from_str("bet column 0 10")
    roulet = Roulet()
    assert roulet.is_model_semantically_valid(model) is False


def test_semantic_invalid_column_four(mm):
    model = mm.model_from_str("bet column 4 10")
    roulet = Roulet()
    assert roulet.is_model_semantically_valid(model) is False


def test_semantic_invalid_split_one_number(mm):
    model = mm.model_from_str("bet split 1 10")
    roulet = Roulet()
    assert roulet.is_model_semantically_valid(model) is False


def test_semantic_invalid_street_two_numbers(mm):
    model = mm.model_from_str("bet street 1,2 10")
    roulet = Roulet()
    assert roulet.is_model_semantically_valid(model) is False


def test_semantic_invalid_corner_three_numbers(mm):
    model = mm.model_from_str("bet corner 1,2,3 10")
    roulet = Roulet()
    assert roulet.is_model_semantically_valid(model) is False


def test_semantic_invalid_sixline_five_numbers(mm):
    model = mm.model_from_str("bet sixline 1,2,3,4,5 10")
    roulet = Roulet()
    assert roulet.is_model_semantically_valid(model) is False


def test_semantic_valid_bet_number_36(mm):
    model = mm.model_from_str("bet number 36 10")
    roulet = Roulet()
    assert roulet.is_model_semantically_valid(model) is True


def test_semantic_valid_dozen_3(mm):
    model = mm.model_from_str("bet dozen 3 10")
    roulet = Roulet()
    assert roulet.is_model_semantically_valid(model) is True


def test_semantic_valid_column_1(mm):
    model = mm.model_from_str("bet column 1 10")
    roulet = Roulet()
    assert roulet.is_model_semantically_valid(model) is True


# ==========================
# INVALID PARSING TESTS
# ==========================


def test_invalid_syntax_missing_amount(mm):
    with pytest.raises(TextXSyntaxError):
        mm.model_from_str("bankroll")


def test_invalid_color(mm):
    with pytest.raises(TextXSyntaxError):
        mm.model_from_str("bet green 10")


def test_invalid_parity(mm):
    with pytest.raises(TextXSyntaxError):
        mm.model_from_str("bet neither 10")


def test_invalid_range(mm):
    with pytest.raises(TextXSyntaxError):
        mm.model_from_str("bet medium 10")


def test_malformed_while_missing_parenthesis(mm):
    with pytest.raises(TextXSyntaxError):
        mm.model_from_str("while balance > 100 { bet red 10\nspin }")


def test_malformed_repeat_missing_times(mm):
    with pytest.raises(TextXSyntaxError):
        mm.model_from_str("repeat { bet red 10\nspin }")


def test_malformed_if_missing_parenthesis(mm):
    with pytest.raises(TextXSyntaxError):
        mm.model_from_str("if balance > 100 { bet red 10\nspin }")


def test_invalid_comparison_operator(mm):
    with pytest.raises(TextXSyntaxError):
        mm.model_from_str("while (balance <> 100) { bet red 10\nspin }")


def test_invalid_logic_operator(mm):
    with pytest.raises(TextXSyntaxError):
        mm.model_from_str("while (balance > 100 xor consecutive_wins > 2) { bet red 10\nspin }")


def test_unclosed_block(mm):
    with pytest.raises(TextXSyntaxError):
        mm.model_from_str("repeat 3 { bet red 10\nspin")


def test_unexpected_token(mm):
    with pytest.raises(TextXSyntaxError):
        mm.model_from_str("bankroll 100\nunknown_command")
