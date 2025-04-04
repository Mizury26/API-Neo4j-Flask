from flask import Flask
from flask_cors import CORS
from app.routes.user_routes import user_bp
from app.routes.post_routes import post_bp
from app.routes.comment_routes import comment_bp

def create_app(config_object):
    app = Flask(__name__)
    app.config.from_object(config_object)
    
    # Enable CORS
    CORS(app)
    
    # Register blueprints
    app.register_blueprint(user_bp, url_prefix='/users')
    app.register_blueprint(post_bp, url_prefix='/posts')
    app.register_blueprint(comment_bp, url_prefix='/comments')
    
    return app