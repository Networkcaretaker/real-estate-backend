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
        
        return f"""As a high-end real estate image specialist, analyze this property image and provide a professional, SEO-optimized title and description. Highlights key selling points visible in the image. Uses real estate industry standard terminology, Incorporate relevant keywords naturally, Maintain a professional tone, and Focuses on unique, visible features. 

Provide a response using the selected tone for each of the following versions {versions}. 

For additional reference here is the:
Property Title: {property_title}
Property Description: {property_description}

Respond in JSON format with an array of objects containing:
"version": "version type",
"image_title": "Brief, compelling title (max 80 chars)",
"image_description": "Detailed, SEO-optimized description (max 300 chars)"
"""
    
    def _process_ai_request(self, image_url: str, prompt: str) -> List[Dict[str, str]]:
        """Process the AI request using the provided image and prompt"""
        try:
            # Get image from URL
            self.logger.info("fetching_image", url=image_url)
            response = requests.get(image_url)
            response.raise_for_status()  # This will raise an HTTPError for bad responses
            
            image = Image.open(BytesIO(response.content))
            self.logger.info("image_fetched_successfully", 
                            size=f"{image.size[0]}x{image.size[1]}")

            # Generate content using Gemini API
            self.logger.info("generating_ai_content")
            response = self.client.models.generate_content(
                model=self.model, 
                contents=[prompt, image]
            )
            
            if not response or not response.text:
                raise ValueError("Empty response from AI service")

            # Clean up response - remove markdown code block syntax
            cleaned_response = response.text.strip()
            if cleaned_response.startswith("```json"):
                cleaned_response = cleaned_response[7:]  # Remove ```json
            if cleaned_response.endswith("```"):
                cleaned_response = cleaned_response[:-3]  # Remove ```
            cleaned_response = cleaned_response.strip()
            
            # Log cleaned response for debugging
            print("Cleaned Response:", cleaned_response)
                
            # Parse response
            result = json.loads(cleaned_response)
            self.logger.info("ai_content_generated_successfully")
            
            # Validate response format
            if not isinstance(result, list):
                raise ValueError("Invalid response format - expected array")
                
            for item in result:
                if not all(key in item for key in ["version", "image_title", "image_description"]):
                    raise ValueError("Invalid response item format")
            
            return result

        except requests.RequestException as e:
            self.logger.error("image_fetch_error", 
                            error=str(e), 
                            url=image_url)
            raise ValueError(f"Failed to fetch image: {str(e)}")
        except json.JSONDecodeError as e:
            self.logger.error("response_parse_error", 
                            error=str(e))
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

    