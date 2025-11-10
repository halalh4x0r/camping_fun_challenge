from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    
    # Configuration
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///camping.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False
    
    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    
    # Register blueprints
    from server.routes.campers import campers_bp
    from server.routes.activities import activities_bp
    from server.routes.signups import signups_bp
    
    app.register_blueprint(campers_bp, url_prefix='/campers')
    app.register_blueprint(activities_bp, url_prefix='/activities')
    app.register_blueprint(signups_bp, url_prefix='/signups')
    
    return app