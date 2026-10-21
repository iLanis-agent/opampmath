import json, subprocess, sys
from fractions import Fraction
sys.path.insert(0, '.')

def dec(v, places=2):
    # v is a Fraction of hundredths; half-up already applied upstream
    if v < 0: return "-" + dec(-v, places)
    base = 10**places
    ip = v.numerator * 10**0 // 1
    # v represents hundredths as an integer Fraction
    n = v.numerator // v.denominator
    s = str(n // base); f = str(n % base).zfill(places).rstrip("0")
    return s + "." + f if f else s

def hu(num, den): return Fraction((2*num + den)//(2*den)) if isinstance(num, int) and num >= 0 else Fraction((2*num + den) - ((2*num + den) % (2*den)), 2*den)

def ohm(r): return f"{r} Ω"
def vfmt(v100): return f"{dec(Fraction(v100))} V"

def noninv(f, g, v):
    gain = hu((f+g)*100, g); out = hu(v*(f+g), g)
    return f"A {ohm(f)} feedback over a {ohm(g)} to ground gives a gain of {dec(gain)}. {vfmt(v)} in comes out at {vfmt(out)}."
def inv(f, n, v):
    gain = hu(f*100, n); out = hu(v*f, n)
    return f"With {ohm(f)} feedback and {ohm(n)} in, the gain is {'-' if gain else ''}{dec(gain)}. {vfmt(v)} in comes out at {'-' if out else ''}{vfmt(out)}."
def sm(f, a, x, b, y):
    out = hu(f*(x*b + y*a), a*b)
    return f"With {ohm(f)} feedback, {vfmt(x)} through {ohm(a)} and {vfmt(y)} through {ohm(b)} sum to {'-' if out else ''}{vfmt(out)}."

cases = []
import random
random.seed(727)
cases.append(dict(fn="noninv", args=["10000","1000","0.2"], expect=noninv(10000,1000,20)))
cases.append(dict(fn="inv", args=["10000","2000","0.2"], expect=inv(10000,2000,20)))
cases.append(dict(fn="sm", args=["10000","10000","0.5","5000","1"], expect=sm(10000,10000,50,5000,100)))
for _ in range(30):
    f = random.randint(1,1000000); g = random.randint(1,1000000); v = random.randint(1,1000)
    cases.append(dict(fn="noninv", args=[str(f),str(g),f"{v/100:g}"], expect=noninv(f,g,v)))
    cases.append(dict(fn="inv", args=[str(f),str(g),f"{v/100:g}"], expect=inv(f,g,v)))
    a = random.randint(1,1000000); b = random.randint(1,1000000); x = random.randint(1,1000); y = random.randint(1,1000)
    cases.append(dict(fn="sm", args=[str(f),str(a),f"{x/100:g}",str(b),f"{y/100:g}"], expect=sm(f,a,x,b,y)))
errcases = [
  ("noninv", ["0","1000","0.2"]), ("noninv", ["1000001","1000","0.2"]), ("noninv", ["10000","1000","0"]), ("noninv", ["10000","1000","10.001"]), ("noninv", ["1.5","1000","0.2"]),
  ("inv", ["10000","0","0.2"]), ("inv", ["10000","2000","10.01"]), ("sm", ["10000","10000","0.5","0","1"]),
]
json.dump({"cases": cases, "errors": errcases}, open("expected.json","w"), ensure_ascii=False, indent=1)
open("expected.json","a").write("\n")
print("expected.json written:", len(cases), "cases")
