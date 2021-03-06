from mpi4py import MPI
import random
import numpy as np
from math import sqrt


comm = MPI.COMM_WORLD
size = comm.size
rank = comm.rank

l = size * 10

data = []
chunks = []


if rank == 0:
    data = [random.randint(0, 10) for _ in range(l)]
    chunks = [data[i*(l // size):(i+1)*(l // size)] for i in range(size)]

block = comm.scatter(chunks)
s = sum(block)
sums = comm.gather(s)

mean = None
if rank == 0:
    mean = sum(sums) / l

mean = comm.bcast(mean)

p_std = 0

for d in block:
    p_std += sqrt((d - mean) ** 2.0)

p_stds = comm.gather(p_std)

if rank == 0:
    std = sum(p_stds) / (l - 1)

    print("Avg: %f" % mean)
    print("Std: %f" % std)
