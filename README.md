**Riot Crawler**
======================
This package is designed to retrieve match history information from LCS, LCK, LMS, and NA-Academy games. 

The information that is returned is a .json file with all of the match history information provided by Riot's tournament API.

**Usage**
--------------
The RiotCrawl class contains a number of methods to retrieve the information requested.

The bellow script will create all the necessary links, search them, and return the JSON's objects saved to the 'Json Downloads' folder.

```python
from RiotCrawler import RiotCrawl
rc = RiotCrawl('config.ini')
rc.make_links()
rc.match_history_links()
rc.get_json(path='Json Downloads')
```

An option is given to return the links that are created or retrieved from Riots website in case batch running of links is wanted.

```python
from RiotCrawler import RiotCrawl
rc = RiotCrawl('config.ini')
schedule_links = rc.make_links(inplace=False)
match_links = rc.match_history_links(schedule_links, inplace=False)
```

The JSON data retrieved can also be returned if a path is not provided to the method .get_json().

Lastly an optional run_all is provided that will run exactly like hte first code block above, but without the separate 
method calls. This takes a while but saves a small amount of typing. 

**Config.ini**
-----------------
The config.ini file is necessary as RiotCrawl will attempt to parse it for necessary information. Everything under the 
DEFAULT_INIT section must be provided otherwise errors will be raised.
