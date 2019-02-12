import github3
import json
import redis
import time

from config import username, password
gh = github3.login(username, password=password)

print (gh)
contributors = {}

redcon = redis.StrictRedis(host='localhost', port=6379, db=10, encoding=u'utf-8')
redcon.flushdb()

for r in gh.repositories():
    if str(r.owner).find('MISP') >= 0:
        print (r.owner)
        try:
            for x in r.contributor_statistics():
                print ('trigger stats for {}'.format(r))
        except:
            continue
        else:
            continue


for r in gh.repositories():
    if str(r.owner).find('MISP',) == -1:
        continue
    redcon.sadd('repositories', r.name)
    for cstatfull in r.contributor_statistics():
        print (cstatfull.author)
        print (str(cstatfull.author.login))
        redcon.zincrby('r:{}'.format(r.name), cstatfull.total, cstatfull.author.login)
        print (r.name," ", cstatfull.total , " ",  cstatfull.author.login)
        redcon.zincrby('topcommit', cstatfull.total, cstatfull.author.login)
    for c in r.contributors():
        contributor = str(c)
        user = gh.user(contributor)
        redcon.set('a:{}'.format(user),user.avatar_url)
        redcon.sadd('users', user.login)
        redcon.zincrby('topversatile', 1, contributor)

