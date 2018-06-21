import json
import os
import pathlib
from typing import Tuple, Union

import requests


def _create_json_links(link: str) -> Tuple[str, str]:
    """
    Parses the links to the match hisotyr page and returns links to the JSON data.
    There are two relevant JSON's they are of the template:
    https://acs.leagueoflegends.com/v1/stats/game/TRLH1/1002440062?gameHash=a3b08c115923f00d
    https://acs.leagueoflegends.com/v1/stats/game/TRLH1/1002440062/timeline?gameHash=a3b08c115923f00d

    :param link: Link to the match history page
    :return: A list of two links one to the full match JSON and the other the timeline JSON
    """

    link_ext = link[62:]
    link_ext = link_ext.split('/')
    link_ext[1] = link_ext[1].split('?')

    game_ext = f'https://acs.leagueoflegends.com/v1/stats/game/{link_ext[0]}/{link_ext[1][0]}?{link_ext[1][1]}'
    time_ext = f'https://acs.leagueoflegends.com/v1/stats/game/{link_ext[0]}/{link_ext[1][0]}/timeline?{link_ext[1][1]}'

    return game_ext, time_ext


def _save_json(path_to_folder: str, json_link: str, json_data: dict) -> None:
    """
    Saves JSON data to a file

    :param json_link: Link to the JSON data for use in filename only
    :param json_data: JSON data to save to file
    :return: None
    """
    pathlib.Path(path_to_folder).mkdir(parents=True, exist_ok=True)

    split_link = json_link.split('/')
    file_name = f'game_{split_link[6]}_{split_link[7][:10]}.json'
    path = os.path.join(path_to_folder, file_name)

    with open(path, 'a') as jfile:
        json.dump(json_data, jfile, indent=4)


def crawl_json(json_links: tuple, path: Union[None, str] = None, ) -> Union[None, dict]:
    """
    Crawls the JSON data and either saves it to a json file or returns it

    :param json_links: Links to the JSON data for each game
    :param path: The path to the location to save the JSON data if save = True
    :return: JSON data or None
    """
    if not isinstance(json_links, (tuple, list)):
        raise TypeError('json_links must be of type tuple or list')

    if json_links:
        for link in json_links:
            tmp_links = _create_json_links(link)

            r = requests.get(tmp_links[0])
            json_resp1 = r.json()
            r = requests.get(tmp_links[1])
            json_resp2 = r.json()

            concat_json = json_resp1.copy()
            concat_json.update(json_resp2)

            if path is not None:
                _save_json(path, tmp_links[0], concat_json)
            else:
                return concat_json
    else:
        raise Exception('The JSON links passed were empty')
