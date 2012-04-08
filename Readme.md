#WebHunter
##A personal web search engine.

This builds on the basic code for search engine, indexing and ranking from Udacity Class CS 101.On top of that I have added a web interface,using flask framework.The basic code form udacity is found at *wsgi/hunter/search.py*.

##Changes:
* A web interface have been added using flask web-framework and jinja2 templating engine.
* Use HTMLParser to provide a better and more accurate HTML parsing.
* Extract more use full data from html like title, scentences containing the word etc.
* Made the whole thing search.py into a class.
* MangoDB provides a persistent index and graph storage.
  * `IndexHunt.py` and `GraphHunt.py` act as abstraction for this purpouse.

##TODO:
* Use urllib to get real web-pages and index those.
* Add a web interface for adding new links to index.