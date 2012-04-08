from cache import cache
from parser import LinkFinder
from pymongo import Connection
from IndexHunt import IndexHunt
from GraphHunt import GraphHunt

class WebHunter:
    def __init__(self):
        #db = Connection().web_hunter
        self.index, self.graph = IndexHunt(),GraphHunt()
        
        self.crawl_web('http://udacity.com/cs101x/urank/index.html')
        self.ranks = {}
        self.compute_ranks()
        #db.index.insert(self.index)

    def qsort(self,tosort,ranks):
        if tosort == []: 
            return []
        else:
            pivot = tosort[0]
            lesser = self.qsort([x for x in tosort[1:] if ranks[x] < ranks[pivot]],ranks)
            greater = self.qsort([x for x in tosort[1:] if ranks[x] >= ranks[pivot]],ranks)
            return greater + [pivot] + lesser

    def ordered_search(self, keyword):
        keyword=keyword.lower()
        links = self.index.find(keyword)
        if links:
            return self.qsort(links,self.ranks)
        return None

    def get_page(self,url):
        if url in cache:
            return cache[url]
        return ""


    def union(self,a, b):
        for e in b:
            if e not in a:
                a.append(e)

    def add_page_to_index(self, url, content):
        words = content.split()
        for word in words:
            self.add_to_index( word, url)

    def add_to_index(self, keyword, url):
        links = self.index.find(keyword)
        if links:
            if url not in links:
                links.append(url)
                self.index.update(keyword,links)
        else:
            self.index.insert(keyword ,url)

    def lookup(self, keyword):
        links = self.index.find(keyword)
        if links:
            return links
        else:
            return None

    def crawl_web(self,seed): # returns index, graph of inlinks
        tocrawl = [seed]
        crawled = []
        while tocrawl: 
            page = tocrawl.pop()
            if page not in crawled:
                content = self.get_page(page)
                outlinks,content,title = LinkFinder().start_parsing(content)
                self.add_page_to_index( page, content)
                self.graph.insert(page,outlinks,title,content)
                self.union(tocrawl, outlinks)
                crawled.append(page)

    def compute_ranks(self):
        d = 0.8 # damping factor
        numloops = 10

        npages = self.graph.size()

        for page in self.graph.find():
            self.ranks[page["url"]] = 1.0 / npages

        for i in range(0, numloops):
            newranks = {}
            graph = self.graph.find()
            for page in graph:
                
                newrank = (1 - d) / npages
                for node in graph:
                    #print page["url"], node["links"]
                    if page["url"] in node["links"]:
                        newrank = newrank + d * (self.ranks[node["url"]] / len(node["links"]))
                        
                newranks[page["url"]] = newrank
            self.ranks = newranks
        

if __name__ == "__main__":
    webHunt = WebHunter()
    print webHunt.ordered_search( 'Hummus')
    #print index
#>>> ['http://udacity.com/cs101x/urank/kathleen.html', 
#    'http://udacity.com/cs101x/urank/nickel.html', 
#    'http://udacity.com/cs101x/urank/arsenic.html', 
#    'http://udacity.com/cs101x/urank/hummus.html', 
#    'http://udacity.com/cs101x/urank/index.html'] 

    print webHunt.ordered_search( 'the')
#>>> ['http://udacity.com/cs101x/urank/nickel.html', 
#    'http://udacity.com/cs101x/urank/arsenic.html', 
#    'http://udacity.com/cs101x/urank/hummus.html', 
#    'http://udacity.com/cs101x/urank/index.html']


    print webHunt.ordered_search( 'babaganoush')
#>>> None
    print webHunt.ranks


    #print webHunt.graph.find(),"loading search.py"
