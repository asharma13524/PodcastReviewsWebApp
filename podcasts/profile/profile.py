from flask import Blueprint, render_template, request, flash
from faker import Faker
fake = Faker()

profile_bp = Blueprint('profile_bp', __name__, url_prefix='/profile',
                       template_folder='templates', static_folder='static')


@profile_bp.route('/<id>')
def profile(id):
    user = fake.simple_profile()

    return render_template('/profile.html', title='profile template', user=user)
