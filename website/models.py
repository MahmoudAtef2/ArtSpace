from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

# database for the user information
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    pro_image = db.Column(db.String(20), unique=False,
                          nullable=False, default='defulat.jpg')
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    posts = db.relationship('Post', backref='user', passive_deletes=True)

# database for the post
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    caption = db.Column(db.Text, nullable=True)
    post_image = db.Column(db.String(150), unique=False,
                           nullable=False, default='imge.jpg')
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    author = db.Column(db.Integer, db.ForeignKey(
        'user.id', ondelete="CASCADE"), nullable=False)
