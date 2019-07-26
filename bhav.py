import os, os.path
import random
import string
import redis
import cherrypy

r = redis.Redis()

class equity_app(object):

    @cherrypy.expose
    def search(self,name=None):
        html_output_string =''

        if name:
            for x in r.lrange('keys',0,r.llen('keys')):
                code_key=x
                # print(type(name),str(r.hget(code_key,'name'),'utf-8').strip())
                if str(r.hget(code_key,'name'),'utf-8').strip()==str(name):
                    html_output_string +='<tr><td>'+str(code_key,'utf-8')+'</td><td>'+ str(r.hget(code_key,'name'),'utf-8')+'</td> <td>'+str(r.hget(code_key,'open'),'utf-8')+'</td><td>'+str(r.hget(code_key,'high'),'utf-8')+'</td><td>'+str(r.hget(code_key,'low'),'utf-8')+'</td><td>'+str(r.hget(code_key,'close'),'utf-8')+'</td></tr>'
                    break
        index = open("search.html").read().format(tab=html_output_string)
        return index



    @cherrypy.expose
    def index(self):
        # style="""
        #             table {
        #               border-collapse: collapse;
        #               width: 70%;
        #             }
        #              th,td {
        #               padding: 8px;
        #               text-align: left;
        #               border-bottom: 1px solid #ddd;
        #             }
        #     """
        html_output_string =''
        for x in range(10):
            code_key=r.lindex('keys',x)
            html_output_string+='<tr><td>'+str(code_key,'utf-8')+'</td><td>'+ str(r.hget(code_key,'name'),'utf-8')+'</td> <td>'+str(r.hget(code_key,'open'),'utf-8')+'</td><td>'+str(r.hget(code_key,'high'),'utf-8')+'</td><td>'+str(r.hget(code_key,'low'),'utf-8')+'</td><td>'+str(r.hget(code_key,'close'),'utf-8')+'</td></tr>'
        index = open("index.html").read().format(tab=html_output_string)
        return index




if __name__ == '__main__':
    conf = {
        '/': {
            'tools.sessions.on': True,
            'tools.staticdir.root': os.path.abspath(os.getcwd())
        },
        '/static': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': './public'
        }
    }
    cherrypy.quickstart(equity_app(), '/', conf)
