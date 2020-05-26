import numpy as np

from zk_snark.elliptic import get_pg, scalar_mult
from zk_snark.qap import r1cs_to_qap, create_solution_polynomials
from zk_snark.to_r1cs import code_to_r1cs_with_inputs
from sqlitedict import SqliteDict
import zlib, pickle, sqlite3
from decimal import Decimal

voters_dict = SqliteDict('./Trusted_users_serv.sqlite', autocommit=True)

func = """
def qeval(x):
    y = x**3
    return y + x + 5
"""

voters_list = []

for i in voters_dict.values():
	voters_list.append(i)


def verifier(index):
    p, G = get_pg()

    r, A, B, C = code_to_r1cs_with_inputs(func, [voters_list[index]])
    Ap, Bp, Cp, Z = r1cs_to_qap(A, B, C)
    Apoly, Bpoly, Cpoly, sol = create_solution_polynomials(r, Ap, Bp, Cp)
    k = 10
    s = np.array([k ** (len(Ap[0]) - 1 - i) for i in range(len(Ap[0]))])

    a = (sum(Apoly * s) + 0.01).round()
    b = (sum(Bpoly * s) + 0.01).round()
    c = (sum(Cpoly * s) + 0.01).round()
    sum_abc = (sum((np.array(Apoly) + np.array(Bpoly) + np.array(Cpoly)) * s) + 0.01).round()

    aell = scalar_mult(int(a), G)
    bell = scalar_mult(int(b), G)
    cell = scalar_mult(int(c), G)
    abcell = scalar_mult(int(sum_abc), G)

    with open('Proof', 'r') as f:
        aell1 = (int(f.readline()), int(f.readline()))
        bell1 = (int(f.readline()), int(f.readline()))
        cell1 = (int(f.readline()), int(f.readline()))
        abcell1 = (int(f.readline()), int(f.readline()))

        for elem1, elem2 in zip([aell, bell, cell, abcell], [aell1, bell1, cell1, abcell1]):
            for i in range(2):
                if elem1[i] != elem2[i]:
                    return -1
    return 0
