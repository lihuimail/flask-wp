from flask import Flask, render_template, request, url_for, redirect
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
        'base': "http://cms.ridgestreet.se:3000/api"
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


@app.route("/search")
def get_search_results():
    query = request.args.get("q")
    posts = wordpress.get_search_results(query)
    if not posts:
        abort(404)
    return render_template('posts.html', posts = posts, q = query)

@app.route("/comment", methods=['POST'])
def post_comment():
    email = request.form.get("email")
    url = request.form.get("url")
    name = request.form.get("name")
    comment = request.form.get("comment")
    post_id = request.form.get("post")

    wordpress.submit_comment(post_id, name, email, comment, url)

    post = wordpress.get_post(post_id = post_id)

    return redirect(url_for('get_custom_post', post_type = 'blog', slug = post['slug']))

@app.route("/category/<category>")
def get_category(category):
    posts = wordpress.get_category_posts(category)
    return render_template('posts.html', posts = posts)

@app.route("/tag/<tag>")
def get_tag(tag):
    posts = wordpress.get_tag_posts(tag)
    return render_template('posts.html', posts = posts)

@app.route("/blog/<slug>")
def get_blog_post(slug):
    post = wordpress.get_post(slug)
    if not post:
        abort(404)
    return render_template('post.html', post = post)

@app.route("/author/<slug>")
def get_author(slug):
    posts = wordpress.get_author_posts(slug)
    if not posts:
        abort(404)
    return render_template('posts.html', posts = posts)

@app.route("/case")
def get_cases():
    cases = wordpress.get_posts(post_type='case')
    if not cases:
        abort(404)
    return render_template('posts.html', posts = cases, post_type = 'case')

@app.route("/<post_type>/<slug>")
def get_custom_post(post_type, slug):
    post = wordpress.get_post(slug, post_type)
    if not post:
        abort(404)
    return render_template('post.html', post = post)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == "__main__":
    app.run(**config['server'])
