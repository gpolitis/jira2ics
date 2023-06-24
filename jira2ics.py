#!/usr/bin/env python3

from atlassian import Jira
from icalendar import Calendar, Todo
import dateutil.parser 
import sys
import argparse
import utils

#import logging
#logging.basicConfig()
#logging.getLogger().setLevel(logging.DEBUG)

def make_todo(issue):
    todo = Todo()
    todo.add('uid', 'id-{}'.format(issue['id']))
    todo.add('url', issue['self'])
    fields = issue['fields']
    todo.add('summary', '[{}] {}'.format(issue['key'], fields['summary']))
    todo.add('description', fields['description'])
    todo.add('created', dateutil.parser.isoparse(fields['created']))
    todo.add('last-modified', dateutil.parser.isoparse(fields['updated']))
    todo.add('status', 'NEEDS-ACTION')
    todo.add('categories', ['Work'])
    return todo
        
def make_calendar(json):
    cal = Calendar()
    for issue in json['issues']:
        cal.add_component(make_todo(issue))
    return cal

def jira2ics(args):
    cookies = utils.parse_chrome_cookie_file(args.chrome_cookies)
    jira = Jira(url=args.url, cookies=cookies)
    cal = make_calendar(jira.jql(args.jql))
    args.outfile.write(cal.to_ical().decode("utf-8"))

parser = argparse.ArgumentParser(description='Convert Jira issues to iCal format.')
parser.add_argument('--chrome-cookies', type=argparse.FileType('r'))
parser.add_argument('--outfile', nargs='?', type=argparse.FileType('w'), default=sys.stdout)
parser.add_argument('--jql', nargs='?', default="resolution = Unresolved AND assignee in (currentUser())")
parser.add_argument('url')

jira2ics(parser.parse_args())
