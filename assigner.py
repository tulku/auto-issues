import os
from flask import Flask, request
import requests
import json
import sys

app = Flask(__name__)


class GitHub(object):
    def __init__(self, api_token, users):
        self.session = requests.Session()
        self.session.headers['Authorization'] = 'token %s' % api_token
        self.reviewers = users

    def set_assigned(self, issue):
        url = issue['url']
        assignee = issue['number'] % len(self.reviewers)
        body = '{{\n "assignee": "{}"\n}}'.format(self.reviewers[assignee])
        return self.session.patch(url, data=body)


@app.route('/', methods=['POST'])
def foo():
    data = json.loads(request.data)
    if 'issue' in data and 'action' in data:
        action = data["action"]
        print "Issue action: {}".format(action)
        if action == "opened":
            print gh.set_assigned(data['issue']).text
    return "OK"

try:
    token = os.environ['GITHUB_TOKEN']
    users = os.environ['GITHUB_USERS'].split(',')
    users = [u.strip() for u in users]
except KeyError:
    print 'You need to set the GITHUB_TOKEN and GITHUB_USERS env variables'
    print 'Exiting...'
    sys.exit(1)


gh = GitHub(token, users)

if __name__ == '__main__':
    app.run()
