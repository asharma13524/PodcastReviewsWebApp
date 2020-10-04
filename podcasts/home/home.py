from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from flask import current_app as app
from ..forms import ReviewForm
from .. import db
from ..models import Review, User
from datetime import datetime as dt
from flask_login import current_user, login_required
from datetime import date
from werkzeug.exceptions import abort
from werkzeug.utils import secure_filename
from os import path
from wtforms.form import *

home_bp = Blueprint('home_bp', __name__,
                    template_folder="templates", static_folder="static")


@home_bp.route('/')
def home():
    all_reviews = Review.query.all()

    return render_template('/home.html', title="Home", all_reviews=all_reviews)


@home_bp.route('/about')
def about():
    return render_template('/about.html', title='About')


def get_review(id, check_author=True):
    review = Review.query.filter_by(id=id).first()
    if review is None:
        abort(404, "Review id {0} doesn't exist.".format(id))

    if check_author and review.reviewer_id != current_user.id:
        flash('You did not write that post!')
        return redirect(render_template('/home.html'))

    return review


@home_bp.route('/create', methods=["GET", "POST"])
@login_required
def create():
    form = ReviewForm()
    if form.validate_on_submit():
        reviewer_id = current_user.id
        reviewer_username = current_user.username
        review_date = dt.now()
        podcast_guest = request.form['podcast_guest']
        picture = form.podcast_img.data
        filename = secure_filename(picture.filename)
        picture.save(path.join(app.config['UPLOAD_FOLDER'], filename))
        podcast_host = request.form['podcast_host']
        podcast_rating = request.form['podcast_rating']
        podcast_genre = request.form['podcast_genre']
        podcast_review = request.form['podcast_review']
        review = Review(reviewer_id=reviewer_id, review_date=review_date, reviewer_username=reviewer_username, podcast_guest=podcast_guest, podcast_host=podcast_host, podcast_img=filename, podcast_rating=podcast_rating, podcast_genre=podcast_genre, podcast_review=podcast_review)
        db.session.add(review)
        db.session.commit()


        return redirect(url_for('home_bp.home'))

    return render_template('/create.html', title='Create a Review', form=form)


@home_bp.route("/<int:id>/update", methods=["GET", "POST"])
@login_required
def update(id):
    review = get_review(id)
    form = ReviewForm(obj=review)

    if form.validate_on_submit():
        review.reviewer_id = current_user.id
        review.review_date = dt.now()
        review.reviewer_username = current_user.username
        review.podcast_img = review.podcast_img
        review.podcast_guest = request.form['podcast_guest']
        review.podcast_host = request.form['podcast_host']
        review.podcast_rating = request.form['podcast_rating']
        review.podcast_genre = request.form['podcast_genre']
        review.podcast_review = request.form['podcast_review']

        db.session.commit()

        return redirect(url_for("home_bp.home"))

    return render_template('/update.html', title='Update a Review', form=form, review=review)


@home_bp.route("/<int:id>/delete", methods=["POST"])
@login_required
def delete(id):
    review = get_review(id)
    db.session.delete(review)
    db.session.commit()

    return redirect(url_for("home_bp.home"))




