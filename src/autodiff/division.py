from functions import Function, Var, Val
from product import Product, Neg
from sum import Sum
from power import Power, Inverse
from compose import Compose

class _Division(Function):

    def __init__(self, numerator: Function, denominator: Function):
        self.numerator = numerator
        self.denominator = denominator
        
        super().__init__()
    

    def _evaluate(self, values: dict[Var, Val]) -> Val:
        num_value = self.numerator._evaluate(values)
        denom_value = self.denominator._evaluate(values)
        if denom_value == 0:
            raise ZeroDivisionError("Division by 0.")
        return num_value / denom_value



    def differentiate(self, var: Var) -> Function:
# (f'g-fg')/g^2
        f_prime_g = Product([self.numerator.differentiate(var),self.denominator])
        f_g_prime = Product([self.numerator,self.denominator.differentiate(var)])
        numerator_diff = Sum([f_prime_g,Neg(f_g_prime)])
        denominator_squared_inverse= Inverse(Power(2,[self.denominator]))
        return Product(numerator_diff, denominator_squared_inverse)
    
    

class Division(Compose):

    def __init__(self, func: Function) -> None:
        super().__init__(func, _Division())

    

    def __repr__(self):
        string = """This class handles division and division differentiation"""