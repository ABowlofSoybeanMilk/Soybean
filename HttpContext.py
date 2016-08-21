 # -*- coding: UTF-8 -*-
from datetime import datetime


class Request(object):
    
    def __init__(self,data):
        self.Cookie = {}
        self.path = '/'
        self.query = {}
        self.method = 'GET'
        self.__initHeader__(data)
        self.__initCookie__()
        self.__initQuery__()        

    def __initHeader__(self,data):        
        header = data.decode('utf-8').split('\r\n')
        self.body = header.pop()
        path = header[0].split(' ')
        self.method = path[0].strip()
        self.path = path[1].strip()
        self.scheme = path[2].strip()
        for item in range(1,len(header)):            
            kv = header[item].split(':')
            if len(kv) < 2:
                continue
            setattr(self.__class__,kv[0].strip(),kv[1].strip())
    
    def __initCookie__(self):
        cookie = {}
        if not self.Cookie:
            self.Cookie = cookie
            return
        cookieList = self.Cookie.split(';')
        for item in cookieList:
            kv = item.split('=')
            cookie[kv[0].strip()] = kv[1].strip()
        self.Cookie = cookie
        
    def __initQuery__(self):
        path = self.path.split('?')
        self.path = path[0]
        if len(path) == 1:
            return
        query = {}
        searchUrl = path[1].split('&')
        for item in range(0,len(searchUrl)):
            k,v = searchUrl[item].split('=')
            query[k] = v
        self.query = query

class Response():
    def __init__(self,Request,clientSocket):    
        self.socket = clientSocket    
        self.scheme = Request.scheme
        self.Connection = 'keep-alive'
        self.Date = str(datetime.now())
        self.Server = 'wwp'    
        self.__setattr__('Cache-Control',"max-age=0")
        self.__setattr__('Content-Encoding',"gzip")
        self.__setattr__('Keep-Alive',"timeout=15")
        self.__setattr__('Last-Modified',"")
        self.__setattr__('Content-Type',hasattr(Request,'Content-Type') and getattr(Request,'Content-Type') or 'text/html; charset=utf-8')      

        self.cookie = [] 

    def setCookie(self,key,value,expires='session',path='/',Domain=''):
        self.cookie.append('%s=%s; expires=%s; Path=%s; Domain=%s' % (key,value,expires,path,Domain))
        
    def write(self,data,code=200,status='OK'):
        decod = data.encode('utf-8')
        result = self.scheme + ' ' + str(code) + ' ' + status
        result = result + '\r\n' 
        # result = result + 'Content-Encoding: ' + self.__getattribute__('Content-Encoding')
        # result = result + '\r\n'       
        result = result + 'Content-Type: ' + self.__getattribute__('Content-Type')
        result = result + '\r\n'
        result = result + 'Content-Length: ' + str(len(decod))
        result = result + '\r\n'   
        for item in self.cookie:
            result = result + 'Set-Cookie: ' + item
            result = result + '\r\n'
        result = result + '\r\n'   
        
        self.socket.send(result.encode('utf-8')+decod)
        
        