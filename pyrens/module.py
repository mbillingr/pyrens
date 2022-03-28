import types

from pyrens import syntax
from pyrens.core_lang import analyze_statement
from pyrens.intrinsics import initialize_intrinsics
from pyrens.macro_lang import expand_macros


def build_module(name, statements):
    mod = types.ModuleType(name)
    module_code = []

    initialize_intrinsics(mod)
    initialize_macros(mod)

    # While compiling we also execute all statements inside
    # the module. This is what enables macros.

    for stmt in module_prelude():
        module_code.append(build_and_execute(stmt, mod))

    for stmt in statements:
        module_code.append(build_and_execute(stmt, mod))

    return "\n".join(module_code), mod


def initialize_macros(mod):
    # predefined macros don't show up in the compiled code.
    # this means they can't be called as functions.
    mod.quasiquote = syntax.quasiquote


def module_prelude():
    return [("import", ("operator",)),]


def build_and_execute(stmt, mod):
    stmt = expand_macros(stmt, mod.__dict__)
    stmt_code = analyze_statement(stmt, mod)
    exec(stmt_code, mod.__dict__)
    return stmt_code
