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
    return "home"

@app.route("/<slug>")
def get_page(slug):
    context = {
        'page': wordpress.get_page(slug)
    }

    return render_template('page.html', **context)

if __name__ == "__main__":
    app.run(**config['server'])