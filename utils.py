import configparser

from sqlitedict import SqliteDict

db = SqliteDict('./db.sqlite', autocommit=True)


def fill_config(port):
    config = configparser.ConfigParser()
    config['DEFAULT']['port'] = str(port)
    with open('config.ini', 'w') as configfile:
        config.write(configfile)


def validate(s):
    return s in ('Novikov', 'Vaganov')


def get_port():
    parser = configparser.ConfigParser()
    parser.read('config.ini')
    return int(parser['DEFAULT']['port'])
