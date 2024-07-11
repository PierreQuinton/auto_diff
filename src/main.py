from autodiff import Var, Cos, Ln, Exp, Val

x = Var("x")
f = x+x
f = x**2/1
f2 = f.differentiate(x)

print(f)
print(f2)
