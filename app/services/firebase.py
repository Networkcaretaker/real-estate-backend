import firebase_admin
from firebase_admin import credentials, firestore
import os
import structlog
from typing import Dict, Any

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
            doc = self.db.collection('properties').document(str(property_id)).get()
            
            if not doc.exists:
                self.logger.warning("property_not_found", property_id=property_id)
                return None
                
            return doc.to_dict()
            
        except Exception as e:
            self.logger.error(
                "property_retrieval_failed",
                property_id=property_id,
                error=str(e)
            )
            raise