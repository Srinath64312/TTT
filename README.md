# Loopless Tic-Tac-Toe

> A fully functional, production-ready Tic-Tac-Toe game in Python built **without a single loop**.

---

## The Concept

Is it possible to write a complete Tic-Tac-Toe game in Python without using **any** `for` or `while` loops?

**Yes!** By utilizing **tail recursion**, **immutable state transitions**, **unrolled index operations**, and **functional decomposition**, all traditional iterative loops are eliminated:

- No `for` loops
- No `while` loops
- No list/dict/set comprehensions (`[x for x in ...]`)
- No generator expressions (`(x for x in ...)`)
- No `async for`

The project includes an **AST (Abstract Syntax Tree) validator** that programmatically inspects the codebase to prove that zero loop nodes exist.

---

## Features

- **Multiple Game Modes**:
  - **2-Player (PvP)**: Play locally with a friend in the terminal or GUI.
  - **Player vs AI**: Challenge an unbeatable recursive **Minimax AI**.
- **Multiple Interfaces**:
  - **Terminal CLI**: Fast, interactive, ASCII-rendered interface with input validation.
  - **Desktop GUI**: Clean, event-driven desktop window powered by Tkinter.
- **Recursive Minimax AI**:
  - Recursively evaluates all board permutations to guarantee the AI never loses.
- **Zero-Loop AST Verification**:
  - Automated test suite using Python's `ast` parser to verify compliance across all source files.
- **Zero External Dependencies**:
  - Built purely with Python Standard Library (`tkinter`, `unittest`, `ast`, `sys`, `os`).

---

## Quick Start

### 1. Clone or Download the Repository

```bash
git clone https://github.com/your-username/loopless-tictactoe.git
cd loopless-tictactoe
```

### 2. Run the Application

#### Launch Interactive CLI Menu:
```bash
python main.py
```

#### Launch Desktop GUI:
```bash
python main.py --gui
```

#### Run the AST Loopless Audit:
```bash
python main.py --check
```

---

## Running Tests

Run the full automated test suite (including game logic and the AST zero-loop audit):

```bash
python -m unittest discover tests
```

---

## How It Works Under the Hood

| Traditional Imperative Approach | Loopless Functional Approach |
|---|---|
| `while not game_over:` | **Tail Recursion**: `play_game_step(board, turn + 1)` |
| `while True: input(...)` | **Retry Recursion**: `get_human_move(board)` |
| `for row in grid:` | **Unrolled Direct Indexing**: `b[0]`, `b[1]`, ..., `b[8]` |
| `[i for i in range(9) if b[i] == ' ']` | **Recursive Tuple Fold**: `get_available_moves(board, idx)` |
| `for move in moves: minimax(...)` | **Recursive Minimax Search**: `_evaluate_moves_recursive(...)` |

---

## Repository Structure

```
loopless-tictactoe/
+-- src/
|   +-- __init__.py
|   +-- engine.py       # 100% loop-free core logic & Minimax AI
|   +-- cli.py          # Loop-free terminal UI & recursive prompts
|   +-- gui.py          # Event-driven desktop GUI (Tkinter)
|   +-- validator.py    # Loop-free AST static code analyzer
+-- tests/
|   +-- __init__.py
|   +-- test_engine.py  # Unit tests for wins, draws, immutability, AI
|   +-- test_ast.py     # Static AST tests enforcing zero loop constructs
+-- .gitignore
+-- LICENSE             # MIT License
+-- pyproject.toml      # Packaging metadata
+-- README.md           # Documentation
+-- main.py             # Main entry point & CLI/GUI dispatcher
```

---

## License

This project is licensed under the MIT License.
