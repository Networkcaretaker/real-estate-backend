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
                "excerpt": crm_data.get("excerpt", ""),
                "price": float(crm_data.get("price", 0)),
                "website_status": "disabled",
                "location": {
                       "country": crm_data.get("country", ""),
                       "region": crm_data.get("region", ""),
                       "municipality": crm_data.get("municipality", ""),
                       "town": crm_data.get("town", ""),
                       "postcode": crm_data.get("postcode", "")
                },
                "details": {
                       "property_type": crm_data.get("property_type", ""),
                       "area_plot": crm_data.get("area_plot", ""),
                       "area_property": crm_data.get("area_property", "")
                },
                "rooms": {
                       "bedrooms": crm_data.get("bedrooms", ""),
                       "bathrooms": crm_data.get("bathrooms", "")
                },
                "features": {
                       "interior": [],
                       "exterior": [],
                       "luxury": [],
                       "aminites": [],
                       "utilities": []
                },
                "flags": {
                       "sold": False,
                       "reduced": False
                },
                "media": {
                       "feature_image_id": None,
                       "interior_image_ids": [],
                       "exterior_image_ids": []
                }
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