# app/routes/images.py

from flask import Blueprint, request, jsonify
from werkzeug.exceptions import BadRequest
from app.services.image_service import ImageService

bp = Blueprint('images', __name__, url_prefix='/api')

@bp.route('/properties/<property_id>/images', methods=['POST', 'OPTIONS'])
def upload_images(property_id):
    if request.method == 'OPTIONS':
        return '', 204
        
    try:
        if 'files' not in request.files:
            raise BadRequest('No files provided')
            
        files = request.files.getlist('files')
        if not files or not any(file.filename for file in files):
            raise BadRequest('No valid files provided')
            
        image_service = ImageService()
        uploaded_images = image_service.process_property_images(property_id, files)
        
        return jsonify(uploaded_images), 201
        
    except BadRequest as e:
        return jsonify({'error': str(e)}), 400
    except ValueError as e:
        return jsonify({'error': str(e)}), 422
    except Exception as e:
        # Log error here
        return jsonify({'error': 'Internal server error'}), 500

@bp.route('/properties/<property_id>/images/<image_id>', methods=['PUT'])
def update_image_metadata(property_id, image_id):
    try:
        data = request.get_json()
        if not data:
            raise BadRequest('No data provided')
            
        allowed_fields = {'title', 'description'}
        update_data = {k: v for k, v in data.items() if k in allowed_fields}
        
        if not update_data:
            raise BadRequest('No valid fields to update')
            
        image_service = ImageService()
        updated = image_service.update_image_metadata(property_id, image_id, update_data)
        
        return jsonify(updated)
        
    except BadRequest as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        # Log error here
        return jsonify({'error': 'Internal server error'}), 500