def expand_macros(expr, env):
    def expand_star(exprs):
        return (expand_macros(x, env) for x in exprs)

    match expr:
        case list([macro, *args]):
            return env[macro](*expand_star(args))
        case [*sub_exprs]:
            constructor = type(expr)
            return constructor(expand_star(sub_exprs))
        case _:
            return expr