from flask import Blueprint, request, jsonify
from app.services.ai_service import AIService
from app.utils.errors import error_handler
from functools import wraps
import structlog
from app.routes.webhook import requires_auth  # Import the auth decorator

# Initialize logger
logger = structlog.get_logger(__name__)

# Create blueprint
ai_routes = Blueprint('ai', __name__)

@ai_routes.route('/analyze-image', methods=['POST'])
@requires_auth
@error_handler
async def analyze_image():
    """Handle image analysis requests"""
    try:
        logger.info("image_analysis_request_received",
                   content_type=request.content_type)
        
        if not request.is_json:
            return jsonify({
                'status': 'error',
                'message': 'Content-Type must be application/json'
            }), 400

        data = request.json
        required_fields = ['property_id', 'image_id', 'versions']  # Updated required fields
        
        if not all(field in data for field in required_fields):
            return jsonify({
                'status': 'error',
                'message': f'Missing required fields: {", ".join(required_fields)}'
            }), 400

        # Validate versions
        valid_versions = ["professional", "luxury", "concise", "funny", "call to action"]
        if not all(version in valid_versions for version in data['versions']):
            return jsonify({
                'status': 'error',
                'message': f'Invalid versions. Must be one of: {", ".join(valid_versions)}'
            }), 400

        ai_service = AIService()
        versions = await ai_service.analyze_property_image(
            data['property_id'],
            data['image_id'],
            data['versions']
        )

        return jsonify({
            'status': 'success',
            'data': {
                'versions': versions
            }
        }), 200

    except Exception as e:
        logger.error("image_analysis_error", 
                    error=str(e),
                    exc_info=True)
        raise