def render(pysoy):
    bufferString=""
    bufferString+="<html>  <body>"
    for item in pysoy.Students:
        bufferString+="<P>my name is"
        bufferString+=item.name
        bufferString+="</p>"
        if item.sex == 1:
            bufferString+="<p>"
            bufferString+=item.name
            bufferString+="is a boy</p>"
        else:
            bufferString+="${item.name}"
            bufferString+="<p>"
            bufferString+=item.name
            bufferString+="is a girl</p>"
    bufferString+="</body></html>"
    return bufferString
