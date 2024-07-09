from functions import Function
from sum import Sum
from neg import Neg


class Substraction(Sum):
    def __init__(self, function_1: Function, function_2: Function) -> None:
        super().__init__([function_1, Neg(function_2)])
