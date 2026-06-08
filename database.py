import sqlite3

def init_db():
    conn = sqlite3.connect("roulette.db")
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS strategy_stats (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        starting_bankroll REAL,
        ending_bankroll REAL,
        number_of_spins INTEGER,
        win_rate REAL,
        max_drawdown REAL,
        net_profit REAL
    )
    """)

    conn.commit()
    conn.close()

def save_strategy(data):
    conn = sqlite3.connect("roulette.db")
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO strategy_stats (
            name,
            starting_bankroll,
            ending_bankroll,
            number_of_spins,
            win_rate,
            max_drawdown,
            net_profit
        ) VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        data["name"],
        data["starting_bankroll"],
        data["ending_bankroll"],
        data["number_of_spins"],
        data["win_rate"],
        data["max_drawdown"],
        data["net_profit"]
    ))

    conn.commit()
    conn.close()
