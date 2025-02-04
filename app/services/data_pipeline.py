from typing import Dict, Any
import structlog
from app.services.firebase import FirebaseService

logger = structlog.get_logger(__name__)

class DataPipeline:
    def __init__(self):
        self.firebase = FirebaseService()
        self.logger = logger.bind(service="data_pipeline")

    def process_property_data(self, crm_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process and store property data from CRM"""
        try:
            self.logger.info("processing_property_data", 
                           property_id=crm_data.get('id'))

            # Transform data to our schema
            property_data = {
                "title": crm_data.get("title", ""),
                "description": crm_data.get("description", ""),
                "price": float(crm_data.get("price", 0)),
                "website_status": "disabled",
            }

            # Store in Firebase
            result = self.firebase.create_or_update_property(
                crm_data.get('id'), 
                property_data
            )
            
            self.logger.info(
                "property_data_processed",
                property_id=crm_data.get('id'),
                status="success"
            )
            
            return result

        except Exception as e:
            self.logger.error(
                "property_data_processing_error",
                property_id=crm_data.get('id'),
                error=str(e)
            )
            raise