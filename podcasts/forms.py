from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, IntegerField, TextAreaField, RadioField, PasswordField, FileField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo, Optional
from flask_wtf.file import FileField, FileRequired, FileAllowed


class ReviewForm(FlaskForm):
    podcast_guest = StringField('Guest', validators=[DataRequired()])
    podcast_img = FileField('Image', validators=[
                            FileRequired(), FileAllowed(['jpg', 'jpeg', 'png'], 'Images only!')])
    podcast_host = StringField('Host', validators=[DataRequired()])
    podcast_rating = RadioField('Rating', choices=[(i, int(i)) for i in range(1,11)], validators=[DataRequired()])
    podcast_genre = SelectField('Genre', choices=[('Health', 'Health'), ('Investing', 'Investing'), ('Business', 'Business'), (
        'Technology', 'Technology'), ('Psychology', 'Psychology'), ('Fitness', 'Fitness'),('Sports', 'Sports'), ('Arts', 'Arts'), ('Science', 'Science'), ('History', 'History')])
    podcast_review = TextAreaField('Review')
    submit = SubmitField('Submit')


class SignupForm(FlaskForm):
    email = StringField('Email', validators=[Length(min=6), Email(message='Enter a valid email.'), DataRequired()])
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, message="Password must be a minimum of 6 characters.")])
    confirm = PasswordField('Confirm Your Password', validators=[DataRequired(), EqualTo('password', message='Passwords must match.')])
    submit = SubmitField('Register')


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In')


