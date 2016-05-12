from html.parser import HTMLParser
from urllib.request import urlopen
from urllib import parse

class LinkParser(HTMLParser):

    def handletags(self, tag, attrs):
        if tag == 'a':
            for(key, value) in attrs:
                if key=='href':
                    newurl = parse.urljoin(self.baseUrl, value)
                    self.links = self.links + [newurl]

    def getLinks(self, url):
        self.links = []
        self.baseUrl = url
        response = urlopen(url)
        if response.getheader('Content-Type')=='text/html':
            html = response.read()
            htmlstring = html.decode("utf-8")
            self.feed(htmlstring)
            return htmlstring, self.links
        else:
            return "",[]

def crawler(url, word):
    pages= [url]
    visited= 0
    found= False
    while pages != [] and not found:
        visited=visited+1
        url=pages[0]
        pages = pages[1:]
        try:
            print(visited, "visiting", url)
            parser = LinkParser()
            data, links = parser.getLinks(url)
            if data.find(word)>-1:
                found = True
            pages = pages + links
            print("success")

        except:
            print("fail")

    if found:
            print(word, "found at", url)

    else:
            print("oops!! not found..")


print("enter url")
url=input()
print("enter the word you want to search")
word=input()

crawler(url, word)
