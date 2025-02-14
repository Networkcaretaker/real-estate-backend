from typing import Dict, List, Any
from enum import Enum
import re

class FeatureCategory(Enum):
    INTERIOR = "interior"
    EXTERIOR = "exterior"
    LUXURY = "luxury"
    AMENITIES = "amenities"
    UTILITIES = "utilities"

class FeatureProcessor:
    """Service class to process and categorize property features"""
    
    def __init__(self):
        # Define feature categories and their keywords
        self._category_keywords = {
            FeatureCategory.INTERIOR: {
                'kitchen', 'equipped kitchen', 'bathroom', 'bedroom', 'living room', 
                'double glazed', 'air conditioning', 'heating', 'floor', 'ceiling',
                'storage', 'lift', 'elevator', 'fitted', 'wardrobe'
            },
            FeatureCategory.EXTERIOR: {
                'garden', 'private garden', 'terrace', 'balcony', 'parking',
                'private parking', 'garage', 'pool', 'private pool', 'fence',
                'gate', 'driveway', 'landscape', 'patio', 'bbq area'
            },
            FeatureCategory.LUXURY: {
                'spa', 'sauna', 'jacuzzi', 'gym', 'wine cellar',
                'home theater', 'smart home', 'security system',
                'infinity pool', 'tennis court', 'cinema room'
            },
            FeatureCategory.AMENITIES: {
                'wifi', 'internet', 'cable', 'satellite', 'intercom',
                'alarm', 'surveillance', 'fitness', 'playground',
                'community pool', 'gated community'
            },
            FeatureCategory.UTILITIES: {
                'water', 'electricity', 'gas', 'sewage', 'solar',
                'generator', 'heating system', 'cooling system',
                'air conditioning unit', 'central heating'
            }
        }

    def _sanitize_feature(self, feature: str) -> str:
        """Clean and normalize feature text"""
        # Remove special characters except spaces and hyphens
        feature = re.sub(r'[^\w\s-]', '', feature)
        # Convert to lowercase and strip
        return feature.lower().strip()

    def _categorize_feature(self, feature: str) -> FeatureCategory:
        """Determine the category of a given feature"""
        sanitized_feature = self._sanitize_feature(feature)
        
        # Check each category for keyword matches
        for category, keywords in self._category_keywords.items():
            if any(keyword in sanitized_feature for keyword in keywords):
                return category
                
        # Default to amenities if no specific category is found
        return FeatureCategory.AMENITIES

    def process_features(self, crm_data: Dict[str, Any]) -> Dict[str, List[str]]:
        """
        Process features from CRM data and categorize them
        
        Args:
            crm_data: Dictionary containing feature data from CRM
            
        Returns:
            Dictionary with categorized features
        """
        # Initialize result structure
        processed_features = {
            "interior": [],
            "exterior": [],
            "luxury": [],
            "amenities": [],
            "utilities": []
        }

        # Get features string from CRM data
        features_string = crm_data.get("features", "")
        
        if not features_string:
            return processed_features

        # Split features using the |##| separator
        features = [f.strip() for f in features_string.split("|##|")]
        
        # Process each feature
        for feature in features:
            if not feature:
                continue
                
            # Sanitize and categorize the feature
            sanitized_feature = self._sanitize_feature(feature)
            category = self._categorize_feature(sanitized_feature)
            
            # Add to appropriate category
            processed_features[category.value].append(sanitized_feature)

        # Remove duplicates and sort each category
        for category in processed_features:
            processed_features[category] = sorted(list(set(
                processed_features[category]
            )))

        return processed_features

    def validate_features(self, features: Dict[str, List[str]]) -> bool:
        """
        Validate the processed features structure
        
        Args:
            features: Dictionary of categorized features
            
        Returns:
            bool: True if valid, False otherwise
        """
        required_categories = {
            "interior", "exterior", "luxury", "amenities", "utilities"
        }
        
        # Check structure
        if not all(category in features for category in required_categories):
            return False
            
        # Validate each category contains a list
        if not all(isinstance(features[cat], list) for cat in features):
            return False
            
        # Validate all features are strings and not empty
        for category in features:
            if not all(isinstance(feature, str) and feature.strip() 
                      for feature in features[category]):
                return False
                
        return True