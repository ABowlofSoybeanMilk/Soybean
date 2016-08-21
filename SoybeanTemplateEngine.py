import re

class compiler():
    def __init__(self,tmplString):
        self.tmplString = tmplString
        self.code = ''
    def compile(self):
        self._compile_()
        return self.code

    def _compile_(self):
        headNode = SyntaxBlockNode()
        self._generateSyntaxTree_(headNode)
        if headNode.childrenNode :
            self._generatePythonCode_(headNode.childrenNode,4)
        self._decorate_()        
    
    def _decorate_(self):
        self.code = 'def render(pysoy):\n' + ' '*4 + 'bufferString=""\n'  + self.code
        self.code += ' '*4 + 'return bufferString\n'    
    def _generatePythonCode_(self,childrenNode,deep):
        for child in childrenNode:            
            if isinstance(child,SyntaxTextNode):
                text = child.content.replace('\n','').strip()
                if text:
                    self.code = self.code + ' '*deep + 'bufferString+="' + text  + '"' + '\n'
            if isinstance(child,SyntaxValueNode):
                self.code = self.code + ' '*deep + 'bufferString+=' + child.content  + '\n'
            if isinstance(child,SyntaxExpressNode):
                self.code = self.code + ' '*deep +  child.content +  '\n'
            if isinstance(child,SyntaxBlockNode):
                self.code = self.code + ' '*deep +  child.keyExpress + ':' + '\n'
                self._generatePythonCode_(child.childrenNode,deep+4)

    def _generateSyntaxTree_(self,node):        
        while self.tmplString:
            index = self._findkeychar_(self.tmplString)
            end = self.tmplString.find('}')
            if  end < index :
                if end == -1:
                    text,self.tmplString = self.tmplString,None
                else:
                    text,self.tmplString = self.tmplString[:end] ,self.tmplString[end+1:]
                node.childrenNode.append(SyntaxTextNode(text))
                return
            text,self.tmplString = self.tmplString[:index] ,self.tmplString[index:]
            node.childrenNode.append(SyntaxTextNode(text))
            keytype,value = self._handlekeyType_(self.tmplString)
            if keytype == "string":
                text,self.tmplString = self.tmplString[1:value+1] ,self.tmplString[value+2:]
                node.childrenNode.append(SyntaxTextNode(text))      
            
            elif keytype == "value":
                text,self.tmplString = self.tmplString[2:value] ,self.tmplString[value+1:]
                node.childrenNode.append(SyntaxValueNode(text))      
            
            elif keytype == "express":
                text,self.tmplString = self.tmplString[2:value] ,self.tmplString[value+1:]
                node.childrenNode.append(SyntaxExpressNode(text))

            elif keytype == "block":
                text,self.tmplString = self.tmplString[1:value] ,self.tmplString[value+1:]
                child = SyntaxBlockNode(text)
                node.childrenNode.append(child)
                self._generateSyntaxTree_(child)
                
              
    def _handlekeyType_(self,string):
        if string.startswith('${'):
            return ("value",string.find('}'))
        
        if string.startswith('@{'):
            return ("express",string.find('}'))
        
        if string.startswith('`'):
            return ('string',string[1:].find('`'))
        
        if string.startswith('@'):
            return ('block',string.find('{'))

        return (None,None)
    
    def _findkeychar_(self,string):
        for index in range(0,len(string)):
            if string[index] in '@$`':
                return index
        return len(string)
class SyntaxTextNode():
    def __init__(self,content=''):
        self.content = content

class SyntaxExpressNode():
    def __init__(self,content=''):
        self.content = content

class SyntaxValueNode():
    def __init__(self,content=''):
        self.content = content

class SyntaxBlockNode():
    def __init__(self,keyExpress=''):
        self.keyExpress = keyExpress
        self.childrenNode = []

def render(dirStr,obj):
    path = dirStr.replace('./','').replace('/','.')
    ls = path.split('.')
    name = ls[len(ls)-1]
    read = open(dirStr+'.html')
    com = compiler(read.read())
    code = com.compile()
    write = open(dirStr+'.py','w')
    write.write(code)
    write.close()
    compiled = __import__(path)
    return getattr(compiled,name).render(obj)
