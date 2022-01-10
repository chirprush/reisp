from reisp.std.operators import operator_exports

def register_exports(env):
    all_exports = [*operator_exports]
    for export in all_exports:
        env.add(export.name, export)
