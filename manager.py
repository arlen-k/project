'''
Description: 
Version: 2.0
Autor: 作者博客：www.arlen.top
Date: 2021-07-20 10:28:03
LastEditors: Seven
LastEditTime: 2021-11-16 14:46:10
'''
# -*- coding: utf-8 -*-
from application import app,manager
from flask_script import Server,Command
from www import *
from jobs.launcher import runJob

##web server
manager.add_command( "runserver",Server( host = "0.0.0.0",use_debugger=True,use_reloader= True,port=80 ) )

# from jobs.movie import MovieJob
# manager.add_command( "runjob", MovieJob )
manager.add_command( "runjob",runJob )

##create_table
@Command
def create_all():
    from application import db
    from common.models.user import User
    db.create_all()

manager.add_command( "create_all",create_all )

def main():
    manager.run()

if __name__ == "__main__":
    #app.run( host = "0.0.0.0",debug=True )
    try:
        import sys
        sys.exit( main() )
    except Exception as e:
        import traceback
        traceback.print_exc()