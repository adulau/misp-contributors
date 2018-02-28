import github3
import json
import redis

from config import username, password
gh = github3.login(username, password=password)

contributors = {}

redcon = redis.StrictRedis(host='localhost', port=6379, db=10)
redcon.flushdb()

for r in gh.iter_repos():
    if str(r.owner).find('MISP',) == -1:
        continue
    redcon.sadd('repositories', r.name)
    for cstat in r.iter_contributor_statistics():
        redcon.zincrby('r:{}'.format(r.name), cstat.author, cstat.total)
        print (r.name," ", cstat.total , " ",  cstat.author)
        redcon.zincrby('topcommit', cstat.author, cstat.total)
    for c in r.iter_contributors():
        contributor = str(c)
        user = gh.user(contributor)
        redcon.set('a:{}'.format(user),user.avatar_url)
        redcon.sadd('users', user)
        redcon.zincrby('topversatile', contributor, 1)

