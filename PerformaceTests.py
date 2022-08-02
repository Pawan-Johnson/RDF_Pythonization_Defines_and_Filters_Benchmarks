import enum
import matplotlib.pyplot as plt
import ROOT
import numpy as np
import time
import numba as nb
from tqdm import tqdm

N = 20
rdf = ROOT.RDataFrame(2**N).Define("x", "rdfentry_")

# 10 Functions for Defines and Filter


def power(x, n):
    return x**n


def sqrt(x):
    return np.sqrt(x)


def vectorize(px, py, pz):
    return np.array([px, py, pz])


def magnitude(x):
    # return np.sqrt(x[0]**2 + x[1]**2 + x[2]**2)
    return np.linalg.norm(x)


def calc_trans(px2, py2):
    return np.sqrt(px2 + py2)


def calc_m(E, p):
    return np.sqrt(E*E - p*p)


def phi(px, py):
    return np.arctan2(px, py)


def eta(pt, pz):
    return np.arctan2(pt, pz)


def pe(phi, eta):
    return phi/eta


def filter_m(m):
    return m > 0


N_iter = 25
times = {}
x = []
for nops in range(1, 5):
    times[nops*100*10] = []
    x.append(nops*100*10)
    for i in tqdm(range(N_iter)):
        start = time.perf_counter()
        rdf = ROOT.RDataFrame(2**N).Define("x", "rdfentry_")
        Nj = 100*nops
        for j in range(Nj):
            rdf1 = rdf.Define("y" + str(j), power, extra_args={"n": 2})
            rdf1 = rdf1.Define("z" + str(j), sqrt, ["x"])
            rdf1 = rdf1.Define("coord" + str(j), vectorize,
                               ["x", "y" + str(j), "z" + str(j)])
            rdf1 = rdf1.Define("r" + str(j), magnitude, ["coord" + str(j)])
            rdf1 = rdf1.Define("trans" + str(j), calc_trans,
                               ["x", "y" + str(j)])
            rdf1 = rdf1.Define("m" + str(j), calc_m,
                               ["z" + str(j), "trans" + str(j)])
            rdf1 = rdf1.Define("phi" + str(j), phi, ["x", "y" + str(j)])
            rdf1 = rdf1.Define("eta" + str(j), eta,
                               ["trans" + str(j), "z" + str(j)])
            rdf1 = rdf1.Define("pe" + str(j), pe,
                               ["phi" + str(j), "eta" + str(j)])
            rdf1 = rdf1.Filter(filter_m, ["m" + str(j)])
        c = rdf1.Sum("x").GetValue()
        del rdf1
        end = time.perf_counter()
        times[nops*100*10].append(end - start)
        # print(c)

with open("res.txt", "a") as f:
    for i in times:
        for idx, t in enumerate(times[i]):
            f.write(f"{i}, {idx}, {t}\n")

