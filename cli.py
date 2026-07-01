import argparse
import os
import sys

from textx import metamodel_from_file

from database import init_db
from interpreter import Roulet

GRAMMAR_PATH = os.path.join(os.path.dirname(__file__), "grammar.tx")

def run_file(filepath, seed=None, num_seeds=10, no_db=False):
    mm = metamodel_from_file(GRAMMAR_PATH)
    model = mm.model_from_file(filepath)

    strategy_name = os.path.splitext(os.path.basename(filepath))[0]
    init_db()
    roulet = Roulet(seed=seed)
    if roulet.is_model_semantically_valid(model):
        stats = roulet.run(model, strategy_name=strategy_name, save_to_db= not no_db, num_seeds=num_seeds)
        return stats
    else:
        print("Greska: Model nije semanticki validan")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(
        description='Rulet DSL simulator - pokretanje .rul strategija'
    )
    parser.add_argument('file', help="Putanja do .rul fajla")
    parser.add_argument('--seed', type=int, default=None, help="Seed za reprodukovanje rezultata")
    parser.add_argument('--num-seeds', type=int, default=10, help="Broj seed-ova za evaluaciju stategije (default: 10)")
    parser.add_argument('--no-db', action='store_true', help="Ne cuva rezultate u bazi")
    args = parser.parse_args()

    if not os.path.exists(args.file):
        print(f"Greska: fajl '{args.file}' ne postoji")
        sys.exit(1)

    try:
        run_file(args.file, seed=args.seed, num_seeds=args.num_seeds, no_db=args.no_db)
    except Exception as e:
        print(f"Greska pri izvrsavanju: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()