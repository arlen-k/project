# -*- coding: utf-8 -*-
from application import app
from www import *
from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop

def main():
    http_server = HTTPServer( WSGIContainer(app) )
    http_server.listen( 5000 )
    IOLoop.instance().start()

if __name__ == "__main__":
    try:
        import sys
        sys.exit( main() )
    except Exception as e:
        import traceback
        traceback.print_exc()