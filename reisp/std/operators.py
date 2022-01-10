from reisp.ast.node_err import NodeErr
from reisp.ast.node import Node
from reisp.std.util import builtin_func

@builtin_func("!", 1)
def op_not(source, env, args):
    if (value := args[0].eval(env)).is_err():
        return value
    return Node.Bool(source.loc, not value.value)

@builtin_func("+", 2)
def op_plus(source, env, args):
    # TODO: We don't type check here because type checking should be
    # done by a type system before the code is run
    if (left := args[0].eval(env)).is_err():
        return left
    if (right := args[1].eval(env)).is_err():
        return right
    return Node.Int(source.loc, left.value + right.value)

@builtin_func("-", 2)
def op_minus(source, env, args):
    if (left := args[0].eval(env)).is_err():
        return left
    if (right := args[1].eval(env)).is_err():
        return right
    return Node.Int(source.loc, left.value - right.value)

@builtin_func("*", 2)
def op_mult(source, env, args):
    if (left := args[0].eval(env)).is_err():
        return left
    if (right := args[1].eval(env)).is_err():
        return right
    return Node.Int(source.loc, left.value * right.value)

@builtin_func("/", 2)
def op_div(source, env, args):
    if (left := args[0].eval(env)).is_err():
        return left
    if (right := args[1].eval(env)).is_err():
        return right
    if right.value == 0:
        return NodeErr.ZeroDiv(source.values[2].loc)
    return Node.Int(source.loc, left.value // right.value)

@builtin_func("%", 2)
def op_mod(source, env, args):
    if (left := args[0].eval(env)).is_err():
        return left
    if (right := args[1].eval(env)).is_err():
        return right
    return Node.Int(source.loc, left.value % right.value)

@builtin_func("=", 2)
def op_eq(source, env, args):
    if (left := args[0].eval(env)).is_err():
        return left
    if (right := args[1].eval(env)).is_err():
        return right
    return Node.Bool(source.loc, left.value == right.value)

@builtin_func("!=", 2)
def op_neq(source, env, args):
    if (left := args[0].eval(env)).is_err():
        return left
    if (right := args[1].eval(env)).is_err():
        return right
    return Node.Bool(source.loc, left.value != right.value)

@builtin_func("<", 2)
def op_less(source, env, args):
    if (left := args[0].eval(env)).is_err():
        return left
    if (right := args[1].eval(env)).is_err():
        return right
    return Node.Bool(source.loc, left.value < right.value)

@builtin_func(">", 2)
def op_greater(source, env, args):
    if (left := args[0].eval(env)).is_err():
        return left
    if (right := args[1].eval(env)).is_err():
        return right
    return Node.Bool(source.loc, left.value > right.value)

@builtin_func("<=", 2)
def op_leq(source, env, args):
    if (left := args[0].eval(env)).is_err():
        return left
    if (right := args[1].eval(env)).is_err():
        return right
    return Node.Bool(source.loc, left.value <= right.value)

@builtin_func(">=", 2)
def op_geq(source, env, args):
    if (left := args[0].eval(env)).is_err():
        return left
    if (right := args[1].eval(env)).is_err():
        return right
    return Node.Bool(source.loc, left.value >= right.value)

operator_exports = [
    op_not,
    op_plus,
    op_minus,
    op_mult,
    op_div,
    op_mod,
    op_eq,
    op_neq,
    op_less,
    op_greater,
    op_leq,
    op_geq
]
