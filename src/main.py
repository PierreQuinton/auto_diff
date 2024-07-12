from autodiff import *
from gd import gradient_descent

x = Var("x")
y = Var("y")
z = Var("z")
# f = Cos(3 * x - Ln(x ** 2 + 1) / Exp(x + x))
f = (x -4) ** 2 + y ** 2
f = f.simplify()
x_0 = {x: 3.0, y: -3.0}

LEgrad = gradient_descent(f, x_0, 0.1)
print(LEgrad)
print(f.evaluate(LEgrad))

# f2 = f.differentiate({x})
