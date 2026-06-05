import json
from os.path import join, dirname
from textx import metamodel_from_file
import base64
import json
import random

RED_NUMBERS = {
    1,3,5,7,9,12,14,16,18,
    19,21,23,25,27,30,32,34,36
}

class Roulet:
    def __init__(self):
        self.balance = 0
        self.current_bets = []
        self.consecutive_wins = 0
        self.consecutive_losses = 0
        self.round_profit = 0
        self.last_spin_won = False
        self._break = False
        self._skip_round = False

    def is_model_semantically_valid(self, model):

        for stmt in model.statements:
            if not self.validate_statement(stmt):
                return False

        return True

    def validate_statement(self, stmt):

        if stmt.__class__.__name__ == 'Bet':
            return self.validate_bet(stmt)

        return True

    def validate_bet(self, bet):

        bet_type = bet.bet_type

        if not self.validate_number_bet(bet_type):
            return False

        if not self.validate_dozen_column(bet_type):
            return False

        if not self.validate_split(bet_type):
            return False

        return True

    def validate_number_bet(self, bet_type):

        if bet_type.__class__.__name__ == 'NumberBet':
            if not (0 <= bet_type.number <= 36):
                print(f"Greska: broj mora biti izmedju 0–36, unet je broj {bet_type.number}")
                return False

        return True   

    def validate_dozen_column(self, bet_type):

        if bet_type.__class__.__name__ == 'DozenBet':
            if not (1 <= bet_type.dozen <= 3):
                print(f"Greska: dozen mora biti izmedju 1 i 3, unet je broj {bet_type.dozen}")
                return False

        elif bet_type.__class__.__name__ == 'ColumnBet':
            if not (1 <= bet_type.column <= 3):
                print(f"Greska: column mora biti izmedju 1 i 3, unet je broj {bet_type.column}")
                return False

        return True

    def validate_split(self, bet_type):

        if bet_type.__class__.__name__ == 'SplitBet':
            if len(bet_type.numbers) != 2:
                print("Error: split mora imati tacno 2 broja")
                return False

        elif bet_type.__class__.__name__ == 'StreetBet':
            if len(bet_type.numbers) != 3:
                print("Error: street mora imati tacno 3 broja")
                return False

        elif bet_type.__class__.__name__ == 'CornerBet':
            if len(bet_type.numbers) != 4:
                print("Error: corner mora imati tacno 4 broja")
                return False

        elif bet_type.__class__.__name__ == 'SixLineBet':
            if len(bet_type.numbers) != 6:
                print("Error: sixline mora imati tacno 6 brojeva")
                return False

        return True 

    def interpret(self, model):

        for stmt in model.statements:
            self.execute_statement(stmt)

    def execute_statement(self, stmt):

        stmt_type = stmt.__class__.__name__

        if stmt_type == 'Bankroll':
            self.handle_bankroll(stmt)

        elif stmt_type == 'Bet':
            self.handle_bet(stmt)

        elif stmt_type == 'Spin':
            self.handle_spin()

        elif stmt_type == 'ShowBalance':
            self.handle_show_balance()

        elif stmt_type == 'CashOut':
            self.handle_cash_out() 

        elif stmt_type == 'RepeatBlock':
            self.handle_repeat(stmt) 

        elif stmt_type == 'WhileBlock':
            self.handle_while(stmt)

        elif stmt_type == 'IfWin':
            self.handle_if_win(stmt)

        elif stmt_type == 'IfLose':
            self.handle_if_lose(stmt)

        elif stmt_type == 'ConditionalIfBlock':
            self.handle_conditional_if(stmt)

        elif stmt_type == 'BreakCommand':
            self._break = True

        elif stmt_type == 'SkipRoundCommand':
            self._skip_round = True

        elif stmt_type == 'Round':
            self.handle_round(stmt)
            
    def handle_bankroll(self, stmt):

        self.balance = stmt.amount

        print(f"Balance postavljen na {self.balance}")

    def handle_bet(self, stmt):

        amount = stmt.amount

        if amount > self.balance:
            print("Nema dovoljno novca")
            return

        self.balance -= amount

        self.current_bets.append({
            "bet_type": stmt.bet_type,
            "amount": amount
        })

        print(f"Bet dodat: {amount}")

    def handle_spin(self):

        result = random.randint(0, 36)

        print(f"Spin rezultat: {result}")

        total_win = 0

        for bet in self.current_bets:

            payout = self.calculate_payout(
                bet["bet_type"],
                bet["amount"],
                result
            )

            total_win += payout

        self.balance += total_win

        self.round_profit = total_win

        if total_win > 0:
            self.last_spin_won = True
            self.consecutive_wins += 1
            self.consecutive_losses = 0

        else:
            self.last_spin_won = False
            self.consecutive_losses += 1
            self.consecutive_wins = 0

        print(f"Ukupan dobitak: {total_win}")

        self.current_bets.clear()

    def handle_show_balance(self):

        print(f"Balance: {self.balance}")

    def handle_cash_out(self):

        print(f"Cash out: {self.balance}")   

    def handle_repeat(self, stmt):

        for _ in range(stmt.times):
            if self._break:
                break
            for inner_stmt in stmt.statements:
                self.execute_statement(inner_stmt)
                if self._break:
                    break
        self._break = False

    def handle_while(self, stmt):

        while self.evaluate_condition(stmt.condition):
            if self._break:
                break
            for inner_stmt in stmt.statements:
                self.execute_statement(inner_stmt)
                if self._break:
                    break
        self._break = False

    def handle_if_win(self, stmt):
        if self.last_spin_won:
            for inner_stmt in stmt.statements:
                self.execute_statement(inner_stmt)
        elif stmt.else_part:
            for inner_stmt in stmt.else_part.statements:
                self.execute_statement(inner_stmt)

    def handle_if_lose(self, stmt):
        if not self.last_spin_won:
            for inner_stmt in stmt.statements:
                self.execute_statement(inner_stmt)
        elif stmt.else_part:
            for inner_stmt in stmt.else_part.statements:
                self.execute_statement(inner_stmt)

    def handle_conditional_if(self, stmt):
        if self.evaluate_condition(stmt.condition):
            for inner_stmt in stmt.statements:
                self.execute_statement(inner_stmt)
        elif stmt.else_part:
            for inner_stmt in stmt.else_part.statements:
                self.execute_statement(inner_stmt)

    def handle_round(self, stmt):
        self.round_profit = 0
        self._skip_round = False
        for inner_stmt in stmt.statements:
            if self._skip_round:
                break
            self.execute_statement(inner_stmt)

    def calculate_payout(self, bet_type, amount, result):

        bet_name = bet_type.__class__.__name__

        # NUMBER BET
        if bet_name == 'NumberBet':

            if result == bet_type.number:
                return amount * 36

        # COLOR BET
        elif bet_name == 'ColorBet':

            if bet_type.color == 'red':

                if result in RED_NUMBERS:
                    return amount * 2

            elif bet_type.color == 'black':

                if result != 0 and result not in RED_NUMBERS:
                    return amount * 2

        # PARITY BET
        elif bet_name == 'ParityBet':

            if result == 0:
                return 0

            if bet_type.parity == 'even' and result % 2 == 0:
                return amount * 2

            if bet_type.parity == 'odd' and result % 2 == 1:
                return amount * 2

        # RANGE BET
        elif bet_name == 'RangeBet':

            if bet_type.range == 'low':

                if 1 <= result <= 18:
                    return amount * 2

            elif bet_type.range == 'high':

                if 19 <= result <= 36:
                    return amount * 2

        # DOZEN BET
        elif bet_name == 'DozenBet':

            if bet_type.dozen == 1 and 1 <= result <= 12:
                return amount * 3

            elif bet_type.dozen == 2 and 13 <= result <= 24:
                return amount * 3

            elif bet_type.dozen == 3 and 25 <= result <= 36:
                return amount * 3

        # COLUMN BET
        elif bet_name == 'ColumnBet':

            if result != 0:

                column = ((result - 1) % 3) + 1

                if column == bet_type.column:
                    return amount * 3

        # SPLIT BET
        elif bet_name == 'SplitBet':

            if result in bet_type.numbers:
                return amount * 18

        # STREET BET
        elif bet_name == 'StreetBet':

            if result in bet_type.numbers:
                return amount * 12

        # CORNER BET
        elif bet_name == 'CornerBet':

            if result in bet_type.numbers:
                return amount * 9

        # SIX LINE BET
        elif bet_name == 'SixLineBet':

            if result in bet_type.numbers:
                return amount * 6

        # BASKET BET
        elif bet_name == 'BasketBet':

            if result in [0, 1, 2, 3]:
                return amount * 7

        return 0   


    def evaluate_condition(self, condition):

        condition_type = condition.__class__.__name__

    #compound condition
        if condition_type == 'CompoundCondition':

            left_result = self.evaluate_condition(condition.left)

            right_result = self.evaluate_condition(condition.right)

            if condition.logic_op == 'and':
                return left_result and right_result

            elif condition.logic_op == 'or':
                return left_result or right_result

    #balance condition
        elif condition_type == 'BalanceCondition':

            return self.compare(
                self.balance,
                condition.operator,
                condition.amount
            )

    
    #consecutive wins
        elif condition_type == 'ConsecutiveWins':

            return self.compare(
                self.consecutive_wins,
                condition.operator,
                condition.count
            )

    
    #consecutive losses
        elif condition_type == 'ConsecutiveLosses':

            return self.compare(
                self.consecutive_losses,
                condition.operator,
                condition.count
            )

   
    #round profit
        elif condition_type == 'RoundProfitCondition':

            return self.compare(
                self.round_profit,
                condition.operator,
                condition.amount
            )

        return False

    def compare(self, left, operator, right):

        if operator == '>':
            return left > right

        elif operator == '<':
            return left < right

        elif operator == '>=':
                return left >= right

        elif operator == '<=':
            return left <= right

        elif operator == '==':
            return left == right

        elif operator == '!=':
            return left != right

        return False          
             

def main(file_name_to_interpret):

    this_folder = dirname(__file__)

    rulet_mm = metamodel_from_file(join(this_folder, 'grammar.tx'), debug=False)
    rulet_model = rulet_mm.model_from_file(file_name_to_interpret)
    roulet = Roulet()
    if roulet.is_model_semantically_valid(rulet_model):
        roulet.interpret(rulet_model)
        
        

if __name__ == "__main__":
    main("test_issue6.rul")
