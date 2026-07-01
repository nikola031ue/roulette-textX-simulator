import os.path
import sqlite3
from datetime import datetime
import json

DB_PATH = os.path.expanduser("~/.roulette_strategies.db")

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS strategies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            played_at TEXT NOT NULL,
            initial_bankroll INTEGER NOT NULL,
            final_bankroll INTEGER NOT NULL,
            net_profit INTEGER NOT NULL,
            total_spins INTEGER NOT NULL,
            wins INTEGER NOT NULL,
            losses INTEGER NOT NULL,
            win_rate REAL NOT NULL,
            max_drawdown INTEGER NOT NULL,
            avg_profit_per_spin REAL NOT NULL,
            score REAL NOT NULL,
            seed_results TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()

def save_strategy(name,initial_bankroll, stats, seed_results, score_value=None):
    score = score_value if score_value is not None else calculate_score(stats)
    conn = get_connection()
    conn.execute("""
        INSERT INTO strategies (
            name,
            played_at,
            initial_bankroll,
            final_bankroll,
            net_profit,
            total_spins,
            wins, losses,
            win_rate,
            max_drawdown,
            avg_profit_per_spin,
            score,
            seed_results
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        name,
        datetime.now().isoformat(),
        initial_bankroll,
        stats['final_bankroll'],
        stats['net_profit'],
        stats['total_spins'],
        stats['wins'],
        stats['losses'],
        stats['win_rate'],
        stats['max_drawdown'],
        stats['avg_profit_per_spin'],
        score,
        json.dumps(seed_results)
    ))
    conn.commit()
    conn.close()
    return score


def calculate_score(stats):
    if stats['total_spins'] == 0:
        return 0.0

    profit_factor = stats['net_profit'] / max(1, abs(stats['max_drawdown']))
    win_rate_factor = stats['win_rate']
    consistency = stats['avg_profit_per_spin']

    score = (profit_factor * 0.5) + (win_rate_factor * 30) + (consistency * 0.2)
    return round(score, 4)

def get_ranking(current_score):
    conn = get_connection()
    total = conn.execute("SELECT COUNT(*) as cnt FROM strategies").fetchone()['cnt']
    better = conn.execute("SELECT COUNT(*) as cnt FROM strategies WHERE score > ?", (current_score,)).fetchone()['cnt']
    all_strategies = conn.execute("SELECT name, score, net_profit, win_rate, total_spins FROM strategies ORDER BY score DESC").fetchall()
    conn.close()

    rank = better + 1
    return rank, total + 1, [dict(s) for s in all_strategies]