"""
Main Application Launcher
Zero-loop entrypoint with CLI/GUI/Validator dispatch.
"""

import sys
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from src.cli import main_menu, run_ast_audit
from src.gui import launch_gui


def dispatch_argument(args):
    if not args:
        return main_menu()

    arg = args[0].lower()
    if arg in ("--gui", "-g"):
        return launch_gui()
    elif arg in ("--cli", "-c"):
        return main_menu()
    elif arg in ("--audit", "--check", "-a"):
        return run_ast_audit(return_to_menu=False)
    elif arg in ("--web", "-w"):
        import webbrowser
        index_path = os.path.join(BASE_DIR, "index.html")
        print("Opening Web Frontend in browser: " + index_path)
        webbrowser.open("file://" + os.path.abspath(index_path))
        return
    elif arg in ("--help", "-h"):
        print("Loopless Tic-Tac-Toe")
        print("Usage:")
        print("  python main.py        Launch interactive CLI menu")
        print("  python main.py --web  Open Minimalist Web Frontend in Browser")
        print("  python main.py --gui  Launch Desktop Tkinter GUI")
        print("  python main.py --cli  Launch Terminal CLI")
        print("  python main.py --check Run AST Zero-Loop Validator")
        return sys.exit(0)
    else:
        print("Unknown argument " + arg + ". Starting default CLI.")
        return main_menu()


if __name__ == "__main__":
    dispatch_argument(sys.argv[1:])
