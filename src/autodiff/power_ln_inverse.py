from functions import Function, Val, Product
from exp import Exp
import math


class Power(Exp):

    def __init__(self, base: Function, exp: Function) -> None:
        func = Product(Ln(base), exp)
        super().__init__(func)


class Inverse(Power):

    def __init__(self, function: Function) -> None:
        super().__init__(function, Val(-1.0))


class Ln(Function):

    def __init__(self, func: Function) -> None:
        self.func = func
        super().__init__([self.func])
         
    
    def _substitute(self, substitutions: dict[Function, Function]) -> Function:
        return Ln(self.func.substitute(substitutions))
    
    
    def _partial(self, func: Function) -> Function:
        return Inverse(self.func)
