<!-- These are examples of badges you might want to add to your README:
     please update the URLs accordingly

[![Built Status](https://api.cirrus-ci.com/github/<USER>/predthread.svg?branch=main)](https://cirrus-ci.com/github/<USER>/predthread)
[![ReadTheDocs](https://readthedocs.org/projects/predthread/badge/?version=latest)](https://predthread.readthedocs.io/en/stable/)
[![Coveralls](https://img.shields.io/coveralls/github/<USER>/predthread/main.svg)](https://coveralls.io/r/<USER>/predthread)
[![PyPI-Server](https://img.shields.io/pypi/v/predthread.svg)](https://pypi.org/project/predthread/)
[![Conda-Forge](https://img.shields.io/conda/vn/conda-forge/predthread.svg)](https://anaconda.org/conda-forge/predthread)
[![Monthly Downloads](https://pepy.tech/badge/predthread/month)](https://pepy.tech/project/predthread)
[![Twitter](https://img.shields.io/twitter/url/http/shields.io.svg?style=social&label=Twitter)](https://twitter.com/predthread)
-->

[![Project generated with PyScaffold](https://img.shields.io/badge/-PyScaffold-005CA0?logo=pyscaffold)](https://pyscaffold.org/)

# predthread

> Tool for easily running a score prediction game on your team's subreddit!

The prediction game that predthread implements is a fun and simple game to add to any football team's subreddit. Users post predictions in the thread each week. They are awarded 3 points for an exactly correct prediction, 1 point for matching the result (W/L/D) but not the exact score, and 0 points for an incorrect result. These tools make it easy to scrape and parse prediction comments from the reddit thread, and generate a standings table that tracks each users points tally throughout the season.

### Predthread relies on a few simple ideas and methods

- The game moderator posts a weekly prediction game thread, typically a day or two before the match. Users post predictions as comments.

- After the match, [PRAW](https://praw.readthedocs.io/en/stable/) is used to scrape comments.

- Scraped comments are parsed into prediction data by a very simple regex pattern and dumped into a pandas DataFrame.

- The prediction DataFrame is combined with the standings table (points tally from all previous matches) into an updated standings table, also a DataFrame.

- The updated standings table is printed to a markdown string in the Reddit table format. The standings are posted in the prediction game thread for the next week. They both inform the users of their standings, and serve as permanent storage for the standings data.

### More details:

- There is a feature to ignore comments made after a certain time cutoff. Typically the cutoff is set by the game moderator to one hour before kickoff, before team lineups are posted.

- A service such as [Later for Reddit](laterforreddit.com) can be used to schedule posts.

### Simplified examples

- See the examples/ folder.

- See the test subreddit [predthreadtest](https://www.reddit.com/r/predthreadtest/)

<!-- pyscaffold-notes -->

## Note

This project has been set up using PyScaffold 4.3.1. For details and usage
information on PyScaffold see https://pyscaffold.org/.
