import socket

from zk_snark.proof import proof
from utils import get_port_host


def main(name='noname'):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        host , port = get_port_host()
        sock.connect((socket.gethostbyname(host),port))
        proof(name)

        sock.sendall(str.encode(name))
        print('Message sent successfully')

        reply = sock.recv(4096)
        return reply.decode() == 'ok'


if __name__ == '__main__':
    main()
