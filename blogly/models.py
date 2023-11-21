from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
import datetime

db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)

DEFAULT_IMAGE_URL = "https://www.freeiconspng.com/uploads/icon-user-blue-symbol-people-person-generic--public-domain--21.png"

# Models go Below!

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer,
                    primary_key = True,
                    autoincrement = True)

    first_name = db.Column(db.Text,
                    nullable = False,
                    unique = False)

    last_name = db.Column(db.Text,
                    nullable = False,
                    unique=False)

    image_url = db.Column(db.Text,
                    nullable = False,
                    default = DEFAULT_IMAGE_URL)

    posts = db.relationship('Post', backref='user', cascade="all, delete-orphan")
    
#added




    @property
    def full_name(self):
        """Return fullname of users"""
        return f"{self.first_name} {self.last_name}"


class Post(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer,
                    primary_key = True,
                    autoincrement = True)

    title = db.Column(db.Text,
                    nullable = False,
                    unique = False)

    content = db.Column(db.Text,
                    nullable = False,
                    unique = False)

    created_at = db.Column(db.DateTime,
                    nullable = False,
                    default = datetime.datetime.now)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable = False)
    
    @property
    def friendly_date(self):
        """Returns perfectly formatted date and time"""

        return self.created_at.strftime("%a %b %-d %Y, %-I:%M %p")



    