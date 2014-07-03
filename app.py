from flask import Flask, render_template
from flaskwp.wordpress import WordpressAPI
from werkzeug.exceptions import abort

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
    posts = wordpress.get_recent_posts()
    pages = wordpress.get_pages()
    page = wordpress.get_page('home')
    return render_template(
        'home.html',
        pages = pages,
        page = page,
        posts = posts
    )

@app.route("/<slug>")
def get_page(slug):
    page = wordpress.get_page(slug)
    if not page:
        abort(404)
    return render_template('page.html', page = page)


@app.route("/blog/<slug>")
def get_blog_post(slug):
    post = wordpress.get_post(slug)
    if not post:
        abort(404)
    return render_template('post.html', post = post)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == "__main__":
    app.run(**config['server'])