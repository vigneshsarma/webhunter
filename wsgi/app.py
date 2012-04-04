import os
import hunter.search as hunter_search
from flask import Flask,render_template,request

app = Flask(__name__)

#url_for('static',filename='style.css')
#url_for('static',filename='favicon.ico')

@app.route('/')
def hello():
    return render_template('base.html')#'Hello World,from Vignesh'+'!'*5

@app.route('/web')
def web():
    results = hunter_search.ordered_search(hunter_search.index, hunter_search.ranks, request.args.get('q'))
    
    if not results:
        results = ["No results found!!!try something else."]
    return render_template('searched.html',results=results,graph=hunter_search.graph)

if __name__ == '__main__':
    port = int(os.environ.get('PORT',5000))
    app.debug = True;
    app.run(host='0.0.0.0',port=port)
