import os, os.path
import random
import string
import redis
import cherrypy
import extract
redis_host = os.getenv('REDISTOGO_URL', 'redis://localhost:6379')
r = redis.StrictRedis.from_url(redis_host, decode_responses=True)

# r = redis.Redis()

class equity_app(object):

    @cherrypy.expose
    def search(self,name=None):
        html_output_string =''
        if name:
            if r.hgetall(name.strip()) :
                html_output_string +='<tr><td>'+str(name)+'</td><td>'+ str(r.hget(name,'code'))+'</td> <td>'+str(r.hget(name,'open'))+'</td><td>'+str(r.hget(name,'high'))+'</td><td>'+str(r.hget(name,'low'))+'</td><td>'+str(r.hget(name,'close'))+'</td></tr>'

            # for x in r.lrange('keys',0,r.llen('keys')):
            #     code_key=x
            #     # print(type(name),str(r.hget(code_key,'name')).strip())
            #     if str(r.hget(code_key,'name')).strip()==str(name):
            #         html_output_string +='<tr><td>'+str(code_key)+'</td><td>'+ str(r.hget(code_key,'name'))+'</td> <td>'+str(r.hget(code_key,'open'))+'</td><td>'+str(r.hget(code_key,'high'))+'</td><td>'+str(r.hget(code_key,'low'))+'</td><td>'+str(r.hget(code_key,'close'))+'</td></tr>'
            #         break
        index = open("search.html").read().format(tab=html_output_string)
        return index

    @cherrypy.expose
    def index(self):
        # extract.load_redis()
        raise cherrypy.HTTPRedirect("index2")

    @cherrypy.expose
    def index2(self):
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
            html_output_string+='<tr><td>'+str(code_key)+'</td><td>'+ str(r.hget(code_key,'code'))+'</td> <td>'+str(r.hget(code_key,'open'))+'</td><td>'+str(r.hget(code_key,'high'))+'</td><td>'+str(r.hget(code_key,'low'))+'</td><td>'+str(r.hget(code_key,'close'))+'</td></tr>'
        index = open("index.html").read().format(tab=html_output_string)
        return index




if __name__ == '__main__':
    cherrypy.config.update({'server.socket_host': '0.0.0.0',})
    cherrypy.config.update({'server.socket_port': int(os.environ.get('PORT', '5000')),})
    cherrypy.quickstart(equity_app())

    # conf = {
    #     '/': {
    #         'tools.sessions.on': True,
    #         'tools.staticdir.root': os.path.abspath(os.getcwd())
    #     }
    # }
    # cherrypy.quickstart(equity_app(), '/', conf)
