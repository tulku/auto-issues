import os
from flask import Flask, request
import requests
import json
import sys

app = Flask(__name__)


class GitHub(object):
    def __init__(self, api_token, users, special_title, special_user):
        self.session = requests.Session()
        self.session.headers['Authorization'] = 'token %s' % api_token
        self.reviewers = users
        self.title = special_title
        self.user = special_user

    def set_assigned(self, issue):
        url = issue['url']
        title = issue['title']
        if (self.title is not None) and (self.user is not None) and (self.title in title):
            assignee = special_user
        else:
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

try:
    special_title = os.environ['SPECIAL_TITLE']
    special_user = os.environ['SPECIAL_USER']
except KeyError:
    special_title = None
    special_user = None

gh = GitHub(token, users)

if __name__ == '__main__':
    app.run()
