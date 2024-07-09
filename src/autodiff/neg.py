from functions import Function, Val, Var
from product import Product


class Neg(Product):
    
    def __init__(self, function: Function):
        super().__init__([Val(-1), function])
