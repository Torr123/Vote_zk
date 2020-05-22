import numpy as np

from zk_snark.elliptic import get_pg, scalar_mult
from zk_snark.qap import r1cs_to_qap, create_solution_polynomials
from zk_snark.to_r1cs import code_to_r1cs_with_inputs

func = """
def qeval(x):
    y = x**3
    return y + x + 5
"""
voters_dict = {'Novikov': 2, 'Vaganov': 3, 'Panov': 4, 'Molotkov': 5}
voters_list = [2, 3, 4, 5]


def proof(name: str):
    p, G = get_pg()
    with open("CRS", 'r') as crs:
        n = int(crs.readline())
        A, B, C, summ = [], [], [], []

        for i in range(n):
            A.append(float(crs.readline()))
            B.append(float(crs.readline()))
            C.append(float(crs.readline()))

        for i in range(n):
            summ.append(float(crs.readline()))

    if name not in voters_dict:
        voters_dict[name] = 123

    r, A1, B1, C1 = code_to_r1cs_with_inputs(func, [voters_dict[name]])

    a1 = np.sum(np.dot(np.array(A), np.array(r)) + 0.01).round()
    b1 = np.sum(np.dot(np.array(B), np.array(r)) + 0.01).round()
    c1 = np.sum(np.dot(np.array(C), np.array(r)) + 0.01).round()
    abc = np.sum(np.dot(np.array(summ), np.array(r)) + 0.01).round()

    aell = scalar_mult(int(a1), G)
    bell = scalar_mult(int(b1), G)
    cell = scalar_mult(int(c1), G)
    abcell = scalar_mult(int(abc), G)

    with open('Proof', 'w') as f:
        f.write(''.join('%s\n%s\n' % i for i in [aell, bell, cell, abcell]))


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
