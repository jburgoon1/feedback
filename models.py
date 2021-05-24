from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import backref
from flask_bcrypt import Bcrypt
import app
db = SQLAlchemy()

bcrypt = Bcrypt()

def connect_db(app):
    """Connect to database."""
    db.app = app
    db.init_app(app)

class User(db.Model):
    __tablename__ = "users"
    username = db.Column(db.String(20), primary_key = True)
    password = db.Column(db.String, nullable = True)
    email = db.Column(db.String(50), nullable = True, unique = True)
    first_name = db.Column(db.String(30), nullable = True)
    last_name = db.Column(db.String(30), nullable = True)
    user_feedback = db.relationship("Feedback", backref = "user" )
    @classmethod
    def authenticate(cls, username, password):

        u = User.query.filter_by(username = username).first()

        if u and bcrypt.check_password_hash(u.password, password):
            # return user instance
            return u
        else:
            return False


class Feedback(db.Model):
    __tablename__ = "feedbacks"
    id = db.Column(db.Integer, primary_key = True, auto_increment = True)
    title = db.Column(db.String(100), nullable = True)
    content = db.Column(db.String, nullable = True)
    username = db.Column(db.String, db.ForeignKey("users.username"))

    