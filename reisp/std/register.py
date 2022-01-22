from reisp.std.operators import operator_exports
from reisp.std.func import func_exports

def register_exports(env):
    all_exports = [*operator_exports, *func_exports]
    for export in all_exports:
        env.add(export.name, export)
