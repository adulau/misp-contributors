#!/usr/bin/env python
import github3
import redis
import argparse

from config import username, token
gh = github3.login(username, token=token)

print("Authenticated with {}".format(gh))
contributors = {}

redcon = redis.StrictRedis(host='localhost', port=6379, db=11, encoding=u'utf-8')
redcon.flushdb()

skip_repos = ['cakephp', 'cti-python-stix2', 'nginx-proxy']

parser = argparse.ArgumentParser(description="Generate MISP contributors list from GitHub statistics")
parser.add_argument( "--all", action="store_true", default=True, help="Run stats triggering and collection in one shot (default).")
parser.add_argument( "--trigger", action="store_true", default=False, help="Trigger stats only.")
parser.add_argument( "--collect", action="store_true", default=False, help=" stats only.")
args = parser.parse_args()

def trigger():
    for r in gh.repositories():
        if str(r.owner).find('MISP') >= 0:
            print(r.owner)
            if r.name.lower() in skip_repos:
                print(f'Skip repo {r.name}')
                continue
            try:
                for x in r.contributor_statistics():
                    print('trigger stats for {}'.format(r))
            except:
                continue
            else:
                continue

def collect():
    for r in gh.repositories():
        if str(r.owner).find('MISP',) == -1:
            continue
        if r.name.lower() in skip_repos:
            print(f'Skip repo {r.name}')
            continue
        redcon.sadd('repositories', r.name)
        for cstatfull in r.contributor_statistics():
            print(cstatfull.author)
            print(str(cstatfull.author.login))
            redcon.zincrby('r:{}'.format(r.name), cstatfull.total, cstatfull.author.login)
            print(r.name, " ", cstatfull.total, " ",  cstatfull.author.login)
            redcon.zincrby('topcommit', cstatfull.total, cstatfull.author.login)
        for c in r.contributors():
            contributor = str(c)
            user = gh.user(contributor)
            redcon.set('a:{}'.format(user), user.avatar_url)
            redcon.sadd('users', user.login)
            redcon.zincrby('topversatile', 1, contributor)

if args.all and args.trigger is False and args.collect is False:
    redcon.flushdb()
    trigger()
    collect()
elif args.trigger is True:
    trigger()
elif args.collect is True:
    redcon.flushdb()
    collect()
