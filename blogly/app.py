from flask import Flask, request, render_template, redirect, flash, session
# from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post
from collections import UserString
from sqlalchemy.sql import text

app = Flask(__name__)

app.app_context().push()

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "ThisMyapp"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
# debug = DebugToolbarExtension(app)

connect_db(app)

@app.route('/')
def root():

    """Redirects to list of users & Shows recent posts by users"""

    posts = Post.query.order_by(Post.created_at.desc()).limit(5).all()
    return render_template("posts/index.html", posts=posts)

#handerrors

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404


@app.route('/users')
def users_index():
    users = User.query.order_by(User.last_name, User.first_name).all()
    return render_template('users/index.html', users=users)


@app.route('/users/new', methods=["GET"])
def user_new_form():
    """display form to add new users"""
    return render_template('users/new.html')


@app.route('/users/new', methods=["POST"])
def create_user():

    """Handles form submissions"""

    first_name = request.form["first_name"].capitalize()
    last_name = request.form["last_name"].capitalize()

    new_user = User(
    first_name = request.form["first_name"],
    last_name = request.form["last_name"],
    image_url = request.form["image_url"] or None)

    db.session.add(new_user)
    db.session.commit()

    flash(f"User{new_user.full_name} has been added")

    return redirect("/users")

@app.route('/users/<int:user_id>')
def users_show(user_id):

    """show a page with info about a user"""

    user = User.query.get_or_404(user_id)
    return render_template('users/show.html', user=user)

@app.route('/users/<int:user_id>/edit')
def user_edit(user_id):
    """show a form to edit an existing user"""

    user = User.query.get_or_404(user_id)
    return render_template('users/edit.html', user=user)


@app.route('/users/<int:user_id>/edit', methods=["POST"])
def users_update(user_id):
    """Handle form submission for updating existing user"""

    user = User.query.get_or_404(user_id)
    user.first_name = request.form['first_name'].capitalize()
    user.last_name = request.form['last_name'].capitalize()
    user.image_url = request.form['image_url']

    db.session.add(user)
    db.session.commit()

    flash(f"User {user.full_name} updated succesfully", "success")

    return redirect("/users")

@app.route('/users/<int:user_id>/delete', methods=["POST"])
def users_destroy(user_id):
    """Handles form submission for deleting existing user"""

    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()

    flash(f"User {user.full_name} has been deleted")

    return redirect('/users')


# POST ROUTES ---------

@app.route('/users/<int:user_id>/post/new')
def posts_new_form(user_id):

    user = User.query.get_or_404(user_id)
    return render_template('posts/new.html', user=user)

@app.route('/users/<int:user_id>/posts/new', methods=["POST"])
def post_new(user_id):

    """Handles form submission for new post form users"""

    user = User.query.get_or_404(user_id)
    new_post = Post(title=request.form['title'],
                    content=request.form['content'],
                    user=user)
    
    db.session.add(new_post)
    db.session.commit()

    flash(f"Post '{new_post.title}' has been added")

    return redirect(f"/users/{user_id}")

@app.route('/posts/<int:post_id>')
def posts_show(post_id):
    """shows page with the post from users"""

    post = Post.query.get_or_404(post_id)
    return render_template('posts/show.html', post=post)

@app.route('/posts/<int:post_id>/edit')
def posts_edit(post_id):
    """shows a form to edit an existing post"""

    post = Post.query.get_or_404(post_id)
    return render_template('posts/edit.html', post=post)


@app.route('/posts/<int:post_id>/edit', methods=["POST"])
def posts_update(post_id):
    """Handle form submission for updating existing post"""

    post = Post.query.get_or_404(post_id)
    post.title = request.form['title']
    post.content = request.form['content']

    db.session.add(post)
    db.session.commit()

    flash(f"Post '{post.title}' is edited")

    return redirect(f"/users/{post.user_id}")

@app.route('/posts/<int:post_id>/delete', methods=["POST"])
def posts_destroy(post_id):
    """Handles form submission for deleting a posts"""

    post = Post.query.get_or_404(post_id)

    db.session.delete(post)
    db.session.commit()

    flash(f"Post '{post.title}' has been deleted")

    return redirect(f"/users/{post.user_id}")
