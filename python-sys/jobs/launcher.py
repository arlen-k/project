# -*- coding: utf-8 -*-
from flask_script import Command
import  sys,argparse,traceback,importlib
'''
Job统一入口文件
python manager.py runjob -m Test ( jobs/tasks/Test.py )
python manager.py runjob -m test/index ( jobs/tasks/test/index.py )
'''
class runJob( Command ):

    capture_all_args = True
    def run(self,*args,**kwargs):
        args = sys.argv[2:]
        parser = argparse.ArgumentParser( add_help= True)
        parser.add_argument("-m","--name",dest="name",metavar="name",help="指定job名",required=True)
        parser.add_argument("-a","--act",dest="act",metavar="act",help="Job动作",required=False)
        parser.add_argument("-p","--param",dest="param",nargs="*",metavar="param",help="业务参数",required=False)
        params = parser.parse_args( args )
        params_dict = params.__dict__
        if "name" not in params_dict or not params_dict['name']:
            return self.tips()

        try:
            '''
            from jobs.tasks.test import JobTask
            '''
            module_name = params_dict['name'].replace("/",".")
            import_string = "jobs.tasks.%s"%( module_name )
            target = importlib.import_module(  import_string )
            exit( target.JobTask().run( params_dict ) )
        except Exception as e:
            traceback.print_exc()
        return

    def tips(self):
        tip_msg = '''
        请正确的调度Job
        python manager.py runjob -m Test ( jobs/tasks/Test.py )
        python manager.py runjob -m test/index ( jobs/tasks/test/index.py )
        '''
        print( tip_msg )
        return
