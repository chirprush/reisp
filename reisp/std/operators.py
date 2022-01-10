from reisp.std.util import builtin_func

@builtin_func("+", 2)
def op_plus(source, env, args):
    pass

@builtin_func("-", 2)
def op_minus(source, env, args):
    pass

@builtin_func("*", 2)
def op_mult(source, env, args):
    pass

@builtin_func("/", 2)
def op_div(source, env, args):
    pass

operator_exports = [op_plus, op_minus, op_mult, op_div]
