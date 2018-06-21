import pytest

from RiotCrawler.Exceptions.errors import BaseExtError
from RiotCrawler.makeLinks import _create_base_ext, _create_schedule_ext

CORRECT_DICT = {'default_init': {'region': 'all', 'split': 'spring', 'week': 'all'},
                'extra'       : {'lolesports': 'correct_lol_esports', 'year': '2017'}}


def test_default_base_ext():
    pass_dict = {}
    correct = 'https://www.lolesports.com/en_US/'
    res = _create_base_ext(pass_dict)
    assert correct == res


def test_config_base_ext():
    correct_dict = CORRECT_DICT
    corr = correct_dict['extra']['lolesports']
    res = _create_base_ext(correct_dict)
    assert corr == res


def test_config_base_ext_error():
    err_dict = {'extra': {'lolesports': ['errors']}}
    with pytest.raises(TypeError):
        _create_base_ext(err_dict)


def test_base_ext_error_type():
    with pytest.raises(BaseExtError):
        _create_schedule_ext(['asdfas'], {'default_init': 'b', 'extra': 'a'})


def test_base_ext_error_len():
    with pytest.raises(BaseExtError):
        _create_schedule_ext('', {'default_init': 'b', 'extra': 'a'})


def test_links_returned_len():
    res = _create_schedule_ext('na', CORRECT_DICT)
    assert len(res) > 0


def test_link_returned_type():
    res = _create_schedule_ext('na', CORRECT_DICT)
    assert type(res) == list

# TODO: Write more links testing
