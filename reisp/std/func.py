from reisp.ast.node_err import NodeErr
from reisp.ast.node import Node
from reisp.std.util import builtin_func

@builtin_func("set", 2)
def func_set(source, env, args):
    assert isinstance(args[0], Node.Ident)
    name = args[0].value
    if (value := args[1].eval(env)).is_err():
        return value
    if env.get(name):
        return NodeErr.VarAlreadyExists(source.loc, name)
    env.add(name, value)
    return value

@builtin_func("let", 2)
def func_let(source, env, args):
    assert isinstance(args[0], Node.List)
    if len(args[0].values) == 0:
        env.push()
        result = args[1].eval(env)
        env.pop()
        return result
    assert len(args[0].values) == 2
    assert isinstance(args[0].values[0], Node.Ident)
    name = args[0].values[0].value
    if (value := args[0].values[1].eval(env)).is_err():
        return value
    env.push()
    env.add(name, value)
    result = args[1].eval(env)
    env.pop()
    return result

@builtin_func("lambda", 2)
def func_lambda(source, env, args):
    assert isinstance(args[0], Node.List)
    parameters = args[0].values
    lambda_parameters = []
    for param in parameters:
        assert isinstance(param, Node.Ident)
        lambda_parameters.append(param.value)
    return Node.UserFunc(source.loc, "", lambda_parameters, args[1])

func_exports = [
    func_set,
    func_let,
    func_lambda
]
