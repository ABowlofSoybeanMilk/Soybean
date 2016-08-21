import compiled
import json
class Student():
    def __init__(self,name,sex):
        self.name = name
        self.sex = sex
class Class():
    def __init__(self):
        self.Students = []
ss = Class()
ss.Students.append(Student("王为蓬1",1))
ss.Students.append(Student("王为蓬2",3))
ss.Students.append(Student("王为蓬3",1))

html = compiled.render(ss)
print(html)

