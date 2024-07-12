from autodiff import Var, Cos, Ln, Exp, Val, Neg

x = Var("x")
y = Var("y")
f = 3*x+y
f = f._simplify()
f2 = f.differentiate({x})

print(f)
print()
print(f2)
