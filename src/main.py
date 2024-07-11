from autodiff import Var, Cos, Ln, Exp, Val

x = Var("x")
y = Var("y")
f = Cos(3 * x - Ln(x ** 2 + 1) / Exp(x + x))
f = Val(0.0) + Val(1.0)
f = f.simplify()
f2 = f.differentiate(x)

print(f)
print()
print(f2)
