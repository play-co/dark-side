import gevent
import requests
import json
import argparse
import sys
from gevent.pywsgi import WSGIHandler, WSGIServer

class Handler(object):

    def __init__(self,hosts):
        self._hosts = hosts

    @property
    def downstream_servers(self):
        return self._hosts

    def __call__(self,environ,start_response):

        path = environ['PATH_INFO'] 
        query_string = environ['QUERY_STRING']
        method = environ['REQUEST_METHOD']

        all_bodies = []
        for server in self.downstream_servers:
            req = self.make_request(environ, server)
            req.send()
            this_body = req.response.content
            try:
                this_response = json.loads(this_body)
            except ValueError, e: 
                this_response = this_body 

            for other_body in all_bodies:
                if not this_response == other_body:
                    print '\noh snap, mismatch in two bodies!\n: %s?%s\n'% (path, query_string)
            all_bodies.append(this_response)

        start_response('200 OK',[])
        if all_bodies:
            return all_bodies[-1]
        else:
            return 'fudgesickles'

    def make_request(self, environ, for_server):
        return requests.Request(url=for_server+environ['PATH_INFO'],
                                method=environ['REQUEST_METHOD'],
                                params=environ['QUERY_STRING'])


def main():
    parser = argparse.ArgumentParser(description='compare multiple server\'s responses')
    parser.add_argument('--hosts',action='append',dest='hosts')
    args = parser.parse_args()

    print 'now comparing hosts', args.hosts

    WSGIServer(('127.0.0.1',8888),Handler(args.hosts)).serve_forever()

if __name__ == "__main__" : main()