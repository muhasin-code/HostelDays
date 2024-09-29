import os
from flask import Flask

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    
    # Load configuration
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'HostelDays.sqlite'),
    )
    
    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)
    
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Initialize database
    from . import db
    db.init_app(app)

    # Register Blueprints
    from .user import user_bp
    app.register_blueprint(user_bp)

    from .warden import warden_bp
    app.register_blueprint(warden_bp, url_prefix='/warden')

    from .student import student_bp
    app.register_blueprint(student_bp, url_prefix='/')
    
    return app
