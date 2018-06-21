import configparser
from typing import Dict

from RiotCrawler.Exceptions.errors import MissingDefaultItemsError, ExtraItemsError


def _parse_init(config_path: str) -> Dict[str, str]:
    """
    Parses the config.ini file for the required information and returns a dict of that information

    :param config_path: Path to the config file
    :return: Dict of the config file
    """

    config = configparser.ConfigParser(allow_no_value=True)
    config.read(config_path)
    return_dict = {k: v for k, v in config['DEFAULT_INIT'].items()}
    if len(return_dict) > 3:
        raise ExtraItemsError('DEFAULT_INIT has extra items in it')

    # Check for null values in default init
    if any((v is None) or (v == '') for v in return_dict.values()):
        raise MissingDefaultItemsError('Necessary Items in DEFAULT_INIT are missing')
    else:
        return return_dict


def _parse_rest_config(config_path: str) -> Dict[str, str]:
    """
    Parses the rest of the config outside of the necessary init dict

    :param config_path: Path to the config.ini file
    :return: Dict of the config details
    """

    config = configparser.ConfigParser(allow_no_value=True)
    config.read(config_path)

    return_dict = dict()
    parse_items = {k: v for k, v in config.items() if k not in ['DEFAULT_INIT', 'DEFAULT']}
    for item in parse_items:
        return_dict.update({k: v for k, v in parse_items[item].items() if (v != '') and (v is not None)})

    return return_dict


def parse_config(path_to_config: str) -> Dict[str, Dict[str, str]]:
    """
    Parses the full config file and returns { default init: { }, extra: { } }

    :param path_to_config: Path to the config file
    :return: A dict containing the default info and the extra parsed info
    """

    return_dict = dict()
    if not isinstance(path_to_config, str):
        raise TypeError('path_to_config must be of type string')
    else:
        return_dict['default_init'] = _parse_init(path_to_config)
        return_dict['extra'] = _parse_rest_config(path_to_config)

    return return_dict
