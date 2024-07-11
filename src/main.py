from autodiff import Var, Cos, Ln, Exp, Val

x = Var("x")
f = Cos(3 * x - Ln(x ** 2 + 1) / Exp(x + x))

f = Val(3.0)
f2 = f.differentiate(x)

print(f)
print(f2)
