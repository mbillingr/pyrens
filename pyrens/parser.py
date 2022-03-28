from lark import Lark, Transformer


def parse_module(src):
    parse_tree = scheme.parse(src)
    return TreeToSexpr().transform(parse_tree)


scheme = Lark(
    r"""
    module: statement*
    
    ?statement: sexpr
    
    ?sexpr: SIGNED_NUMBER -> number
          | SYMBOL -> symbol
          | ESCAPED_STRING -> string
          | list | bracket_list
          | quote | quasiquote | unquote

    quote: "'" sexpr
    quasiquote: "`" sexpr
    unquote: "," sexpr
    
    list: "(" sexpr* ")"
    bracket_list: "[" sexpr* "]"
    
    SYMBOL: SYMBOL_INITIAL SYMBOL_REST*
    SYMBOL_INITIAL: ("A".."Z" | "a".."z" | "0".."9" | "-" | "+" | "/" | "_" | "." | "!" | "?" | "<" | "=" | ">")
    SYMBOL_REST: /[^\s()]/
    
    COMMENT: ";" /[^\n]*/ NEWLINE
    %ignore COMMENT
    
    %import common.ESCAPED_STRING
    %import common.SIGNED_NUMBER
    %import common.NEWLINE
    %import common.WS
    %ignore WS
    """,
    start = "module"
)


class TreeToSexpr(Transformer):
    def module(self, mod):
        return mod

    def quote(self, value):
        return ("quote", value[0])

    def quasiquote(self, value):
        return ["quasiquote", value[0]]

    def unquote(self, value):
        return ("unquote", value[0])

    def list(self, items):
        return tuple(items)

    def bracket_list(self, items):
        return list(items)

    def string(self, sym):
        content = str(sym[0])[1:-1]
        return ("quote", content)

    def symbol(self, sym):
        name = str(sym[0])
        return name

    def number(self, num):
        return int(num[0])
