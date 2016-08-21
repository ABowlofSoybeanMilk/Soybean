import re



class compiler():
    def __init__(self,tmplString):
        self.tmplString = tmplString
        self.code = ''
    def render(self,dataObj):
        code = self._compile_()

    def _compile_(self):
        headNode = SyntaxBlockNode()
        self._generateSyntaxTree_(headNode)
        if headNode.childrenNode :
            self._generatePythonCode_(headNode.childrenNode,4)
        self._decorate_()
        read = open('compiled.py','w')
        read.write(self.code)
        read.close()
    
    def _decorate_(self):
        self.code = 'def render(pysoy):\n' + ' '*4 + 'bufferString=""\n'  + self.code
        self.code += ' '*4 + 'return bufferString\n'    
    def _generatePythonCode_(self,childrenNode,deep):
        for child in childrenNode:            
            if type(child) is SyntaxTextNode:
                text = child.content.replace('\n','').strip()
                if text:
                    self.code = self.code + ' '*deep + 'bufferString+=\'\'\'' + text  + '\'\'\'' + '\n'
            if type(child) is SyntaxValueNode:
                self.code = self.code + ' '*deep + 'bufferString+=' + child.content  + '\n'
            if type(child) is SyntaxExpressNode:
                self.code = self.code + ' '*deep +  child.content +  '\n'
            if type(child) is SyntaxBlockNode:
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

if __name__ == "__main__":
    read = open('test.html')
    com = compiler(read.read())
    com.render({})