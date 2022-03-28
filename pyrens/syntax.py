
def quasiquote(x):
    match x:
        case ("unquote", y):
            return y
        case tuple():
            expanded = [quasiquote(y) for y in x]
            return ("make-tuple", *expanded)
        case _:
            return ("quote", x)
