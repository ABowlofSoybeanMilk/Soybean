import  Controller.BaseController as BaseController
import sys
sys.path.append('./View')
import SoybeanTemplateEngine as engine

class HomeController(BaseController.Controller):
    def __init__(self,request,response):
        super().__init__(request,response)

    def index(self,name):        
        tmpl = engine.render('./View/home',ss)
        self.response.write(tmpl)
    
class Student():
    def __init__(self,name,sex):
        self.name = name
        self.sex = sex
class Class():
    def __init__(self):
        self.Students = []
ss = Class()
ss.Students.append(Student("Razor1",1))
ss.Students.append(Student("Razor2",3))
ss.Students.append(Student("Razor3",1))
