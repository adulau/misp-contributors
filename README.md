# MISP contributors

Extracting statistics from GitHub about MISP organisation repositories and populating
a Redis database with the various contributors per repositories in MISP organisation.
A simple script generates the top lists from the Redis in Markdown format.

Sample output: [https://www.misp-project.org/contributors/](https://www.misp-project.org/contributors/)

## Requirements

- Python 3
- Redis
- github3

