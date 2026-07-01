import json
from os.path import join, dirname
from unittest import result

from textx import metamodel_from_file
import base64
import json
import random
from database import init_db, save_strategy, calculate_score, get_ranking
from simulator import spin_wheel

RED_NUMBERS = {
    1,3,5,7,9,12,14,16,18,
    19,21,23,25,27,30,32,34,36
}

class StopGame(Exception):
    """Izuzetak za zaustavljanje igre na cash_out i stop_on_win/loss"""
    pass

class Roulet:
    def __init__(self, seed=None):
        self.balance = 0
        self.current_bets = []
        self.consecutive_wins = 0
        self.consecutive_losses = 0
        self.round_profit = 0
        self.last_spin_won = False
        self.total_spins = 0
        self.total_wins = 0
        self.biggest_win = 0
        self.biggest_loss = float("inf")
        self.net_profit = 0
        self.history = []
        self.starting_bankroll = 0
        self._break = False
        self._skip_round = False
        self.peak_balance = 0
        self.max_drawdown = 0
        self.last_bet_amount = 0
        self.initial_bet_amount = 0
        self.seed = seed
        self.spin_counter = 0

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

    def run(self, model, strategy_name="unnamed", save_to_db=True, num_seeds=10):
        try:
            self.interpret(model)
        except StopGame:
            pass

        stats = self._compute_stats()

        if save_to_db and self.starting_bankroll > 0:
            seed_results = self._evaluate_multiple_seeds(model, num_seeds)
            avg_stats = self._compute_avg_stats(seed_results)
            score = save_strategy(strategy_name, self.starting_bankroll, stats, seed_results, score_value=calculate_score(avg_stats))
            rank, total, all_strategies = get_ranking(score)
            self._print_ranking(rank, total, score, all_strategies, strategy_name)

        return stats

    def _compute_stats(self):
        total_spins = self.total_spins
        net_profit = self.balance - self.starting_bankroll
        win_rate = (self.total_wins / total_spins * 100) if total_spins > 0 else 0
        avg_profit = net_profit / total_spins if total_spins > 0 else 0
        losses = total_spins - self.total_wins
        return {
            'final_bankroll': self.balance,
            'net_profit': net_profit,
            'total_spins': total_spins,
            'wins': self.total_wins,
            'losses': losses,
            'win_rate': win_rate,
            'max_drawdown': self.max_drawdown,
            'avg_profit_per_spin': avg_profit,
        }

    def _evaluate_multiple_seeds(self, model, num_seeds):
        results = []
        for s in range(num_seeds):
            roulet = Roulet(seed=s)
            try:
                roulet.interpret(model)
            except StopGame:
                pass
            results.append({
                'seed': s,
                **roulet._compute_stats()
            })
        return results

    def _compute_avg_stats(self, seed_results):
        """Racuna prosecnu statistiku iz rezultata vise seed-ova."""
        if not seed_results:
            return self._compute_stats()

        n = len(seed_results)
        avg_net_profit = sum(r['net_profit'] for r in seed_results) / n
        avg_total_spins = sum(r['total_spins'] for r in seed_results) / n
        avg_max_drawdown = sum(r['max_drawdown'] for r in seed_results) / n
        avg_win_rate = sum(r['win_rate'] for r in seed_results) / n
        avg_final_bankroll = sum(r['final_bankroll'] for r in seed_results) / n
        avg_wins = sum(r['wins'] for r in seed_results) / n
        avg_losses = sum(r['losses'] for r in seed_results) / n
        avg_profit_per_spin = avg_net_profit / max(1, avg_total_spins)

        return {
            'final_bankroll': int(avg_final_bankroll),
            'net_profit': int(avg_net_profit),
            'total_spins': int(avg_total_spins),
            'wins': int(avg_wins),
            'losses': int(avg_losses),
            'win_rate': round(avg_win_rate, 2),
            'max_drawdown': int(avg_max_drawdown),
            'avg_profit_per_spin': round(avg_profit_per_spin, 4),
        }

    def _print_ranking(self, rank, total, score, all_strategies, strategy_name):
        print("\n" + "=" * 50)
        print(f"  RANGIRANJE STRATEGIJE")
        print("=" * 50)
        print(f"  Tvoj rank: #{rank} od {total} strategija")
        print(f"  Tvoj score: {score:.4f}")
        print("\n  Top 5 strategija:")
        for i, s in enumerate(all_strategies[:5], 1):
            print(f"  {i}. {s['name']} | score: {s['score']:.4f} | profit: {s['net_profit']}")
        print("=" * 50 + "\n")

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

        elif stmt_type == 'ShowStats' :
            self.handle_show_stats()

        elif stmt_type == 'ShowHistory':
            self.handle_show_history()

        elif stmt_type == 'CashOut':
            self.handle_cash_out()

        elif stmt_type == 'ClearBets':
            self.handle_clear_bets()

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

        elif stmt_type == 'Strategy':
            self.handle_strategy(stmt)

        elif stmt_type == 'DoubleBet':
            self.handle_double_bet()

        elif stmt_type == 'ResetBet':
            self.handle_reset_bet()

        elif stmt_type == 'StopOnWin':
            self.handle_stop_on_win(stmt)

        elif stmt_type == 'StopOnLoss':
            self.handle_stop_on_loss(stmt)
            
    def handle_bankroll(self, stmt):

        self.balance = stmt.amount
        self.starting_bankroll = stmt.amount
        self.peak_balance = stmt.amount
        print(f"Balance postavljen na {self.balance}")

    def handle_show_stats(self):
        win_rate = 0
        if self.total_spins > 0:
            win_rate = (self.total_wins / self.total_spins) * 100

        print("\n--- STATS ---")
        print(f"Total spins: {self.total_spins}")
        print(f"Win rate: {win_rate:.2f}%")
        print(f"Net profit: {self.net_profit}")
        print(f"Biggest win: {self.biggest_win}")
        print(f"Biggest loss: {self.biggest_loss}")

    def handle_show_history(self):
        print("\n--- ISTORIJA SPINOVA ---")
        for i, entry in enumerate(self.history, 1):
            print(f"  #{i:3d}: broj={entry['result']:2d} | profit={entry['profit']:+d}")
        print("------------------------\n")

    def handle_clear_bets(self):
        self.current_bets.clear()
        print("Opklade obrisane")

    def handle_strategy(self, stmt):
        for inner_stmt in stmt.statements:
            self.execute_statement(inner_stmt)

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

        self.last_bet_amount = amount
        if self.initial_bet_amount == 0 and amount > 0:
            self.initial_bet_amount = amount

        print(f"Bet dodat: {amount}")

    def handle_spin(self):

        seed = None
        if self.seed is not None:
            seed = self.seed + self.spin_counter
        result = spin_wheel(seed)
        self.spin_counter += 1

        self.total_spins += 1

        print(f"Spin rezultat: {result}")

        total_win = 0
        total_bet = 0

        for bet in self.current_bets:

            total_bet += bet["amount"]

            payout = self.calculate_payout(
                bet["bet_type"],
                bet["amount"],
                result
            )

            total_win += payout

        self.balance += total_win

        spin_profit = total_win - total_bet

        self.net_profit += spin_profit

        if spin_profit > self.biggest_win:
            self.biggest_win = spin_profit

        if spin_profit < self.biggest_loss:
            self.biggest_loss = spin_profit

        if spin_profit > 0:
            self.total_wins += 1
            self.last_spin_won = True
            self.consecutive_wins += 1
            self.consecutive_losses = 0
        else:
            self.last_spin_won = False
            self.consecutive_losses += 1
            self.consecutive_wins = 0

        self.round_profit = spin_profit
        if self.balance > self.peak_balance:
            self.peak_balance = self.balance

        drawdown = self.peak_balance - self.balance

        if drawdown > self.max_drawdown:
            self.max_drawdown = drawdown

        print(f"Ukupan dobitak: {total_win}")
        print(f"Profit spin-a: {spin_profit}")

        self.history.append({
            "result": result,
            "profit": spin_profit,
            "balance": self.balance
        })

        self.current_bets.clear()

    def handle_show_balance(self):

        print(f"Balance: {self.balance}")

    def handle_cash_out(self):

        print(f"Cash out: {self.balance}")
        raise StopGame()

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

    def handle_double_bet(self):
        if not self.current_bets:
            print("Nema aktivnih opklada za dupli ulog")
            return

        #da li ima dovoljno novca za sve opklade?
        total_additional = sum(bet["amount"] for bet in self.current_bets)
        if self.balance < total_additional:
            print("Nema dovoljno novca za duplu ulog")
            return

        self.balance -= total_additional
        for bet in self.current_bets:
            bet["amount"] *= 2
        self.last_bet_amount *= 2
        print(f"Dupli ulog: Ulog je udvostrucen na {self.last_bet_amount}")

    def handle_reset_bet(self):
        if not self.current_bets:
            return
        #prvo izracunaj ukupnu razliku i proveri
        total_needed = 0
        total_refund = 0
        for bet in self.current_bets:
            current = bet["amount"]
            target = self.initial_bet_amount
            if current < target:
                total_needed += (target - current)
            elif current > target:
                total_refund += (current - target)

        net_needed = total_needed - total_refund
        if net_needed > 0 and self.balance < net_needed:
            return

        if net_needed > 0:
            self.balance -= net_needed
        elif net_needed < 0:
            self.balance += abs(net_needed)

        for bet in self.current_bets:
            bet["amount"] = self.initial_bet_amount
        self.last_bet_amount = self.initial_bet_amount
        print(f"Reset bet: Ulog vracen na {self.last_bet_amount}")

    def handle_stop_on_win(self, stmt):
        if self.balance >= stmt.amount:
            print(f"Stop on win: dostignut {stmt.amount}!")
            raise StopGame()

    def handle_stop_on_loss(self, stmt):
        if self.balance <= self.starting_bankroll - stmt.amount:
            print(f"Stop on loss: izgubljeno {stmt.amount}!")
            raise StopGame()

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

             

def main(file_name_to_interpret, seed=None, num_seeds=10, save_to_db=True):

    this_folder = dirname(__file__)

    rulet_mm = metamodel_from_file(join(this_folder, 'grammar.tx'), debug=False)
    rulet_model = rulet_mm.model_from_file(file_name_to_interpret)
    init_db()
    roulet = Roulet(seed=seed)
    if roulet.is_model_semantically_valid(rulet_model):
        strategy_name = file_name_to_interpret.split('.')[0]
        roulet.run(rulet_model, strategy_name=strategy_name, save_to_db=save_to_db, num_seeds=num_seeds)
        


if __name__ == "__main__":
    main("test_issue7.rul")
