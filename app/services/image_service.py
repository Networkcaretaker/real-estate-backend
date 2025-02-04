from typing import List, Dict, Any
from PIL import Image
import io
import os
from firebase_admin import storage, firestore
from uuid import uuid4

class ImageService:
    def __init__(self):
        self.bucket = storage.bucket()
        self.db = firestore.client()
        self.standard_size = (800, 600)
        self.output_format = 'JPEG'
        self.quality = 85

    async def process_property_images(
        self, 
        property_id: str, 
        files: List[Any]
    ) -> List[Dict[str, str]]:
        """Process multiple images for a property"""
        
        # Get next image number for this property
        next_number = await self._get_next_image_number(property_id)
        processed_images = []

        for index, file in enumerate(files, start=next_number):
            # Generate standardized filename
            filename = f"{property_id}-{str(index).zfill(2)}.jpg"
            
            # Process image
            processed_image = await self._process_image(file)
            
            # Upload to Firebase Storage
            image_path = f"properties/{property_id}/images/{filename}"
            blob = self.bucket.blob(image_path)
            blob.upload_from_string(processed_image, content_type='image/jpeg')
            
            # Generate public URL
            url = blob.public_url
            
            # Create image metadata document
            image_id = str(uuid4())
            image_ref = self.db.collection('properties').document(property_id)\
                           .collection('images').document(image_id)
            
            image_data = {
                'storage_url': url,
                'filename': filename,
                'title': '',
                'description': '',
                'order': index,
                'created_at': firestore.SERVER_TIMESTAMP
            }
            
            await image_ref.set(image_data)
            processed_images.append({'id': image_id, **image_data})
            
        return processed_images

    async def _process_image(self, file_data: bytes) -> bytes:
        """Process a single image"""
        image = Image.open(io.BytesIO(file_data))
        
        # Convert to RGB if necessary
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        # Resize maintaining aspect ratio
        image.thumbnail(self.standard_size, Image.Resampling.LANCZOS)
        
        # Center crop if aspect ratio doesn't match
        current_ratio = image.size[0] / image.size[1]
        target_ratio = self.standard_size[0] / self.standard_size[1]
        
        if current_ratio != target_ratio:
            if current_ratio > target_ratio:
                # Image is too wide
                new_width = int(image.size[1] * target_ratio)
                left = (image.size[0] - new_width) // 2
                image = image.crop((left, 0, left + new_width, image.size[1]))
            else:
                # Image is too tall
                new_height = int(image.size[0] / target_ratio)
                top = (image.size[1] - new_height) // 2
                image = image.crop((0, top, image.size[0], top + new_height))
        
        # Save with compression
        output = io.BytesIO()
        image.save(output, format=self.output_format, quality=self.quality, optimize=True)
        return output.getvalue()

    async def _get_next_image_number(self, property_id: str) -> int:
        """Get the next available image number for a property"""
        images_ref = self.db.collection('properties').document(property_id)\
                        .collection('images')
        images = await images_ref.order_by('filename', direction='DESCENDING')\
                                .limit(1).get()
        
        if not images:
            return 1
            
        last_filename = images[0].get('filename')
        last_number = int(last_filename.split('-')[1].split('.')[0])
        return last_number + 1

    async def update_image_metadata(
        self, 
        property_id: str, 
        image_id: str, 
        metadata: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Update image title and description"""
        image_ref = self.db.collection('properties').document(property_id)\
                       .collection('images').document(image_id)
        
        await image_ref.update(metadata)
        return metadata

    async def update_image_collections(
        self, 
        property_id: str, 
        feature_image_id: str = None,
        interior_image_ids: List[str] = None,
        exterior_image_ids: List[str] = None
    ) -> Dict[str, Any]:
        """Update image collections in property document"""
        property_ref = self.db.collection('properties').document(property_id)
        
        media_data = {}
        if feature_image_id is not None:
            media_data['feature_image_id'] = feature_image_id
        if interior_image_ids is not None:
            media_data['interior_image_ids'] = interior_image_ids
        if exterior_image_ids is not None:
            media_data['exterior_image_ids'] = exterior_image_ids
            
        await property_ref.update({'media': media_data})
        return media_data