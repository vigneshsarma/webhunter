from HTMLParser import HTMLParser

# create a subclass and override the handler methods
class MyHTMLParser(HTMLParser):
    def __init__(self):
        self.data =""
        self.url = []
    def handle_starttag(self, tag, attrs):
        print "Encountered a start tag:", tag, attrs
        if tag== 'a':
            for at in attrs:
                if at[0]=="href":
                    url.append(at[1])
    def handle_endtag(self, tag):
        print "Encountered an end tag :", tag
    def handle_data(self, data):
        print "Encountered some data  :",
        self.data += data



if __name__=="__main__":
    # instantiate the parser and fed it some HTML
    parser = MyHTMLParser()
    parser.feed('<html><head><title>Test</title></head>'
            '<body id="bla"><h1>Parse me!</h1></body></html>')
