# mpchebdif.sage
# Arbitrary-precision Chebyshev differentiation matrices (mpmath port of chebdif by Weideman & Reddy).
#
#   xgrid, Ds = mpchebdif(N, M)
#
# xgrid : the N+1 Chebyshev-Gauss-Lobatto points x_j = cos(pi j / N), from +1 down to -1 (mpmath matrix)
# Ds    : list [D1, D2, ..., DM] of (N+1)x(N+1) differentiation matrices on [-1, 1]
#
# Plain Python syntax, so it can be loaded from Sage with load("mpchebdif.sage")
# or imported from Python after renaming to .py.
import mpmath as mp


def mpchebdif(N, M):
    N = int(N)
    n = N + 1
    x = mp.matrix(n, 1)
    for j in range(n):
        x[j] = mp.cos(mp.pi * j / N)
    c = [mp.mpf(2) if j in (0, N) else mp.mpf(1) for j in range(n)]
    c = [c[j] * (-1) ** j for j in range(n)]
    D = mp.zeros(n, n)
    for i in range(n):
        for j in range(n):
            if i != j:
                D[i, j] = (c[i] / c[j]) / (x[i] - x[j])
    for i in range(n):  # negative-sum trick for the diagonal
        D[i, i] = -sum(D[i, j] for j in range(n) if j != i)
    Ds = [D]
    for _ in range(1, int(M)):
        Ds.append(Ds[-1] * D)
    return x, Ds
