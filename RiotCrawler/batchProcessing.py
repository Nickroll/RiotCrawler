from multiprocessing import Pool
from typing import Union, List

from requests_html import HTMLSession

from RiotCrawler.Exceptions.errors import BatchError


def _create_batch(links: Union[list, tuple] = None, batch_size: int = None) -> List[Union[list, tuple]]:
    """
    Creates batches of links and returns a list of them

    :param links: A tuple or list of links that can be iterated over
    :param batch_size: How big of batches to create
    :return: A list of tuple/lists of size batch_size
    """

    return [links[i:i + batch_size] for i in range(0, len(links), batch_size)]


def _link_processor(batch_links: List[Union[list, tuple]]) -> list:
    """
    Processes links in a batch manner, similar to get_match_history_links

    :param batch_links: A list that contains either lists or tuples
    :return: A list of links to the match history stats pages
    """

    results = []
    session = HTMLSession()

    for l in batch_links:
        r = session.get(l)
        r.html.render(sleep=10)
        tmp_next = r.html.xpath('//a[contains(@href, "/matches/")]')
        next_link = list()

        for tl in tmp_next:
            next_link.extend(([h for h in tl.absolute_links]))

        for nl in next_link:
            r = session.get(nl)
            r.html.render(sleep=10)
            stat_link = r.html.find('{}'.format('.stats-link'))

            for stat in stat_link:
                results.extend([h for h in stat.absolute_links])

    return results


def _multi_process(batch: List[Union[list, tuple]] = None, num_process: int = None) -> list:
    """
    Creates the multiprocess for running batch links

    :param batch: The batch of links to process
    :param num_process: The number of process to run
    :return: A list of links to the stats match history pages
    """

    pool = Pool(processes=num_process)
    output = pool.map(_link_processor, batch)
    pool.close()
    pool.join()

    return output


def batch_process_links(links: Union[list, tuple] = None, batch_size: int = None, num_process: int = None) -> list:
    """
    Processes the links passed using multiprocessing in a batch manner. Best performance when tested was with batch_size
    of 2 with 10 processes. This was not fully tested. Smaller batches and larger process should increase performance

    :param links: A list or tuple of links to the schedule page of lolesports
    :param batch_size: The size to cut up the lists into
    :param num_process: The number of processes to be passed to _multi_process
    :return: A list of links to the stats match history pages
    """
    if not all([batch_size, num_process]):
        raise BatchError('One of batch_size or num_process was None')

    print('Creating Batches')
    batch = _create_batch(links, batch_size)
    print('Starting Multiprocess run')
    stats_links = _multi_process(batch, num_process)

    return stats_links
