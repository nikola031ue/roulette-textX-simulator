# Roulette DSL textX

Roulette DSL is a domain-specific language built with textX that
lets users describe and simulate roulette betting strategies
in a simple way.

Instead of writing Python code or tracking results by hand, the user writes a short script that describes the flow of the game, such as the starting budget, bet types, rules and strategies.

The language produces a clear roulette simulation that is easy to experiment with. It removes the need to write program code, track results manually or deal with complicated repetition logic.
Roulette DSL lets you describe a strategy, repetitions, statistics and more in just a few lines.

The target users of the language are players who want to test their strategies and track how well they perform, without writing code, building Excel spreadsheets or doing manual analysis.

# Syntax
Basic syntax example
```
bankroll 500
bet red 20
spin

show_balance
cash_out
```

## Commands
The commands available to the user cover money management (bankroll, cash_out), bets (bet red 20, bet number 7 5, bet even 20...), game flow (spin, repeat number_of_repetitions {...}), risk control (stop_on_win/loss int), automation logic (if_win/lose {...}, double_bet) and information (show_stats, show_history).

## Martingale strategy
This strategy increases the stake after each loss in order to recover previous losses.
```
bankroll 500 
repeat 15 { 
    bet black 10 
    spin 
    if_lose { 
        double_bet
    } 
    if_win { 
        reset_bet 
    }
} 
cash_out
```

# Installation and usage

```bash
pip install .
# or directly from GitHub
pip install git+https://github.com/nikola031ue/roulette-textX-simulator.git
```

After installation, the `roulette` CLI command is available:
```bash
roulette path/to/strategy.rul --seed 42 --num-seeds 20
```

# VS Code support (Syntax Highlighting + LSP)

The VS Code extension provides syntax highlighting and Language Server Protocol (LSP) support for `.roul` files, including autocomplete and real-time error diagnostics.

## Installation

**1. Python dependencies:**
```bash
pip install pygls textx
```

**2. Node dependencies (once, in the `vscode-roul/` folder):**
```bash
cd vscode-roul
npm install
```

**3. Install the extension in VS Code:**
```bash
# Windows
xcopy /E /I /Y vscode-roul "%USERPROFILE%\.vscode\extensions\roul-language-0.2.0"

# Linux/Mac
cp -r vscode-roul ~/.vscode/extensions/roul-language-0.2.0
```

**4. Restart VS Code** (`Ctrl+Shift+P` → `Developer: Reload Window`)

## Result

- **Syntax highlighting**: colors keywords, bet types, conditions and comments
- **Autocomplete**: `Ctrl+Space` suggests all DSL commands
- **Diagnostics**: errors are underlined in red as you type

---

# Grammar Validation and Visualization

## Checking the textX grammar
To check whether the `grammar.tx` file is syntactically valid, use the textX command:
```bash
textx check roulette/grammar.tx
```

## Generating a PNG visualization of the grammar
To visualize the structure of the grammar, generate a DOT file and convert it to PNG:

1. **Generate a DOT file from the textX grammar:**
```bash
textx generate roulette/grammar.tx --target dot
```
This command generates a `grammar.dot` file that describes the structure of the grammar.

2. **Convert the DOT file to PNG:**
```bash
dot -Tpng -O grammar.dot
```
This command creates a `grammar.dot.png` file with a visual representation of the grammar.

**Note:** Generating the image requires Graphviz, which you can download from [graphviz.org](https://graphviz.org/download/).
