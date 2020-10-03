from . import db, ma
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy_imageattach.entity import Image, image_attachment



class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    created_on = db.Column(db.DateTime)
    email = db.Column(db.String(100), nullable=False, unique=True)
    username = db.Column(db.String(200), index=False,
                         nullable=False, unique=True)
    password = db.Column(db.String(200), index=False,
                         nullable=False, unique=False)
    last_login = db.Column(db.DateTime, index=False,
                           unique=False, nullable=True)

    def set_password(self, password):
        """Create hashed password with werkzeug"""
        self.password = generate_password_hash(password, method='pbkdf2:sha256')

    def check_password(self, password):
        """Verify password function"""
        return check_password_hash(self.password, password)

    def __repr__(self):
        return "<User {}>".format(self.username)


class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'created_on', 'email', 'username', 'password', 'last_login')


class Review(db.Model):
    '''Model for podcast review'''

    # could add image for each podcast
    __tablename__ = 'reviews'
    id = db.Column(db.Integer, primary_key=True)
    reviewer_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    review_date = db.Column(db.DateTime, index=False)
    reviewer_username = db.Column(
        db.String(200), db.ForeignKey('users.username'))
    podcast_guest = db.Column(db.String(200), index=False, nullable=False)
    podcast_host = db.Column(
        db.String(200), index=False, unique=False, nullable=True)
    podcast_img = db.Column(db.String(200), index=False, nullable=False)
    podcast_rating = db.Column(db.Integer, index=False, nullable=False)
    podcast_genre = db.Column(db.String(200), index=False, nullable=True)
    podcast_review = db.Column(db.Text, index=False, nullable=True)


    def __init__(self, reviewer_id, review_date, reviewer_username, podcast_img, podcast_guest, podcast_host, podcast_rating, podcast_genre, podcast_review):
        self.reviewer_id = reviewer_id
        self.review_date = review_date
        self.reviewer_username = reviewer_username
        self.podcast_img = podcast_img
        self.podcast_guest = podcast_guest
        self.podcast_host = podcast_host
        self.podcast_rating = podcast_rating
        self.podcast_genre = podcast_genre
        self.podcast_review = podcast_review

    def __repr__(self):
        return '<Reviewer: {} Book: {}>'.format(self.reviewer_username, self.podcast_guest)


class ReviewSchema(ma.Schema):
    fields = ('id', 'reviewer_id', 'review_date', 'reviewer_username', 'podcast_img', 'podcast_guest', 'podcast_host', 'podcast_rating', 'podcast_genre', 'podcast_review')


user_schema = UserSchema()
users_schema = UserSchema(many=True)

review_schema = ReviewSchema()
reviews_schema = ReviewSchema(many=True)
