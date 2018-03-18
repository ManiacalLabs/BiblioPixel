import math, operator
from . address import Address

"""
Simple numerical operations put together in a list, useful for
scaling or offsetting some incoming numerical value.

Examples:

   Ops()(x)
returns the number unchanged

   Ops('mul', 0.5)(x)
multiples x by 0.5

   Ops('add', 0.1)(x)
adds 1 to x

   Ops('sqrt')(x)
returns the square root of x

   Ops('mul', 0.5, 'add', 1, 'sqrt')(x)
returns sqrt(1 + 0.5 * x)

"""


class Op:
    def __init__(self, op, *values):
        if len(values) > len(OPS):
            raise KeyError('Too many arguments for ' + op)
        ops = OPS[len(values)]

        if op not in ops:
            raise KeyError(OPS_ERROR.format(op, ', '.join(sorted(ops))))
        self.op = ops[op]

        self.opname = op
        self.values = values

    def __call__(self, x):
        return self.op(x, *self.values)

    def __str__(self):
        values = ', '.join(str(v) for v in self.values)
        return '%s(%s)' % self.opname, values


class Ops:
    def __init__(self, *ops):
        self.ops = tuple(_make_ops(ops))

    def __call__(self, x):
        for op in self.ops:
            x = op(x)
        return x

    def __bool__(self):
        return bool(self.ops)

    def __str__(self):
        return '->'.join(str(i) for i in self.ops)


def _make_ops(ops):
    op, values = None, []
    for o in ops:
        if isinstance(o, str):
            # We're starting a new operation
            if op:
                yield Op(op, *values)
            op, values = o, []
        else:
            # We're in the middle of an operation
            if not op:
                raise ValueError('Value without op')
            values.append(o)
    if op:
        yield Op(op, *values)


def _two_ops():
    def add(ops, op):
        f = getattr(operator, 'truediv' if op == 'div' else op)
        ops[op] = f
        if op not in COMMUTATIVE:
            ops['r' + op] = lambda x, y: f(y, x)

    ops = {}
    for op in TWO_OPERATORS:
        add(ops, op)

    ops.update(max=max, min=min, gamma=ops['rpow'])
    return ops


def _join(items, indent='    ', per_line=8):
    lines = []
    for i in range(0, len(items), 8):
        lines.append(indent + ', '.join(items[i:i + 8]) + '\n')
    return ''.join(lines)


TWO_OPERATORS = 'add', 'div', 'mod', 'mul', 'pow', 'sub'
COMMUTATIVE = 'add', 'mul'

ONE_OPERATORS = (
    'acos',
    'acosh',
    'asin',
    'asinh',
    'atan',
    'atanh',
    'ceil',
    'cos',
    'cosh',
    'degrees',
    'erf',
    'erfc',
    'exp',
    'expm1',
    'fabs',
    'floor',
    'gamma',
    'lgamma',
    'log',
    'log10',
    'log1p',
    'log2',
    'radians',
    'sin',
    'sinh',
    'sqrt',
    'tan',
    'tanh',
    'trunc')

OPS = [{k: getattr(math, k) for k in ONE_OPERATORS}, _two_ops()]

OPS_ERROR = """\
Do not understand operator {0}.

One argument operators are:
   %s

Two argument operators are:
   %s
""" % tuple(_join(sorted(o)) for o in OPS)
