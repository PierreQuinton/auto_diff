from autodiff import *
from graph import plot_one_var_function
from gd import gradient_descent

x = Var("x")
y = Var("y")
z = Var("z")
f = Cos(3 * x - Ln(x ** 2 + 1) / Exp(x + x))
# f = (x - 4) ** 2
# f = Cos(Sin(f))
f = f.simplify()
x_0 = {x: -3.0}
learn_rate = 0.000001

zegrad = gradient_descent(f, x_0, learn_rate, max_iter=100)
print(zegrad)
plot_one_var_function(f, x, zegrad, 1000, learn_rate)
f2 = f.differentiate({x})
print(f2)
