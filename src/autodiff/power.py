from functions import Function, Var, Val, Sum, Product
from ln import Ln
from exp import Exp


class Power(Exp):

    def __init__(self, base: Function, exp: Function) -> None:
        func = Product(Ln(base), exp)
        super().__init__(func)


class Inverse(Power):

    def __init__(self, function: Function) -> None:
        super().__init__(function, Val(-1.0))
