import ROOT
import time 

def square(x):
    return x*x

def add(x, y):
    return x + y

def half(x):
    return x/2

def greater(x, z):
    return x > z

N  = 20
rdf = ROOT.RDataFrame(2**N).Define("x", "rdfentry_")

N_iter = 25
times = []
for i in range(N_iter):
    if i == 0:
        square = ROOT.Numba.Declare(["double"], "double")(square)
        add = ROOT.Numba.Declare(["double", "double"], "double")(add)
        half = ROOT.Numba.Declare(["double"], "double")(half)
        greater = ROOT.Numba.Declare(["double", "double"], "bool")(greater)

    Nj = 1000
    # NOps = Nj*4
    start = time.perf_counter()
    for j in range(Nj):
        rdf1 = rdf.Define("y"+str(j), "Numba::square(x)")
        rdf1 = rdf1.Define("z"+str(j), "Numba::add(x, y" + str(j) + ")")
        rdf1 = rdf1.Define("avg"+str(j), "Numba::half(z" + str(j) + ")")
        rdf1 = rdf1.Filter("Numba::greater(avg" + str(j) + ", x)")
    c = rdf1.Sum("x").GetValue()
    del rdf1
    end = time.perf_counter()
    t = end - start
    times.append(t)

with open("Compare.txt", "a") as f:
    for idx, t in enumerate(times):
        f.write(f"{4000}, {idx}, {times[idx]}, Numba\n")
