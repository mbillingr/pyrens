
class Intrinsic:
    pass


def initialize_intrinsics(mod):
    # intrinsics don't show up in the compiled code because they are
    # replaced by special python constructs
    mod.__dict__.update({
        "make-tuple": MakeTuple(),
        "getattr": GetAttr(),
        "+": Addition(),
    })


class MakeTuple(Intrinsic):
    def application(self, *args):
        return "(" + " ".join(a + "," for a in args) + ")"

    def reference(self):
        return "(lambda *args: args)"


class GetAttr(Intrinsic):
    def application(self, obj, attr):
        if is_string_literal(attr):
            return f"({obj}).{string_literal_content(attr)}"
        else:
            return f"getattr({obj}, {attr})"

    def reference(self):
        return "getattr"


class Addition(Intrinsic):
    def application(self, a, b):
        return f"({a} + {b})"

    def reference(self):
        return "(lambda a, b: a + b)"


def is_string_literal(s: str) -> bool:
    return s[0] == '"' and s[-1] == '"' or s[0] == "'" and s[-1] == "'"


def string_literal_content(s: str) -> str:
    return s[1:-1]
