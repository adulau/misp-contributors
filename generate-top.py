import redis
redcon = redis.StrictRedis(host='localhost', port=6379, db=10, charset="utf-8", decode_responses=True)

output = '---\n'
output += 'layout: page\n'
output += 'title: MISP contributors per repository\n'
output += 'permalink: /contributors/\n'
output += 'toc: true\n'
output += '---\n\n'


url_github = 'https://www.github.com/MISP/'
url_user = 'https://www.github.com/'
repo_to_skip = ['cti-python-stix2', 'SwiftCodes']

output += "# Contributors \n\n"

for user in redcon.zrevrange('topversatile', 0, -1):
    gravatar = redcon.get("a:{}".format(user))
    output += "[![{}]({}){{:height=\"36px\" width=\"36px\"}}]({}{})".format(user, gravatar, url_user,
                                                     user)
output += "\n"

for repository in sorted(redcon.smembers('repositories')):
    if repository in repo_to_skip:
        continue
    output += "# {} \n\n".format(repository)
    output += "The repository [{}]({}{}) is part of the MISP project and has the following top contributors \n\n".format(repository, url_github, repository)
    output += "| username | total commits |\n"
    output += "|:--------:|:-------------:|\n"
    for top in redcon.zrevrange('r:{}'.format(repository), 0, -1, withscores=True):
        output += "|[{}]({}{})|{}|\n".format(top[0],url_user,top[0],top[1])
    output += "\n"

print (output)
