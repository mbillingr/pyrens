import subprocess

from pyrens.parser import parse_module
from pyrens.module import build_module


def transpile(lisp_src):
    tree_lang = parse_module(lisp_src)
    print(tree_lang)
    py_code, _ = build_module("unnamed module", tree_lang)
    print(py_code)
    return py_code


def test_compile_and_run_a_simple_module():
    lisp_src = "(print 'abc \"xyz\")"
    py_src = transpile(lisp_src)
    output = run_code_in_process(py_src)
    assert output == "abc xyz"


def test_import_a_python_module():
    lisp_src = "(import (sys)) (print (getattr sys '__name__))"
    py_src = transpile(lisp_src)
    output = run_code_in_process(py_src)
    assert output == "sys"


def test_import_nested_python_module():
    lisp_src = "(import (collections abc)) (print collections.abc.__name__)"
    py_src = transpile(lisp_src)
    output = run_code_in_process(py_src)
    assert output == "collections.abc"


def test_define_function_and_use_it_as_macro():
    lisp_src = """
        (define (inc x) `(+ ,x 1))
        (print (inc 10))  ; normal application
        (print [inc 10])  ; macro application
    """
    py_src = transpile(lisp_src)
    output = run_code_in_process(py_src)
    assert output.splitlines() == ["('+', 10, 1)", "11"]


def run_code_in_process(py_src):
    res = subprocess.run(("python", "-c", py_src), capture_output=True)
    return res.stdout.decode().strip()
