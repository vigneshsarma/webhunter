from cache import cache
from parser import LinkFinder


class WebHunter:
    def __init__(self):
        self.index, self.graph = {},{}# <url>, [list of pages it links to]
        self.crawl_web('http://udacity.com/cs101x/urank/index.html')
        self.ranks = {}
        self.compute_ranks()

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
        if keyword in self.index:
            results = self.index[keyword]
            return self.qsort(results,self.ranks)
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
        if keyword in self.index:
            if url not in self.index[keyword]:
                self.index[keyword].append(url)
        else:
            self.index[keyword] = [url]

    def lookup(self, keyword):
        if keyword in self.index:
            return self.index[keyword]
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
                self.graph[page] = (outlinks,title,content)
                self.union(tocrawl, outlinks)
                crawled.append(page)

    def compute_ranks(self):
        d = 0.8 # damping factor
        numloops = 10

        npages = len(self.graph)
        for page in self.graph:
            self.ranks[page] = 1.0 / npages

        for i in range(0, numloops):
            newranks = {}
            for page in self.graph:
                newrank = (1 - d) / npages
                for node in self.graph:
                    if page in self.graph[node][0]:
                        newrank = newrank + d * (self.ranks[node] / len(self.graph[node][0]))
                newranks[page] = newrank
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


    print "loading search.py"
