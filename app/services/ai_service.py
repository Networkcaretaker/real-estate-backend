from typing import Dict, Any, List
import structlog
from google import genai
import os
from PIL import Image
import requests
from io import BytesIO
import json
from app.services.firebase import FirebaseService

logger = structlog.get_logger(__name__)

class AIService:
    def __init__(self):
        self.logger = logger.bind(service="ai_service")
        # Initialize Gemini API
        self.client = genai.Client(api_key=os.getenv('GOOGLE_AI_API_KEY'))
        self.model = "gemini-2.0-flash"
        self.firebase = FirebaseService()

    def _build_prompt(self, property_title: str, property_description: str, versions: List[str]) -> str:
        """Build the prompt for the AI model"""
        
        return f"""As a high-end real estate image specialist, analyze this property image and provide a professional, SEO-optimized title and description. Highlights key selling points visible in the image. Using real estate industry standard terminology, Incorporate relevant keywords naturally, Maintain a professional tone, and Focuses on unique, visible features. 

        Provide a response using the selected tone for each of the following versions {versions}. 

        For additional reference here is the:
        Property Title: {property_title}
        Property Description: {property_description}

        Respond in JSON format with an array of objects containing:
        "version": "version type",
        "image_title": "Brief, compelling title (max 80 chars)",
        "image_description": "Detailed, SEO-optimized description (max 300 chars)"
        """
    
    def _build_property_prompt(
        self,
        property_type: str,
        property_location: str,
        property_data: Dict[str, Any],
        property_summary: str,
        versions: List[str]
    ) -> str:
        """Build the prompt for property content generation"""

        # Create a formatted example JSON structure
        example_json = {
            "version": "version name",
            "title": "property title",
            "description": "full description",
            "excerpt": "brief summary"
        }

        return f'''As a high-end real estate specialist, analyze this {property_type} located in {property_location} and using the image and the information provided, create an engaging title, description and excerpt for this real estate. Highlight key selling points using real estate industry standard terminology, incorporate relevant keywords naturally and maintain a professional tone.

        Property Category: {property_type}
        Primary Location: {property_location}
        Property Summary: {property_summary}
        Property Details: {json.dumps(property_data, indent=2)}
        Versions Required: {versions}
        Market Position: High-end real estate market

        For each requested version ({versions}), maintain the core information while adapting:
        - Tone and vocabulary
        - Emphasis points
        - Writing style
        - Market positioning

        Content Requirements:
        - Title: Create a compelling, location-specific title that highlights the property's main selling points
        - Description: Craft a flowing narrative that guides potential buyers through the property
        - Excerpt: Deliver a concise, keyword-rich summary focusing on unique selling propositions

        Structural Guidelines:
        1. Title (80 chars max):
        - Include location and key property type
        - Highlight a standout feature
        - Use market-appropriate terminology

        2. Description (2000 chars max):
        - Opening: Strong location context and property positioning
        - Body: Progressive reveal of property features and spaces
        - Closing: Emphasize lifestyle benefits and investment potential
        - Natural keyword integration
        - <br> tags for section breaks only
        - Minimal use of <b> and <i> tags for emphasis
        - Do not use any bullet points or lists.
        - Avoid repetition of descriptive adjectives.

        3. Excerpt (300 chars max):
        - Lead with strongest selling point
        - Include location context
        - Mention key features
        - End with value proposition

        IMPORTANT: Respond with a JSON array where each object has EXACTLY these fields:
        {json.dumps(example_json, indent=2)}

        Keep all responses in valid JSON format.
        '''

    def _process_ai_request(self, image_url: str, prompt: str) -> List[Dict[str, str]]:
        try:
            # Get image from URL
            self.logger.info("fetching_image", url=image_url)
            response = requests.get(image_url)
            response.raise_for_status()
            
            image = Image.open(BytesIO(response.content))
            self.logger.info("image_fetched_successfully", 
                            size=f"{image.size[0]}x{image.size[1]}")

            # Generate content using Gemini API
            self.logger.info("generating_ai_content")
            response = self.client.models.generate_content(
                model=self.model, 
                contents=[prompt, image]
            )
            
            # Fix this logging statement - use key-value pairs for structlog
            self.logger.info("ai_response_received", response_text=response.text)
            
            if not response or not response.text:
                raise ValueError("Empty response from AI service")

            # Clean up response
            cleaned_response = response.text.strip()
            if cleaned_response.startswith("```json"):
                cleaned_response = cleaned_response[7:]
            if cleaned_response.endswith("```"):
                cleaned_response = cleaned_response[:-3]
            cleaned_response = cleaned_response.strip()
            
            # Log cleaned response
            self.logger.info("cleaned_response_prepared", response=cleaned_response)
            
            # Parse response
            result = json.loads(cleaned_response)
            
            # Validate response format
            if not isinstance(result, list):
                raise ValueError("Invalid response format - expected array")
                
            # Update validation for property content
            for item in result:
                required_fields = ["version", "title", "description", "excerpt"]
                if not all(key in item for key in required_fields):
                    self.logger.error("missing_required_fields", item=item)
                    raise ValueError(f"Invalid response item format. Required fields: {required_fields}")
            
            return result

        except json.JSONDecodeError as e:
            self.logger.error("json_parse_error", 
                            error=str(e), 
                            response=cleaned_response)
            raise ValueError(f"Failed to parse AI response: {str(e)}")
        except Exception as e:
            self.logger.error("ai_request_error", 
                            error=str(e))
            raise ValueError(f"AI request failed: {str(e)}")

    def analyze_property_image(
        self,
        property_id: str,
        image_id: str,
        versions: List[str]
    ) -> List[Dict[str, str]]:
        """Analyze property image using provided IDs"""
        try:
            # Get property data from Firebase
            property_data = self.firebase.get_property(property_id)
            if not property_data:
                raise ValueError(f"Property not found: {property_id}")

            # Get image data from Firebase
            image_data = self.firebase.get_property_image(property_id, image_id)
            if not image_data:
                raise ValueError(f"Image not found: {image_id}")

            # Get signed URL for the image
            signed_url = self.firebase.get_image_download_url(image_data["urls"]["large"])

            # Build prompt
            prompt = self._build_prompt(
                property_data["title"],
                property_data["description"],
                versions
            )

            # Process image with signed URL
            response = self._process_ai_request(signed_url, prompt)

            # Save results to image ai_meta in firebase
            self.firebase.update_image_ai_meta(property_id, image_id, response)
            return response

        except Exception as e:
            self.logger.error("image_analysis_error",
                            error=str(e),
                            property_id=property_id,
                            image_id=image_id)
            raise

    def analyze_property_content(
        self,
        property_id: str,
        image_id: str,
        versions: List[str]
    ) -> List[Dict[str, str]]:
        """Analyze property and generate content using provided property and image"""
        try:
            # Get property data from Firebase
            property_data = self.firebase.get_property(property_id)
            if not property_data:
                raise ValueError(f"Property not found: {property_id}")

            # Get image data from Firebase
            image_data = self.firebase.get_property_image(property_id, image_id)
            if not image_data:
                raise ValueError(f"Image not found: {image_id}")

            # Get signed URL for the image
            signed_url = self.firebase.get_image_download_url(image_data["urls"]["medium"])

            # Prepare property information
            property_type = property_data.get("details", {}).get("property_type", "property")
            location = property_data.get("location", {})
            property_location = f"{location.get('town', '')}, {location.get('municipality', '')}"

            # Clean and structure property data
            clean_data = {
                "details": {k: v for k, v in property_data.get("details", {}).items() if v},
                "rooms": {k: v for k, v in property_data.get("rooms", {}).items() if v},
                "features": {k: v for k, v in property_data.get("features", {}).items() if v and v != []},
                "price": property_data.get("price")
            }

            # Build prompt
            self.logger.info("Building prompt with data", 
                            property_type=property_type,
                            location=property_location,
                            versions=versions)

            prompt = self._build_property_prompt(
                property_type=property_type,
                property_location=property_location,
                property_data=clean_data,
                property_summary=property_data.get("excerpt", ""),
                versions=versions
            )

            self.logger.info("Prompt built successfully")

            # Process image with signed URL
            response = self._process_ai_request(signed_url, prompt)
            self.logger.info("AI request processed successfully")

            # Save results to property ai_meta in firebase
            self.firebase.update_property_ai_meta(
                property_id=property_id,
                image_id=image_id,
                ai_response=response
            )

            return response

        except Exception as e:
            self.logger.error("property_analysis_error",
                            error=str(e),
                            property_id=property_id,
                            image_id=image_id)
            raise
    