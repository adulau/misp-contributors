# MISP contributors

Extracting statistics from GitHub about MISP organisation repositories and populating
a Redis database with the various contributors per repositories in MISP organisation.
A simple script generates the top lists from the Redis in Markdown format.

Sample output: [https://www.misp-project.org/contributors/](https://www.misp-project.org/contributors/)

# Usage

Start your Redis server.

- Edit the config.py.sample, set your username and access token and copy the file as `config.py`
- Run the tool to gather statistics from GitHub: `contributors.py` The tool will feed all the stats into the Redis server
- Run the tool to generate a MarkDown file of all the contributions: `generate-top.py`

## Requirements

- Python 3
- Redis
- github3.py

## License

The software is released under the GNU Affero General Public License v3.0.

Copyright (C) 2018-2020 Alexandre Dulaunoy - https://www.foo.be/
