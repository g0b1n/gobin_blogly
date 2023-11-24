from flask import Flask, request, render_template, redirect, flash, session
# from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post, Tag, PostTag
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
    """Show a page with info on all users"""
    users = User.query.order_by(User.last_name, User.first_name).all()
    return render_template('users/index.html', users=users)


@app.route('/users/new', methods=["GET"])
def user_new_form():
    """display form to add new users"""
    return render_template('users/new.html')


@app.route('/users/new', methods=["POST"])
def create_user():
    """Handles form submissions for creating new user"""

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
def users_edit(user_id):
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


##### POST ROUTES --------- #####

@app.route('/users/<int:user_id>/posts/new')
def posts_new_form(user_id):
    """Shows a form to create a new post for a user"""

    user = User.query.get_or_404(user_id)
    tags = Tag.query.all()
    return render_template('posts/new.html', user=user, tags=tags)


@app.route('/users/<int:user_id>/posts/new', methods=["POST"])
def post_new(user_id):
    """Handles form submission for new post form users"""

    user = User.query.get_or_404(user_id)
    tags_id = [int(num) for num in request.form.getlist("tags")]
    tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()

    new_post = Post(title=request.form['title'],
                    content=request.form['content'],
                    user=user, tags=tags)
    
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
    tags = Tag.query.all()
    return render_template('posts/edit.html', post=post, tags=tags)


@app.route('/posts/<int:post_id>/edit', methods=["POST"])
def posts_update(post_id):
    """Handle form submission for updating existing post"""

    post = Post.query.get_or_404(post_id)
    post.title = request.form['title']
    post.content = request.form['content']

    tags_ids = [int(num) for num in request.form.getlist("tags")]
    post.tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()

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


##### TAG ROUTES --------- #####

@app.route('/tags')
def tags_index():
    """Shows all tags"""

    tags = Tag.query.all()
    
    return render_template('tags/index.html', tags=tags)

@app.route('/tags/new')
def tags_new_form():
    """Form to create new tags"""

    posts = Post.query.all()

    return render_template('tags/new.html', posts=posts)


@app.route('/tags/new', methods=["POST"])
def tags_new():
    """Handles form submission for new tags"""

    posts_ids = [int(num) for num in request.form.getlist("posts")]
    posts = Post.query.filter(Post.id.in_(post_ids)).all()
    new_tag = Tag(name = request.form['name'], posts = posts)

    db.session.add(new_tag)
    db.session.commit()
    flash(f"Tag '{new_tag.name} has been added")

    return redirect("/tags")


@app.route('/tags/<int:tag_id>')
def tags_shows(tag_id):
    """Info on specific tag"""

    tag = Tag.query.get_or_404(tag_id)

    return render_template('tags/show.html', tag = tag)


@app.route('/tags/<int:tag_id>/edit')
def tags_edit_form(tag_id):
    """Show form to edit an existing tag"""

    tag = Tag.query.get_or_404(tag_id)
    posts = Post.query.all()

    return render_template('tags/edit.html', tag = tag, posts = posts)

@app.route('/tags/<int:tag_id>/edit', methods=["POST"])
def tags_edit(tag_id):
    """Handle submission for updating an existing tag"""

    tag = Tag.query.get_or_404(tag_id)
    tag.name = request.form['name']
    post_ids = [int(num) for num in request.form.getlist("posts")]
    tag.posts = Post.query.filter(Post.id.in_(post_ids)).all()

    db.session.add(tag)
    db.session.commit()
    flash(f"Tag '{tag.name}' has been updated")

    return redirect('/tags')

@app.route('/tags/<int:tag_id>/delete', methods=["POST"])
def tags_destroy(tag_id):
    """Handles submission for deleting existing tag"""

    tag = Tag.query.get_or_404(tag_id)

    db,session.delete(tag)
    db.session.commit()
    flash(f"Tag '{tag.name}' has been deleted")

    return redirect('/tags')