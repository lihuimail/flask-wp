from flask import Flask, render_template
from flaskwp.wordpress import WordpressAPI

app = Flask(__name__)

config = {
    'server': {
        'host': '0.0.0.0',
        'port': 3001,
        'debug': True
    },
    'cms': {
        'base': "http://cms.tieroom.dev/api"
    }
}

wordpress = WordpressAPI(api_root = config['cms']['base'])

@app.route("/")
def home():
    pages = wordpress.get_pages()
    page = wordpress.get_page('home')
    return render_template('home.html', pages = pages, page = page)

@app.route("/<slug>")
def get_page(slug):
    page = wordpress.get_page(slug)
    return render_template('page.html', page = page)

if __name__ == "__main__":
    app.run(**config['server'])