"""Compile static assets."""
from flask_assets import Environment, Bundle
from flask import current_app as app

def compile_static_assets(assets):
    #stylesheets bundle
    common_less_bundle = Bundle(
        'src/css/nav.css',
        'src/css/style.css',
        output='dist/css/style.css'
        # extra={'rel': 'stylesheet/css'}
    )
    home_less_bundle = Bundle(
        'home_bp/css/home.css',
        output='dist/css/home.css',
        # extra={'rel': 'stylesheet/css'}
    )
    profile_less_bundle = Bundle(
        'profile_bp/css/profile.css',
        output = 'dist/css/profile.css',
        # extra={'rel': 'stylesheet/css'}
    )
    auth_less_bundle = Bundle(
        'auth_bp/css/auth.css',
        output='dist/css/auth.css',
        # extra={'rel': 'stylesheet/css'}
    )

    assets.register('common_less_bundle', common_less_bundle)
    assets.register('home_less_bundle', home_less_bundle)
    assets.register('profile_less_bundle', profile_less_bundle)
    assets.register('auth_less_bundle', auth_less_bundle)

    if app.config['FLASK_ENV'] == 'development':
        common_less_bundle.build()
        home_less_bundle.build()
        profile_less_bundle.build()
        auth_less_bundle.build()
        return assets