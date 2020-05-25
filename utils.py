import configparser

from sqlitedict import SqliteDict

db = SqliteDict('./db.sqlite', autocommit=True)


def fill_config(host, port):
    config = configparser.ConfigParser()
    config['DEFAULT']['host'] = host
    config['DEFAULT']['port'] = str(port)
    with open('config.ini', 'w') as configfile:
        config.write(configfile)


def validate(s):
    return s in ('Novikov', 'Vaganov')


def get_port_host():
    parser = configparser.ConfigParser()
    parser.read('config.ini')
    return (parser['DEFAULT']['host'],int(parser['DEFAULT']['port']))
