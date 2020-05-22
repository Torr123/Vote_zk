import numpy as np
import rsa

from zk_snark.qap import r1cs_to_qap
from zk_snark.to_r1cs import code_to_r1cs_with_inputs

(pubkey, privkey) = rsa.newkeys(2048)

func = """
def qeval(x):
    y = x**3
    return y + x + 5
"""


def main():
    k = 10

    r, A, B, C = code_to_r1cs_with_inputs(func, [3])
    Ap, Bp, Cp, Z = r1cs_to_qap(A, B, C)

    with open("CRS", 'w') as crs:
        crs.write(f'{len(Ap)}\n')
        s = np.array([k ** (len(Ap[0]) - i - 1) for i in range(len(Ap[0]))])
        Apx = np.dot(np.array(Ap), s)
        Bpx = np.dot(np.array(Bp), s)
        Cpx = np.dot(np.array(Cp), s)
        for i in range(len(Ap)):
            ai = Apx[i]
            bi = Bpx[i]
            ci = Cpx[i]
            crs.write(''.join('%s\n%s\n%s\n' % (ai, bi, ci)))
        ABCpx = np.dot(np.array(np.array(Ap) + np.array(Bp) + np.array(Cp)), s)
        for i in range(len(Ap)):
            abci = ABCpx[i]
            crs.write(''.join('%s\n' % abci))


if __name__ == '__main__':
    main()
