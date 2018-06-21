from typing import Tuple

from requests_html import HTMLSession


def get_match_history_links(schedule_links: Tuple[str], xpath: str = None,
                            css_selector: str = None) -> tuple:
    """
    Crawls the schedule page of lolesports to find the match history pages and return the links to them

    :param schedule_links: A Tuple of links to the lolesports schedule page
    :param xpath: The xpath selector for the links to the game pages
    :param css_selector: The class for the links to the full match history pages.
    :return: A tuple of links to the match history pages
    """
    if any([xpath is None, css_selector is None]):
        raise ValueError('xpath and css_selector must not be None')

    if not isinstance(schedule_links, (list, tuple)):
        raise TypeError('The links provided were not of type list or tuple')

    session = HTMLSession()
    match_history_list = list()

    for link in schedule_links:
        r = session.get(link)
        r.html.render(sleep=10)
        tmp_next = r.html.xpath('//a[contains(@href, "{}")]'.format(xpath))
        next_link = list()

        for nl in tmp_next:
            next_link.extend(([h for h in nl.absolute_links]))

        for l in next_link:
            r = session.get(l)
            r.html.render(sleep=10)
            stat_link = r.html.find('{}'.format(css_selector))

            for stat in stat_link:
                match_history_list.extend([h for h in stat.absolute_links])

    return tuple(match_history_list)
