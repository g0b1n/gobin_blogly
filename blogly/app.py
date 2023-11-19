from flask import Flask, request, render_template, redirect, flash, session
# from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User
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
    """Redirects to list of users"""
    return redirect("/users")

@app.route('/users')
def users_index():
    users = User.query.order_by(User.last_name, User.first_name).all()
    return render_template('index.html', users=users)

@app.route('/users/new', methods=["GET"])
def user_new_form():
    """display form to add new users"""
    return render_template('new.html')

@app.route('/users/new', methods=["POST"])
def create_user():

    first_name = request.form["first_name"].capitalize()
    last_name = request.form["last_name"].capitalize()

    new_user = User(
    first_name = request.form["first_name"],
    last_name = request.form["last_name"],
    image_url = request.form["image_url"] or None)

    db.session.add(new_user)
    db.session.commit()

    return redirect("/users")

@app.route('/users/<int:user_id>')
def users_show(user_id):
    """show a page with info about a user"""

    user = User.query.get_or_404(user_id)
    return render_template('show.html', user=user)

@app.route('/users/<int:user_id>/edit')
def user_edit(user_id):
    """show a form to edit an existing user"""

    user = User.query.get_or_404(user_id)
    return render_template('edit.html', user=user)


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

    return redirect('/users')