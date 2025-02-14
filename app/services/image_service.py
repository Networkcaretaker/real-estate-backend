# app/services/image_service.py

from typing import List, Dict, Any, Optional, Tuple
from PIL import Image
import io
import os
from firebase_admin import storage, firestore
from uuid import uuid4
from werkzeug.datastructures import FileStorage
from datetime import datetime

class ImageService:
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
    MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
    
    # Image size configurations
    THUMBNAIL_SIZE = (150, 150)
    MEDIUM_SIZE = (800, 600)
    LARGE_SIZE = (1600, 1200)
    
    # Quality settings for different sizes
    THUMBNAIL_QUALITY = 70
    MEDIUM_QUALITY = 85
    LARGE_QUALITY = 90

    def __init__(self):
        self.bucket = storage.bucket()
        self.db = firestore.client()
        self.output_format = 'JPEG'

    def allowed_file(self, filename: str) -> bool:
        """Check if file extension is allowed"""
        return '.' in filename and \
            filename.rsplit('.', 1)[1].lower() in self.ALLOWED_EXTENSIONS

    def process_property_images(
        self, 
        property_id: str, 
        files: List[FileStorage]
    ) -> List[Dict[str, Any]]:
        """Process multiple images for a property"""
        try:
            next_number = self._get_next_image_number(property_id)
            processed_images = []

            for index, file in enumerate(files, start=next_number):
                # Validate file
                if not file or not file.filename:
                    continue
                    
                if not self.allowed_file(file.filename):
                    raise ValueError(f"Invalid file type for {file.filename}")
                    
                if file.content_length and file.content_length > self.MAX_FILE_SIZE:
                    raise ValueError(f"File {file.filename} exceeds maximum size")

                # Read file data
                file_data = file.read()
                
                # Generate standardized filename
                filename = f"{property_id}-{str(index).zfill(2)}.jpg"
                
                # Process image in different sizes and upload
                urls = self._process_and_upload_images(property_id, filename, file_data)
                
                # Create image metadata document
                image_id = str(uuid4())
                image_ref = self.db.collection('properties').document(property_id)\
                               .collection('images').document(image_id)
                
                image_data = {
                    'urls': urls,
                    'filename': filename,
                    'title': '',
                    'description': '',
                    'order': index,
                    'created_at': datetime.utcnow(),
                    'updated_at': datetime.utcnow()
                }
                
                image_ref.set(image_data)
                processed_images.append({'id': image_id, **image_data})
                
            return processed_images
            
        except Exception as e:
            # Log error here
            raise RuntimeError(f"Error processing images: {str(e)}")

    def _process_and_upload_images(
        self, 
        property_id: str, 
        filename: str, 
        file_data: bytes
    ) -> Dict[str, str]:
        """Process and upload image in different sizes"""
        urls = {}
        sizes = {
            'thumbnail': (self.THUMBNAIL_SIZE, self.THUMBNAIL_QUALITY, 'thumbnails'),
            'medium': (self.MEDIUM_SIZE, self.MEDIUM_QUALITY, 'medium'),
            'large': (self.LARGE_SIZE, self.LARGE_QUALITY, 'large')
        }

        for size_key, (dimensions, quality, folder) in sizes.items():
            # Process image for current size
            processed_image = self._process_image(file_data, dimensions, quality)
            
            # Upload to Firebase Storage
            image_path = f"properties/{property_id}/{folder}/{filename}"
            blob = self.bucket.blob(image_path)
            blob.upload_from_string(processed_image, content_type='image/jpeg')
            
            # Set cache control based on size
            cache_time = self._get_cache_control_time(size_key)
            blob.cache_control = f'public, max-age={cache_time}'
            blob.patch()
            
            # Store URL
            urls[size_key] = blob.public_url
            
        return urls

    def _process_image(
        self, 
        file_data: bytes, 
        size: Tuple[int, int], 
        quality: int
    ) -> bytes:
        """Process a single image to specific size"""
        try:
            image = Image.open(io.BytesIO(file_data))
            
            # Convert to RGB if necessary
            if image.mode != 'RGB':
                image = image.convert('RGB')
            
            # For thumbnails, we crop to square first
            if size == self.THUMBNAIL_SIZE:
                image = self._crop_to_square(image)
            
            # Resize maintaining aspect ratio
            image.thumbnail(size, Image.Resampling.LANCZOS)
            
            # Center crop if aspect ratio doesn't match (except for thumbnails)
            if size != self.THUMBNAIL_SIZE:
                image = self._center_crop(image, size)
            
            # Save with compression
            output = io.BytesIO()
            image.save(output, format=self.output_format, quality=quality, optimize=True)
            return output.getvalue()
            
        except Exception as e:
            raise RuntimeError(f"Error processing image: {str(e)}")

    def _crop_to_square(self, image: Image.Image) -> Image.Image:
        """Crop image to square for thumbnail"""
        width, height = image.size
        new_size = min(width, height)
        left = (width - new_size) // 2
        top = (height - new_size) // 2
        right = left + new_size
        bottom = top + new_size
        return image.crop((left, top, right, bottom))

    def _center_crop(
        self, 
        image: Image.Image, 
        target_size: Tuple[int, int]
    ) -> Image.Image:
        """Center crop image to match target aspect ratio"""
        current_ratio = image.size[0] / image.size[1]
        target_ratio = target_size[0] / target_size[1]
        
        if current_ratio != target_ratio:
            if current_ratio > target_ratio:
                # Image is too wide
                new_width = int(image.size[1] * target_ratio)
                left = (image.size[0] - new_width) // 2
                return image.crop((left, 0, left + new_width, image.size[1]))
            else:
                # Image is too tall
                new_height = int(image.size[0] / target_ratio)
                top = (image.size[1] - new_height) // 2
                return image.crop((0, top, image.size[0], top + new_height))
        return image

    def _get_cache_control_time(self, size_key: str) -> int:
        """Get cache control time based on image size"""
        cache_times = {
            'thumbnail': 86400,    # 24 hours
            'medium': 604800,      # 1 week
            'large': 2592000       # 30 days
        }
        return cache_times.get(size_key, 86400)

    def _get_next_image_number(self, property_id: str) -> int:
        """Get the next available image number for a property"""
        images_ref = self.db.collection('properties').document(property_id)\
                        .collection('images')
        images = images_ref.order_by('filename', direction=firestore.Query.DESCENDING)\
                          .limit(1).get()
        
        if not images or len(list(images)) == 0:
            return 1
            
        last_filename = list(images)[0].get('filename')
        last_number = int(last_filename.split('-')[1].split('.')[0])
        return last_number + 1