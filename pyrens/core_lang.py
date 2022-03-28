"""
This is the core language, which finally compiles to Python.

The core language aims for simplicity. It should have only few special forms.
However, absolute minimalism is not a goal. Small increases in complexity that
lead to big improvements in the resulting Python will be included.
"""
from pyrens.intrinsics import Intrinsic

BLOCK_INDENT = "    "


def analyze_statement(expr, env, indent=""):
    match expr:
        case ("import", *libs):
            return indent + "import " + ", ".join(".".join(lib) for lib in libs)
        case ("define", (name, *params), *body, last):
            head = indent + f"def {name}({', '.join(params)}):"
            body = (analyze_statement(body_stmt, env, indent + BLOCK_INDENT) for body_stmt in body)
            last = indent + BLOCK_INDENT + "return " + analyze_expr(last, env)
            return "\n".join([head, *body, last])
        case _:
            return indent + analyze_expr(expr, env)


def analyze_expr(expr, env):
    match expr:
        case("quote", value):
            return repr(value)
        case(func, *args):
            args = [analyze_expr(a, env) for a in args]
            if func in env.__dict__:
                f = env.__dict__[func]
                if isinstance(f, Intrinsic):
                    return f.application(*args)
            func = analyze_expr(func, env)
            return f"{func}({', '.join(args)})"
        case _:
            return str(expr)
