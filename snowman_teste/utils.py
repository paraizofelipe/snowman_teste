import hashlib
import configparser

from snowman_teste import project


def read_conf_file(path_conf):
    try:
        datasource_parser = configparser.ConfigParser()
        datasource_parser.read(path_conf)
        return datasource_parser
    except FileExistsError as error:
        raise error
    except Exception as error:
        raise error


def get_conf_key(key):
    try:
        dict_conf = read_conf_file(project.CONFIG_FILE)
        return dict_conf[key]

    except Exception:
        raise


def hash_password(password, salt):
    """
    Função para encodar a senha em hash
    :param password:
    :param salt:
    :return: Codificação hash Hex SHA512 da senha fornecida
    """
    password = str(password).encode('utf-8')
    salt = str(salt).encode('utf-8')
    return hashlib.sha512(password + salt).hexdigest()