import datetime
import warnings
from typing import Dict, List, Tuple

from RiotCrawler.Exceptions.errors import BaseExtError, RegionError, SplitError


def _create_base_ext(config_dict: Dict[str, Dict[str, str]]) -> str:
    """
    Parses the config dict to get the necessary parts to create the lolesports base extension

    :param config_dict: Dict parsed from the config.ini file
    :return: A string containing the base extension
    """

    try:
        if not isinstance(config_dict['extra']['lolesports'], str):
            raise TypeError(f'Expected type string got type {type(config_dict["extra"]["lolesports"])}')
        base_ext = config_dict['extra']['lolesports']

    except KeyError:
        base_ext = 'https://www.lolesports.com/en_US/'

    return base_ext


def _create_schedule_ext(base_ext: str, config_dict: Dict[str, Dict[str, str]]) -> List[str]:
    """
    Adds the region, split, and year to the base extension

    :param config_dict: Dict returned from the config.ini
    :param base_ext: The base link created from _create_base_ext
    :return: A list of strings with the extensions
    """

    default_init = config_dict['default_init']
    extra = config_dict['extra']
    links = list()

    if not isinstance(base_ext, str) or (len(base_ext) == 0):
        raise BaseExtError('Invalid base ext provided must be type str, and greater than 0 in length. ')

    # Adding the region to the base link and checking to make sure it is valid
    if default_init['region'] not in ['all', 'na', 'eu', 'lck', 'lms', 'acad', 'academy']:
        raise RegionError('Invalid region provided. Must be one of all, lck, na, eu, lms, acad, or academy')
    else:
        if default_init['region'].lower() in ['na', 'all']:
            links.append(f'{base_ext}na-lcs/na_')
        if default_init['region'].lower() in ['eu', 'all']:
            links.append(f'{base_ext}eu-lcs/eu_')
        if default_init['region'].lower() in ['lms', 'all']:
            links.append(f'{base_ext}lms/lms_')
        if default_init['region'].lower() in ['lck', 'all']:
            links.append(f'{base_ext}lck/lck_')
        if default_init['region'].lower() in ['acad', 'academy', 'all']:
            links.append(f'{base_ext}na-academy/na_academy_')

    # Adding the year if one is provided
    try:
        links = [f'{l}{extra["year"]}_' for l in links.copy()]
    except KeyError:
        links = [f'{l}{datetime.datetime.now().year}_' for l in links.copy()]
        warnings.warn('Date was set to current year, specify year in config.ini if another year is wanted')

    if default_init['split'].lower() not in ['summer', 'spring', 'all']:
        raise SplitError('Split must be one of summer, spring, or all')
    else:
        if default_init['split'].lower() != 'all':
            links = [f'{l}{default_init["split"]}/schedule/' for l in links.copy()]
        else:
            tmp = links.copy()
            links = [f'{l}spring/schedule/' for l in links.copy()]
            links.extend([f'{l}summer/schedule/' for l in tmp])

    return links


def _handle_week(links: List[str], config_dict: Dict[str, Dict[str, str]]) -> Tuple[str]:
    """
    Creates the final full link by parseing the weeks variable

    :param links: A list of links to add the week property too. Created by _create_schedule_ext
    :param config_dict: The config dict of the config.ini
    :return: A tuple of full links to the lolesports schedule page
    """
    week = config_dict['default_init']['week']
    playoff_exts = ['Wild%20Card', 'Round%201', 'Round%202', 'Round%203', 'Finals', 'Quarterfinals', 'Semifinals']

    try:
        if config_dict['extra']['flag'].lower() == 'true':
            try:
                week = range(1, int(week) + 1)
            except ValueError:
                pass
        else:
            try:
                week = int(week)
            except ValueError:
                pass
    except KeyError:
        try:
            week = int(week)
        except ValueError:
            pass

    if not isinstance(links, list) or (len(links) == 0):
        raise Exception('Invalid links provided. Must be of type list and have length greater than 0.')

    if isinstance(week, range):
        return tuple(f'{l}regular_season/{i}' for i in week for l in links)
    elif isinstance(week, int):
        return tuple(f'{l}regular_season/{week}' for l in links)
    else:
        if week.lower() == 'all':
            l1 = [f'{l}regular_season/{i}' for i in range(1, 10) for l in links]

            if config_dict['default_init']['region'] in ['all', 'lck', 'lms']:
                l1.extend([f'{l}regular_season/10' for l in links])

            l2 = [f'{l}playoffs/{p}' for p in playoff_exts for l in links]
            l1.extend(l2)
            return _clean_up_links(l1)

        elif week.lower() == 'playoffs':
            l1 = [f'{l}playoffs/{p}' for p in playoff_exts for l in links]
            return _clean_up_links(l1)

        else:
            l1 = [f'{l}playoffs/{config_dict["default_init"]["week"]}' for l in links]
            return _clean_up_links(l1)


def _clean_up_links(links: List[str]) -> Tuple[str]:
    """
    Cleans up links by removing known dead links

    :param links: A list of links to remove dead links from
    :return: A tuple of good links
    """
    final_list = links.copy()
    for l in links:
        if ('%20' in l) and ('-' in l):
            final_list.remove(l)
    if len(final_list) != 0:
        return tuple(final_list)
    else:
        warnings.warn('All links were removed during cleanup as they were invalid links. This usually happens when '
                      'one of NA, EU, or Academy were provided with an invalid playoff specification like '
                      'Wild%20Card or Round%201')
        return tuple(final_list)


def create_links(config_dict: Dict[str, Dict[str, str]]) -> Tuple[str]:
    """
    Will create a list of links to the schedule page on lolesports. From here you can find all the match histories
    :param config_dict: The configuration dict created from the config.ini file
    :return: A tuple of links
    """

    base_ext = _create_base_ext(config_dict)
    links = _create_schedule_ext(base_ext, config_dict)
    return _handle_week(links, config_dict)
