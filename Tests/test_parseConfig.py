import pytest

from RiotCrawler.Exceptions.errors import MissingDefaultItemsError, ExtraItemsError
from RiotCrawler.parseConfig import _parse_init, _parse_rest_config, parse_config


def test_raise_missing_default_init():
    with pytest.raises(KeyError):
        _parse_init('./config_files/error_config.ini')


def test_bad_file_path():
    with pytest.raises(KeyError):
        _parse_init('askldjf.ini')


def test_none_in_default_init():
    with pytest.raises(MissingDefaultItemsError):
        _parse_init('./config_files/missing_default_config.ini')


def test_dict_return():
    correct = {'region': 'all', 'split': 'spring', 'week': 'all'}
    res = _parse_init('./config_files/correct_config.ini')
    assert res == correct


def test_extra_items():
    with pytest.raises(ExtraItemsError):
        _parse_init('./config_files/extra_config.ini')


def test_extra_return():
    correct = {'lolesports': 'https://www.lolesports.com/en_US/', 'year': '2017'}
    res = _parse_rest_config('./config_files/correct_config.ini')
    assert res == correct


def test_no_empty():
    res = _parse_rest_config('./config_files/extra_config.ini')
    with pytest.raises(KeyError):
        res['flag']


def test_non_str_path():
    with pytest.raises(TypeError):
        parse_config(['adfa', 10])


def test_correct_final_dict():
    correct = {'default_init': {'region': 'all', 'split': 'spring', 'week': 'all'},
               'extra'       : {'lolesports': 'https://www.lolesports.com/en_US/', 'year': '2017'}}
    res = parse_config('./config_files/correct_config.ini')
    assert correct == res


def test_len_final_dict():
    res = parse_config('./config_files/correct_config.ini')
    assert len(res) == 2


def test_errors_final_config():
    with pytest.raises(KeyError):
        parse_config('./config_files/error_config.ini')
