import numpy as np

from zk_snark.elliptic import get_pg, scalar_mult
from zk_snark.qap import r1cs_to_qap, create_solution_polynomials
from zk_snark.to_r1cs import code_to_r1cs_with_inputs
from sqlitedict import SqliteDict
import zlib, pickle, sqlite3

def my_encode(obj):
	return sqlite3.Binary(zlib.compress(pickle.dumps(obj, pickle.HIGHEST_PROTOCOL)))
def my_decode(obj):
	return pickle.loads(zlib.decompress(bytes(obj)))

voters_dict = SqliteDict('./Trusted_users_app.sqlite', autocommit=True, encode=my_encode, decode=my_decode)

voters_dict['Novikov'] = 2
voters_dict['Vaganov'] = 3
voters_dict['Panov'] = 4
voters_dict['Molotkov'] = 5

func = """
def qeval(x):
    y = x**3
    return y + x + 5
"""

voters_list = [voters_dict['Novikov'], voters_dict['Vaganov'], voters_dict['Panov'], voters_dict['Molotkov']]


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
