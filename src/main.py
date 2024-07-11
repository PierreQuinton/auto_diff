from autodiff import Var, Cos, Ln, Exp, Val

x = Var("x")
f = x+x
f = Cos(3**2*x)
f2 = f.differentiate(x)

print(f)
print(f2)
