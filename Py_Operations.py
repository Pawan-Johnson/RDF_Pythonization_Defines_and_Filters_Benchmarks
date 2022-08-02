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
        pass
    Nj = 1000
    # NOps = 400
    start = time.perf_counter()
    for j in range(Nj):
        rdf1 = rdf.Define("y"+str(j), square, ["x"])
        rdf1 = rdf1.Define("z"+str(j), add, ["x", "y"+str(j)])
        rdf1 = rdf1.Define("avg"+str(j), half, ["z"+str(j)])
        rdf1 = rdf1.Filter(greater, ["avg"+str(j), "x"])
    c = rdf1.Sum("x").GetValue()
    del rdf1
    end = time.perf_counter()
    t = end - start
    times.append(t)

with open("Compare.txt", "a") as f:
    for idx, t in enumerate(times):
        f.write(f"{4000}, {idx}, {times[idx]}, Python\n")


