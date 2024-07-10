from functions import Function, Var, Val
from neg import Neg
import math



class Cos(Function):

    def __init__(self, func: Function):
        self.func = func
        super().__init__([self.func])


    def _substitute(self, substitutions: dict[Function, Function]) -> Function:
        return Cos(self.func.substitute(substitutions))


    def _partial(self, func: Function) -> Function:
        return Neg(Sin(self.func))

        
class Sin(Function):

    def __init__(self, func: Function) -> None:
        self.func = func
        super().__init__([self.func])

        
    def _substitute(self, substitutions: dict[Function, Function]) -> Function:
        return Sin(self.func.substitute(substitutions))

   
    def _partial(self, func: Function) -> Function:
           return Cos(self.func)
