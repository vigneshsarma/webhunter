from cache import cache
from parser import LinkFinder

def qsort(tosort,ranks):
    if tosort == []: 
        return []
    else:
        pivot = tosort[0]
        lesser = qsort([x for x in tosort[1:] if ranks[x] < ranks[pivot]],ranks)
        greater = qsort([x for x in tosort[1:] if ranks[x] >= ranks[pivot]],ranks)
        return greater + [pivot] + lesser

def ordered_search(index, ranks, keyword):
    keyword=keyword.lower()
    if keyword in index:
        results = index[keyword]
        return qsort(results,ranks)
    return None
        



def get_page(url):
    if url in cache:
        return cache[url]
    return ""

#These functions are beeing replaced by a class that implements HTMLParser.

# def get_next_target(page):     
#     start_link = page.find('<a href=')
#     if start_link == -1: 
#         return None, 0
#     start_quote = page.find('"', start_link)
#     end_quote = page.find('"', start_quote + 1)
#     url = page[start_quote + 1:end_quote]
#     return url, end_quote

# def get_all_links(page):
#     links = []
#     while True:
#         url, endpos = get_next_target(page)
#         if url:
#             links.append(url)
#             page = page[endpos:]
#         else:
#             break
#     return links

#def get_all_links(page):
    

    
def union(a, b):
    for e in b:
        if e not in a:
            a.append(e)

def add_page_to_index(index, url, content):
    words = content.split()
    for word in words:
        add_to_index(index, word, url)
        
def add_to_index(index, keyword, url):
    if keyword in index:
        if url not in index[keyword]:
            index[keyword].append(url)
    else:
        index[keyword] = [url]
    
def lookup(index, keyword):
    if keyword in index:
        return index[keyword]
    else:
        return None

def crawl_web(seed): # returns index, graph of inlinks
    tocrawl = [seed]
    crawled = []
    graph = {}  # <url>, [list of pages it links to]
    index = {} 
    while tocrawl: 
        page = tocrawl.pop()
        if page not in crawled:
            content = get_page(page)
            outlinks,content,title = LinkFinder().start_parsing(content)
            add_page_to_index(index, page, content)
            graph[page] = outlinks
            union(tocrawl, outlinks)
            crawled.append(page)
    return index, graph

def compute_ranks(graph):
    d = 0.8 # damping factor
    numloops = 10
    
    ranks = {}
    npages = len(graph)
    for page in graph:
        ranks[page] = 1.0 / npages
    
    for i in range(0, numloops):
        newranks = {}
        for page in graph:
            newrank = (1 - d) / npages
            for node in graph:
                if page in graph[node]:
                    newrank = newrank + d * (ranks[node] / len(graph[node]))
            newranks[page] = newrank
        ranks = newranks
    return ranks


#Here are some example showing what ordered_search should do:

#Observe that the result list is sorted so the highest-ranking site is at the
#beginning of the list.

#Note: the intent of this question is for students to write their own sorting
#code, not to use the built-in sort procedure.

index, graph = crawl_web('http://udacity.com/cs101x/urank/index.html')
ranks = compute_ranks(graph)

if __name__ == "__main__":
    
    print ordered_search(index, ranks, 'Hummus')
    #print index
#>>> ['http://udacity.com/cs101x/urank/kathleen.html', 
#    'http://udacity.com/cs101x/urank/nickel.html', 
#    'http://udacity.com/cs101x/urank/arsenic.html', 
#    'http://udacity.com/cs101x/urank/hummus.html', 
#    'http://udacity.com/cs101x/urank/index.html'] 

    print ordered_search(index, ranks, 'the')
#>>> ['http://udacity.com/cs101x/urank/nickel.html', 
#    'http://udacity.com/cs101x/urank/arsenic.html', 
#    'http://udacity.com/cs101x/urank/hummus.html', 
#    'http://udacity.com/cs101x/urank/index.html']


    print ordered_search(index, ranks, 'babaganoush')
#>>> None


    print "loading search.py"
