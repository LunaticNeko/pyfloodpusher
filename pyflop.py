import json
from pprint import pprint
import argparse
import urllib2
import urllib

parser = argparse.ArgumentParser(description=
    'Work with Floodlight staticflowentrypusher')

parser.add_argument('-c', '--clear', dest='op_clear', action='store_true', help='Clear the flow rules from all switches first. IRREVERSIBLE!')
parser.add_argument('-l', '--list', dest='op_list', action='store_true', help='List all flow rules to your console. If used in conjunction with other options, this will be done last. Can get messy -- please have a JSON reader tool handy.')
parser.add_argument('-s', '--server', dest='server', action='store', default='localhost', help='Specify a Floodlight server here')
parser.add_argument('-p', '--port', dest='port', action='store', default='8080', help='Specify a Floodlight port')
parser.add_argument('rulesfile', nargs='?', help='Load up to one rule file in JSON to be processed. Only JSON is supported.')

args = parser.parse_args()
print args

#make base URL
baseurl = 'http://'+args.server+':'+args.port

#connect to server and get list of switches
#switches = json.loads(urllib2.urlopen(baseurl+
#                      '/wm/core/controller/switches/json').read())

if args.op_clear:
    urllib2.urlopen(baseurl+'/wm/staticflowentrypusher/clear/all/json').read()
    #print json.loads(urllib2.urlopen(baseurl+'/wm/staticflowentrypusher/clear/all/json').read())

if args.rulesfile:
    rules=json.load(open(args.rulesfile))
    for rule in rules:
        postdata = json.dumps(rule)
        open_request = urllib2.urlopen(
                urllib2.Request(baseurl+'/wm/staticflowentrypusher/json',
                                postdata,
                                {'Content-Type': 'application/json'}))
        print open_request.read()

if args.op_list:
    print json.loads(urllib2.urlopen(baseurl+
        '/wm/staticflowentrypusher/list/all/json').read())
