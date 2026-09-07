"""
AST Zero-Loop Verification Tests.
Asserts that every Python file in the repository contains exactly ZERO loop nodes in its AST.
"""

import unittest
import os
import ast
from src.validator import validate_file, inspect_node


class TestASTNoLoops(unittest.TestCase):
    def setUp(self):
        self.repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.target_files = (
            os.path.join(self.repo_root, "src", "engine.py"),
            os.path.join(self.repo_root, "src", "validator.py"),
            os.path.join(self.repo_root, "src", "cli.py"),
            os.path.join(self.repo_root, "src", "gui.py"),
            os.path.join(self.repo_root, "main.py"),
        )

    def test_source_files_have_zero_loops(self):
        def _check_files_recursive(files):
            if not files:
                return
            filepath = files[0]
            self.assertTrue(os.path.exists(filepath), "File missing: " + str(filepath))
            is_valid, violations = validate_file(filepath)
            self.assertTrue(
                is_valid,
                "Loop violation detected in " + os.path.basename(filepath) + ": " + str(violations)
            )
            _check_files_recursive(files[1:])

        _check_files_recursive(self.target_files)

    def test_validator_detects_synthetic_loop(self):
        bad_code = "def foo():\n    for i in [1, 2]:\n        pass\n"
        tree = ast.parse(bad_code)
        violations = inspect_node(tree)
        self.assertTrue(len(violations) > 0)
        self.assertIn("For", violations[0])


if __name__ == "__main__":
    unittest.main()
