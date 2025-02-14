from flask import Flask, jsonify
from flask_cors import CORS
from app.services.firebase import init_firebase
import structlog

logger = structlog.get_logger(__name__)

def create_app():
    app = Flask(__name__)
    
    # Initialize CORS
    CORS(app)
    
    # Initialize Firebase
    try:
        init_firebase()
        logger.info("firebase_initialized_successfully")
    except Exception as e:
        logger.error("firebase_initialization_failed", error=str(e))
        raise
    
    # Register blueprints
    from app.routes.webhook import webhook
    app.register_blueprint(webhook, url_prefix='/webhook')

    from .routes import images
    app.register_blueprint(images.bp)

    from .routes import ai_routes
    app.register_blueprint(ai_routes, url_prefix='/api/ai')
    
    @app.route('/')
    def root():
        return jsonify({
            'status': 'error',
            'message': 'Invalid endpoint. Use /webhook/property for property webhooks'
        }), 404
        
    @app.route('/health')
    def health_check():
        return {'status': 'healthy'}, 200
        
    return app