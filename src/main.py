from autodiff import Var, Cos, Ln, Exp, Val, Neg

x = Var("x")
y = Var("y")
f = Cos(3 * x - Ln(x ** 2 + 1) / Exp(x + x))
f = x + Neg(Val(0.0))
f = x*x - x
f = f.simplify()
f2 = f.differentiate(x)

print(f)
print()
print(f2)
