import configparser


def get_access_token(path: str) -> str:
    """
    Returns the token given a config.cfg file in the path given
    :param path: directory where the config is
    :return: token
    """
    config = configparser.ConfigParser()
    config.read(f'{path}/config.cfg')
    token = config['ACCESS']['token']
    return token