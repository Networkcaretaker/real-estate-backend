import firebase_admin
from firebase_admin import credentials, firestore
import os
import structlog
from typing import Dict, Any
from datetime import datetime

# import firebase storage
from firebase_admin import storage

logger = structlog.get_logger(__name__)

def init_firebase():
    """Initialize Firebase Admin SDK"""
    try:
        cred = credentials.Certificate(os.getenv('FIREBASE_SERVICE_ACCOUNT'))
        firebase_admin.initialize_app(cred, {
            'storageBucket': os.getenv('FIREBASE_STORAGE_BUCKET')
        })
        logger.info("firebase_initialized_successfully")
    except Exception as e:
        logger.error("firebase_initialization_failed", error=str(e))
        raise

class FirebaseService:
    def __init__(self):
        self.db = firestore.client()
        self.logger = logger.bind(service="firebase")

    def create_or_update_property(self, property_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Create or update a property document in Firestore"""
        try:
            # Add metadata
            data['updated_at'] = firestore.SERVER_TIMESTAMP
            
            # Create or update the document
            property_ref = self.db.collection('properties').document(str(property_id))
            property_ref.set(data, merge=True)
            
            self.logger.info("property_updated", property_id=property_id)
            
            return {
                'status': 'success',
                'property_id': property_id,
                'message': 'Property updated successfully'
            }
            
        except Exception as e:
            self.logger.error(
                "property_update_failed",
                property_id=property_id,
                error=str(e)
            )
            raise

    def get_property(self, property_id: str) -> Dict[str, Any]:
        """Retrieve a property document from Firestore"""
        try:
            self.logger.info("attempting_property_retrieval", property_id=property_id)
            
            # Get collection reference and print it
            collection_ref = self.db.collection('properties')
            print(f"Collection reference: {collection_ref._path}")
            
            # Get document reference
            doc_ref = collection_ref.document(str(property_id))
            print(f"Document reference: {doc_ref._path}")
            
            # Get document
            doc = doc_ref.get()
            print(f"Document exists: {doc.exists}")
            
            if not doc.exists:
                self.logger.warning("property_not_found", 
                                property_id=property_id,
                                collection_path=collection_ref.path)
                return None
            
            data = doc.to_dict()
            print(f"Document data: {data}")
                
            return data
                
        except Exception as e:
            self.logger.error(
                "property_retrieval_failed",
                property_id=property_id,
                error=str(e)
            )
            raise

    # get property image data from firebase collection
    def get_property_image(self, property_id: str, image_id: str) -> Dict[str, Any]:
        """Retrieve a property image data from Firestore"""
        try:
            doc = self.db.collection('properties').document(str(property_id)).collection('images').document(str(image_id)).get()
            
            if not doc.exists:
                self.logger.warning("image_not_found", image_id=image_id)
                return None
                
            return doc.to_dict()
            
        except Exception as e:
            self.logger.error(
                "image_retrieval_failed",
                image_id=image_id,
                error=str(e)
            )
            raise
    
    def get_image_download_url(self, full_url: str) -> str:
        """Get a signed download URL for a Firebase Storage image"""
        try:
            # Extract the path from the full URL
            # From: https://storage.googleapis.com/real-estate-65605.firebasestorage.app/properties/CP000208/large/CP000208-04.jpg
            # To: properties/CP000208/large/CP000208-04.jpg
            storage_path = full_url.split('.app/', 1)[1]
            
            self.logger.info("getting_signed_url", 
                            full_url=full_url,
                            storage_path=storage_path)
            
            # Get bucket
            bucket = storage.bucket()
            
            # Get blob
            blob = bucket.blob(storage_path)
            
            # Generate signed URL that expires in 3600 seconds (1 hour)
            url = blob.generate_signed_url(
                version='v4',
                expiration=3600,
                method='GET'
            )
            
            self.logger.info("generated_signed_url", 
                            storage_path=storage_path)
            
            return url
            
        except Exception as e:
            self.logger.error(
                "signed_url_generation_failed",
                full_url=full_url,
                error=str(e)
            )
            raise

    def update_image_ai_meta(self, property_id: str, image_id: str, ai_response: list[Dict[str, str]]) -> None:
        """Update the ai_meta field of a property image with new AI responses"""
        try:
            # Get reference to the image document
            image_ref = self.db.collection('properties').document(str(property_id))\
                            .collection('images').document(str(image_id))
            
            # Get current ai_meta if it exists
            image_doc = image_ref.get()
            if not image_doc.exists:
                raise ValueError(f"Image not found: {image_id}")
                
            current_time = datetime.now().isoformat()
            
            # Simple update with merge
            image_ref.set({
                'ai_meta': {
                    'last_generated': current_time,
                    'responses': ai_response
                }
            }, merge=True)
            
            self.logger.info("ai_meta_updated",
                            property_id=property_id,
                            image_id=image_id)
                            
        except Exception as e:
            self.logger.error(
                "ai_meta_update_failed",
                property_id=property_id,
                image_id=image_id,
                error=str(e)
            )
            raise