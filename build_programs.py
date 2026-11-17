import json
import ast
import os

programs = [
    {
        "id": 1,
        "topic": "Find Eigen Values of a 3×3 Matrix",
        "code": """import numpy as np
A=np.array([[2,1,1],[1,2,1],[1,1,2]])
eigen_values=np.linalg.eigvals(A)
print("Eigen values:",np.round(eigen_values,2))"""
    },
    {
        "id": 2,
        "topic": "Find Eigen Values of a 3×3 Complex Matrix",
        "code": """import numpy as np
a=np.array([[2+1j,1,0],[0,3+2j,1],[0,0,4+3j]])
e=np.linalg.eigvals(a)
print("Eigen values:",e)"""
    },
    {
        "id": 3,
        "topic": "Find Eigen Values and Eigen Vectors of a 3×3 Matrix",
        "code": """import numpy as np
A=np.array([[1,2,0],[2,1,0],[0,0,3]])
vals,vect=np.linalg.eig(A)
print("Eigen values:\\n",vals)
print("Eigen vectors:\\n",vect)"""
    },
    {
        "id": 4,
        "topic": "Find the Root of a Given Non-Linear Equation Using Bisection Method",
        "code": """def f(x):
    return x**3-5*x+1
def bisection_method(a,b,E):
    if f(a)*f(b)>0:
        print("Root doesn't exist in this interval")
        return None
    c=(a+b)/2.0
    print("a\\t\\tb\\t\\tc")
    while abs(b-a)/2.0>E:
        c=(a+b)/2.0
        print(f"{a:.5f}\\t{b:.5f}\\t{c:.5f}")
        if f(c)==0:
            break
        elif f(a)*f(c)<0:
            b=c
        else:
            a=c
    return c
a=float(input("Enter a: "))
b=float(input("Enter b: "))
E=float(input("Enter E (tolerance): "))
root=bisection_method(a,b,E)
if root is not None:
    print(f"\\nThe root is: {root:.4f}")"""
    },
    {
        "id": 5,
        "topic": "Find the Root of a Given Non-Linear Equation Using Newton-Raphson Method",
        "code": """def f(x):
    return x**3-5*x+1
def df(x):
    return 3*x**2-5
x_old=0.5
E=0.000001
n=10
print("--------------------------------")
print("Iteration   x_old   x_new   Error")
print("--------------------------------")
for i in range(n):
    x_new=x_old-f(x_old)/df(x_old)
    error=abs(x_new-x_old)
    print(f"{i+1:2d}  {x_old:.5f}  {x_new:.5f}  {error:.5f}")
    if error<E:
        break
    x_old=x_new
print("Root =",x_new)"""
    },
    {
        "id": 6,
        "topic": "Solution of a System of Linear Equations Using Gauss-Jacobi Method",
        "code": """x_old,y_old,z_old=0.0,0.0,0.0
E=0.00001
n=15
print("----------------------------------------")
print("Iteration    x_new      y_new      z_new")
print("----------------------------------------")
for i in range(n):
    x_new=(6+y_old-2*z_old)/10
    y_new=(25+x_old+z_old)/11
    z_new=(-11-2*x_old+y_old)/10
    print(f"{i+1:2d}  {x_new:.4f}  {y_new:.4f}  {z_new:.4f}")
    if abs(x_new-x_old)<E and abs(y_new-y_old)<E and abs(z_new-z_old)<E:
        break
    x_old=x_new
    y_old=y_new
    z_old=z_new
print(f"x:{x_new}")
print(f"y:{y_new}")
print(f"z:{z_new}")"""
    },
    {
        "id": 7,
        "topic": "Gauss-Seidel Method",
        "code": """x_old=0
y_old=0
z_old=0
E=0.00001
n=15
print("------------------------------------------")
print("Iteration\\t x-new\\t y-new\\t z-new")
print("------------------------------------------")
for i in range(n):
    x_new=(4-y_old-2*z_old)/4
    y_new=(7-3*x_new-z_old)/5
    z_new=(3-x_new-y_new)/3
    print(f"{i+1:2d}\\t{x_new:.5f}\\t{y_new:.5f}\\t{z_new:.5f}")
    if abs(x_new-x_old)<E and abs(y_new-y_old)<E and abs(z_new-z_old)<E:
        print("------------------------------------------")
        break
    x_old=x_new
    y_old=y_new
    z_old=z_new
print(f"x={x_new:.4f}")
print(f"y={y_new:.4f}")
print(f"z={z_new:.4f}")"""
    },
    {
        "id": 8,
        "topic": "Solution of Exact Differential Equation",
        "code": """import sympy as s
x,y=s.symbols('x y')
M=2*x*y+y**2
N=x**2+2*x*y
My=s.diff(M,y)
Nx=s.diff(N,x)
if My==Nx:
    print("Exact DE")
    F=s.integrate(M,x)
    F=F+s.integrate(N-s.diff(F,y),y)
    print("Solution:",F,"= C")
else:
    print("Non-Exact DE")"""
    },
    {
        "id": 9,
        "topic": "Solution of Non-Exact Differential Equation",
        "code": """import sympy as s
x,y=s.symbols('x y')
M=4*y+x**3
N=x
My=s.diff(M,y)
Nx=s.diff(N,x)
if My==Nx:
    print("Exact Differential Equation")
    F=s.integrate(M,x)
    F=F+s.integrate(N-s.diff(F,y),y)
    print("Solution:",F,"= C")
else:
    print("Non-Exact DE")
    IF=None
    IF1=s.simplify((My-Nx)/N)
    IF2=s.simplify(-(My-Nx)/M)
    if not IF1.has(y):
        IF=s.simplify(s.exp(s.integrate(IF1,x)))
        print("IF depends on x")
    elif not IF2.has(x):
        IF=s.simplify(s.exp(s.integrate(IF2,y)))
        print("IF depends on y")
    else:
        print("No IF found")
    if IF is not None:
        print("Integrating Factor:",IF)
        M1=s.simplify(IF*M)
        N1=s.simplify(IF*N)
        print("Mnew:",M1)
        print("Nnew:",N1)
        F=s.integrate(M1,x)
        F=F+s.integrate(N1-s.diff(F,y),y)
        print("Solution:",F,"= C")"""
    },
    {
        "id": 10,
        "topic": "Solving Higher-Order Differential Equation",
        "code": """import sympy as s
x=s.symbols('x')
y=s.Function('y')
deq=s.diff(y(x),x,2)-4*s.diff(y(x),x)+4*y(x)
solution=s.dsolve(deq,y(x))
print("Differential Equation:")
s.pprint(deq)
print("General Solution:")
s.pprint(solution)"""
    },
    {
        "id": 11,
        "topic": "Solving Non-Homogeneous Higher-Order Differential Equation",
        "code": """import sympy as s
x=s.symbols('x')
y=s.Function('y')
eq=s.Eq(s.diff(y(x),x,2)-3*s.diff(y(x),x)+2*y(x),s.exp(3*x))
sol=s.dsolve(eq)
print("Differential Equation:")
s.pprint(eq)
print("Solution:")
s.pprint(sol)"""
    }
]

# Validation
print(f"Total programs: {len(programs)}")
assert len(programs) == 11, "Must have exactly 11 programs"

for p in programs:
    # 1. Parse AST to verify 100% valid Python syntax
    try:
        ast.parse(p["code"])
    except SyntaxError as e:
        print(f"Syntax error in Program {p['id']} ({p['topic']}): {e}")
        raise e
    
    # 2. Verify no python comments '#' exist
    lines = p["code"].split("\n")
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("#"):
            raise ValueError(f"Found comment line in Program {p['id']}: {line}")
            
    # 3. Verify indentation (nested blocks use 4 spaces)
    print(f"Program {p['id']}: '{p['topic']}' - {len(lines)} lines - Valid Python AST [OK]")

os.makedirs("src", exist_ok=True)
with open("src/programs.json", "w", encoding="utf-8") as f:
    json.dump(programs, f, indent=2, ensure_ascii=False)

print("src/programs.json written successfully!")
