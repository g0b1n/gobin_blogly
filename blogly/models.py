from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func

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
                            unique = False)
    image_url = db.Column(db.Text,
                            nullable = False,
                            default = DEFAULT_IMAGE_URL)

    @property
    def full_name(self):
        """Return fullname of users"""
        return f"{self.first_name} {self.last_name}"
    