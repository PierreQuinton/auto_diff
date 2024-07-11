from autodiff import Var, Cos, Ln, Exp

x = Var("x")
f = Cos(3 * x - Ln(x ** 2 + 1) / Exp(x + x))

f2 = f.differentiate()

print(f)
print(f2)
