import json
from os.path import join, dirname
from textx import metamodel_from_file
import base64
import json
class Roulet:
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

        if bet_type.__class__.__name__ in ['DozenBet', 'ColumnBet']:
            if not (1 <= bet_type.value <= 3):
                print(f"Greska: mora biti izmedju  1 i 3, unet je broj {bet_type.value}")
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

def main(file_name_to_interpret):

    this_folder = dirname(__file__)

    rulet_mm = metamodel_from_file(join(this_folder, 'grammar.tx'), debug=False)
    rulet_model = rulet_mm.model_from_file(file_name_to_interpret)
    roulet = Roulet()
    roulet.is_model_semantically_valid(rulet_model)
        

if __name__ == "__main__":
    main("ruletPrimer.rul")    