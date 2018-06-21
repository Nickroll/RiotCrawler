import warnings
from typing import Union

from .crawlJSON import crawl_json
from .makeLinks import create_links
from .matchCrawler import get_match_history_links
from .parseConfig import parse_config


class RiotCrawl(object):
    """
    A crawler for Riot's lolesports.com schedule page for each of lms, lck, na, eu, and na-academy. LPL is not yet
    supported due to no match history links on the pages. The crawler works by reading a config.ini file to see what
    data is requested and then creating a set of links for that data. The links are then followed and the match history
    JSON'S retrieved and either saved on disk or returned. Saving is recommended.

    Usage with out returning links and saving JSON data to file:

    >>> rc = RiotCrawl('./path_to_config.ini')
    >>> rc.make_links()
    >>> rc.match_history_links()
    >>> rc.get_json(path='path_to_folder')


    Usage with returning links and JSON

    >>> rc = RiotCrawl('./path_to_config.ini')
    >>> schedule_links = rc.make_links(inplace=False)
    >>> match_links = rc.match_history_links(schedule_links, inplace=False)
    >>> json = rc.get_json(match_links)

    ***** WARNING *****

    Running the following command will run make_links(), match_history_links(), and get_json() and save to a file. This
    will take a long time depending upon how many links were provided. Inplace is assumed and the JSON data is saved to
    the provided path

    >>> rc.run_all(path='path_to_folder')
    """

    def __init__(self, config_file_path: str):
        """
        Creates the RiotCrawl class from a config_file path.
        :param config_file_path: Path to the config.ini file
        """

        self.config_dict = parse_config(config_file_path)
        self.schedule_links = None
        self.match_links = None

    def make_links(self, inplace: bool = True) -> Union[None, tuple]:
        """
        Creates links to the schedule page from which the match history links can be found

        :param inplace: Inplace tuple creation and stored in RiotCrawl.schedule_links. Else returns tuple of links.
        :return: None or a tuple of links to the schedule page
        """

        if inplace:
            self.schedule_links = create_links(self.config_dict)
            return None
        else:
            return create_links(self.config_dict)

    def match_history_links(self, schedule_links: tuple = None, xpath: str = '/matches/',
                            css_selector: str = '.stats-link',
                            inplace: bool = True) -> Union[None, tuple]:
        """
        Finds the links to the full match history pages and returns them as a tuple or modifies inplace.

        :param schedule_links: Links to the schedule page of lolesports from which match history links can be found
        :param xpath: The xpath selector for the match history links. Don't change unless Riot modifies their website
        :param css_selector: The css selector from which the specific stats links can be found.
        :param inplace: If True will store results in RiotCrawl.match_links. Else returns a tuple of links
        :return: None or a tuple of links
        """

        if schedule_links is None:
            schedule_links = self.schedule_links

        if inplace:
            self.match_links = get_match_history_links(schedule_links, xpath, css_selector)
            return None
        else:
            return get_match_history_links(schedule_links, xpath, css_selector)

    def get_json(self, match_links: tuple = None, path: Union[None, str] = None) -> Union[None, dict]:
        """
        Will return the JSON information as a dict that includes the total match history as well as the timeline stats

        :param match_links: Links to the match history page
        :param path: A folder path to save the JSON information.
        :return: None or a dict of JSON stats
        """

        if match_links is None:
            match_links = self.match_links

        if path is not None:
            crawl_json(match_links, path)
        else:
            return crawl_json(match_links)

    def run_all(self, path: str) -> None:
        """
        Will run all of the commands necessary to download the JSON data and save it to the path specified.

        :param path: A path to a folder for saving the information
        :return: None
        """
        warnings.warn('This may take a long time depending on amount of game information to collect')

        self.make_links()
        print('Links made')
        print('Getting the match history links, may take a while')
        self.match_history_links()
        print('Match history links made')
        print('Getting JSON information now, may take a while')
        self.get_json(path=path)
        print('Done!!!')
