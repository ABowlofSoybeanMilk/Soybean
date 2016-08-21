 # -*- coding: UTF-8 -*-
 
import gevent
from gevent import socket
from gevent import event
import HttpContext
import Route

rev=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
rev.bind(('',112)) 
rev.listen(5)

def handler(rev,data,client):
    request = HttpContext.Request(data)    
    response = HttpContext.Response(request,client)
    result = getResult(request,response)
    print(result)

def handlers(client):
    while True:
        data=client.recv(1024)
        return data;

def main():
    while True:
        print('wait collection')
        client,add = rev.accept()
        data = handlers(client)
        gevent.spawn(handler,rev,data,client)
        
def getResult(request,response):
     for item in Route.routeConfig:
        add,cls,action = item
        if(add == request.path):            
            contro = cls(request,response)
            mtd = getattr(contro,action)
            return mtd(request.query)

if __name__ == '__main__':
    main()