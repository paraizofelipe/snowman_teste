import os
import configparser


def get_conf(path_conf):
    try:
        datasource_parser = configparser.ConfigParser()
        datasource_parser.read(path_conf)
        return datasource_parser
    except FileExistsError as error:
        raise error
    except Exception as error:
        raise error


PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIG_PATH = os.path.join(PATH, 'snowman_teste/confs/')
CONFIG_FILE = os.path.join(CONFIG_PATH, 'snowman.ini')

CONFIG = get_conf(CONFIG_FILE)


print(PATH)