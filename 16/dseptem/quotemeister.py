from flask import Flask, render_template
import requests
from json import JSONDecodeError
import webview
from multiprocessing import Process
app = Flask(__name__)

quotes_url = 'http://api.forismatic.com/api/1.0/'
wiki_url = 'https://en.wikipedia.org/w/api.php?action=query&format=json&prop=extracts&titles=TITLEHERE&redirects=1&utf8=1&exintro=1&explaintext=1'


@app.route("/")
def wisdom():
    quote, author = get_random_quote()
    bio = get_author_bio(author)
    return render_template('index.html', quote=quote, author=author, bio=bio)


def get_random_quote():
    while True:
        try:
            j = requests.post(quotes_url, data={'method': 'getQuote', 'format': 'json', 'lang': 'en'}).json()
        except JSONDecodeError:
            continue
        return j['quoteText'], j['quoteAuthor']


def get_author_bio(author_name):
    query_url = wiki_url.replace('TITLEHERE', author_name)
    try:
        j = requests.get(query_url).json()
        for p in j['query']['pages']:
            if 'may refer to' in j['query']['pages'][p]['extract']:
                return "Biography not available =("
            return j['query']['pages'][p]['extract']
    except:
        return "Biography not available =("


def start_web():
    app.run()


def start_view():
    webview.create_window('Wisdom of the Ages', 'http://127.0.0.1:5000')

if __name__ == "__main__":
    server = Process(target=start_web)
    server.start()
    view = Process(target=start_view)
    view.start()
    view.join()
    server.terminate()
