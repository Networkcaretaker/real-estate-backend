from flask import Blueprint, request, jsonify
from app.services.data_pipeline import DataPipeline
from app.utils.errors import error_handler
from functools import wraps
import os
import structlog

logger = structlog.get_logger(__name__)
webhook = Blueprint('webhook', __name__)

@webhook.before_request
def log_request_info():
    logger.info("webhook_request_received",
        method=request.method,
        url=request.url,
        path=request.path,
        headers=dict(request.headers),
        data=request.get_data(as_text=True)
    )

def check_auth(username, password):
    """Check if the username and password match"""
    return username == os.getenv('API_USERNAME') and password == os.getenv('API_PASSWORD')

def authenticate():
    """Send 401 response that enables basic auth"""
    return jsonify({
        'status': 'error',
        'message': 'Could not verify your credentials'
    }), 401, {'WWW-Authenticate': 'Basic realm="Login Required"'}

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated

@webhook.route('/property', methods=['POST'])
@requires_auth
@error_handler
def handle_property_webhook():
    """Handle incoming property data from CRM webhook"""
    try:
        logger.info("property_webhook_received", 
                   content_length=request.content_length,
                   content_type=request.content_type)
        
        if not request.is_json:
            return jsonify({
                'status': 'error',
                'message': 'Content-Type must be application/json'
            }), 400

        data = request.json
        if not data:
            return jsonify({
                'status': 'error',
                'message': 'No data provided'
            }), 400

        pipeline = DataPipeline()
        result = pipeline.process_property_data(data)
        
        logger.info("property_webhook_processed", 
                   status='success')
        
        return jsonify({
            'status': 'success',
            'message': 'Property data processed successfully',
            'property_id': result.get('property_id')
        }), 200
        
    except Exception as e:
        logger.error("property_webhook_error", 
                    error=str(e),
                    exc_info=True)
        raise