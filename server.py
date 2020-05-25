import socket

from zk_snark.verify import verifier, voters_list
from utils import fill_config


def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        print('Socket created')

        sock.bind(('', 0))
        sock.listen()
        fill_config(port=sock.getsockname()[1], host='localhost')

        while True:
            conn, addr = sock.accept()
            print(f'Connected with {addr[0]}:{addr[1]}')

            user = conn.recv(1024).decode()
            print(f'username: {user}')

            answers = [verifier(i) for i in range(len(voters_list))]
            valid = 0 in answers
            print(valid)

            conn.send(b'ok' if valid else b'not ok')
            print('validation completed')


if __name__ == '__main__':
    main()
