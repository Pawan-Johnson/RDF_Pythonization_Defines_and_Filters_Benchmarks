import ROOT
import time 

square = """
namespace Numba{
    double square(double x){
        return x*x;
    }
}
"""

add = """
namespace Numba{
    double add(double x, double y){
        return x + y;
    }
}
"""

half = """
namespace Numba{
    double half(double x){
        return x/2;
    }
}
"""

greater = """
namespace Numba{
    double greater(double x, double z){
        return x > z;
    }
}
"""


N  = 20
rdf = ROOT.RDataFrame(2**N).Define("x", "rdfentry_")

N_iter = 25
times = []
for i in range(N_iter):
    if i == 0:
        ROOT.gInterpreter.Declare(square)
        ROOT.gInterpreter.Declare(add)
        ROOT.gInterpreter.Declare(half)
        ROOT.gInterpreter.Declare(greater)
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
        f.write(f"{4000}, {idx}, {times[idx]}, CPP\n")