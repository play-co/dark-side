#!/usr/bin/python

import gevent
import requests
import json
import argparse
import sys
import logging
import json_tools
from webob import Request
from gevent.pywsgi import WSGIHandler, WSGIServer

class Handler(object):

    def __init__(self,master,apprentices):
        self._master = master
        self._apprentices = apprentices

        self._mismatch_log = logging.getLogger("darkside-mismatch")
        self._mismatch_log.setLevel(logging.INFO)
        file_handler = logging.FileHandler('darkside-mismatch.log')
        file_handler.setFormatter(logging.Formatter('%(asctime)s\n----\n%(message)s'))
        self._mismatch_log.addHandler(file_handler)

    def __call__(self,environ,start_response):


        incoming = Request(environ)

        all_bodies = []
        all_servers =  [ self._master]  + self._apprentices
        master_response = None
        master_body = None

        for server in all_servers:
            req = self.make_request(incoming, server)
            req.send()
            this_body = req.response.content
            try:
                this_response = json.loads(this_body)
            except ValueError, e: 
                this_response = this_body 

            if server == self._master:
                master_response = req.response
                master_body = this_response

            if not this_response == master_body:
                self._mismatch_log.info('apprentice %s failed fetching %s?%s:\n----\n%s\n---vs---\n%s' %
                 (server, incoming.path,incoming.query_string, this_response, master_body))
                if isinstance(this_response, dict) and isinstance(master_body, dict):
                    diff =  json_tools.diff(this_response,master_body)
            all_bodies.append(this_response)

        if master_response:
            status = '%s %s' % (master_response.status_code, master_response.reason)
            start_response(status,master_response.headers.items())
            return master_response.content
        else:
            start_response('200 OK',[])
            return 'fudgesickles'

    def make_request(self, incoming_request, for_server):
        return requests.Request(url=for_server+incoming_request.path,
                                method=incoming_request.method,
                                params=dict(incoming_request.GET.items()))

def main():
    #set up the arguments parser
    parser = argparse.ArgumentParser(description='run a proxy server that compares response from the master to responses returned by any number of apprentices')
    parser.add_argument('master',help="return this server's response")
    parser.add_argument('--apprentice',action='append',dest='apprentices',
        help="compare this host's response to the master's. use this argument multiple times for multiple apprentices.")
    parser.add_argument('--port',help='listen on this port',type=int,default=8987)
    #now parse that shit
    args = parser.parse_args()
    
    #set up the logger
    logging.basicConfig()

    print 'dark side: listening on port %s for your deepest fears and worries' % args.port
    print 'master:'
    print '\t',args.master 
    print 'apprentices:'
    print '\t'+(' '.join(args.apprentices))
    WSGIServer(('127.0.0.1',args.port),Handler(args.master, args.apprentices)).serve_forever()

if __name__ == "__main__" : main()
