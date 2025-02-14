from flask import Blueprint, request, jsonify
from flask_cors import cross_origin
from app.services.ai_service import AIService
from app.utils.errors import error_handler
import structlog

logger = structlog.get_logger(__name__)

ai_bp = Blueprint('ai', __name__)

@ai_bp.route('/analyze-image', methods=['POST', 'OPTIONS'])
@cross_origin(
    origins=['http://localhost:5173', 'http://127.0.0.1:5173'],
    methods=['POST', 'OPTIONS'],
    allow_headers=['Content-Type', 'Authorization']
)
@error_handler
def analyze_image():
    try:
        logger.info("Received AI analysis request")
        
        # Validate JSON input
        if not request.is_json:
            logger.error("Invalid request: Not JSON")
            return jsonify({
                'status': 'error', 
                'message': 'Invalid request format'
            }), 400

        # Parse request data
        data = request.json
        required_fields = ['property_id', 'image_id', 'versions']
        
        if not all(field in data for field in required_fields):
            logger.error("Missing required fields", data=data)
            return jsonify({
                'status': 'error',
                'message': f'Missing required fields: {", ".join(required_fields)}'
            }), 400

        # Process AI analysis (now a synchronous call)
        ai_service = AIService()
        versions = ai_service.analyze_property_image(
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
        logger.error("AI analysis error", error=str(e), exc_info=True)
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500