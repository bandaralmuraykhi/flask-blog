import os
from flask import Flask, render_template

def create_app(test_config=None):
    # Create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    configure_app(app, test_config)
    register_blueprints(app)
    register_error_handlers(app)
    initialize_extensions(app)
    add_app_routes(app)
    add_template_filters(app)

    return app

def configure_app(app, test_config):
    """Set configurations for the app."""
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite')
    )

    if test_config:
        # Load the test config if passed in
        app.config.from_mapping(test_config)
    else:
        # Load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)

    # Ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

def register_blueprints(app):
    """Register blueprints with the app."""
    from . import auth, blog

    app.register_blueprint(auth.bp)
    app.register_blueprint(blog.bp)
    app.add_url_rule('/', endpoint='blog.index')

def register_error_handlers(app):
    """Register error handlers."""
    @app.errorhandler(403)
    def forbidden_error(error):
        return render_template('403.html'), 403

    @app.errorhandler(404)
    def not_found_error(error):
        return render_template('404.html'), 404

    @app.errorhandler(500)
    def internal_error(error):
        return render_template('500.html'), 500

def initialize_extensions(app):
    """Initialize extensions for the app."""
    from . import db
    db.init_app(app)

def add_app_routes(app):
    """Add routes to the app."""
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

def add_template_filters(app):
    """Add custom template filters."""
    @app.template_filter('short')
    def short_filter(s):
        return ' '.join(s.split(' ')[:10])
