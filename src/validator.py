"""
AST Compliance Validator
Statically verifies that target Python code contains zero loops:
- No ast.For
- No ast.AsyncFor
- No ast.While
- No ast.ListComp
- No ast.SetComp
- No ast.DictComp
- No ast.GeneratorExp

This validator itself is also written 100% loop-free!
"""

import ast

LOOP_NODE_TYPES = (
    ast.For,
    ast.AsyncFor,
    ast.While,
    ast.ListComp,
    ast.SetComp,
    ast.DictComp,
    ast.GeneratorExp,
)


def _check_ast_node_children(children, violations):
    if not children:
        return violations
    node = children[0]
    node_violations = inspect_node(node)
    return _check_ast_node_children(children[1:], violations + node_violations)


def inspect_node(node):
    current_violation = ()
    if isinstance(node, LOOP_NODE_TYPES):
        line = getattr(node, "lineno", "Unknown")
        type_name = type(node).__name__
        current_violation = ("Loop construct " + type_name + " at line " + str(line),)

    children = tuple(ast.iter_child_nodes(node))
    return _check_ast_node_children(children, current_violation)


def validate_source(source_code, filename="<source>"):
    tree = ast.parse(source_code, filename=filename)
    violations = inspect_node(tree)
    return len(violations) == 0, violations


def validate_file(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    return validate_source(content, filename=filepath)
