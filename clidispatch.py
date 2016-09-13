"""
>>> @Cli.register
... def a_function(x, y):
...     return x + y
>>> @Cli.register
... def one_two_three(ex, why=1, zee=2):
...     return 1 * ex + 2 * why + 3 * zee
>>> Cli.dispatch('--a-function', 4, 5)
9
>>> Cli.dispatch('--one-two-three', 1)
9
"""


import doctest
from functools import partial
from inspect import signature, Parameter
import sys


class _final(partial):
    def __call__(instance, *args, **kwargs):
        super().__call__()


class Cli:
    _reg = {}
    _usage = ['USAGE:']
    _usage_pre = '\tpython %s' % sys.argv[0]

    @classmethod
    def register(cls, fn):
        key = '--' + '-'.join(fn.__name__.split('_'))
        cls._reg[key] = fn
        cls._usage.append('%s %s %s' % (cls._usage_pre, key, cls._build_argspec(fn)))
        return fn

    @classmethod
    def dispatch(cls, key, *args, **kwargs):
        if key is None:
            return cls.usage()
        return cls._reg[key](*args, **kwargs)
    
    @classmethod
    def usage(cls):
        print('\n'.join(cls._usage))

    @classmethod
    def _build_argspec(cls, fn):
        specs = []
        params = signature(fn).parameters
        for proxymap, param in params.items():
            if param.default is not Parameter.empty:
                specs.append('[%s=%s]' % (param.name, param.default))
            else:
                specs.append('<%s>' % param.name)
        return ' '.join(specs)


if __name__ == '__main__':
    doctest.testmod()
