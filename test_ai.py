from google import genai
import os
import PIL

# Example Property Inormation
property = {
    "title": "Beautiful 3 Bedroom Home",
    "description": "This beautiful 3 bedroom home is located in the heart of the city. It features a spacious living room, modern kitchen, and a large backyard with a pool.",
    "versions": ["professional", "funny", "call to action"],
    "image": "property.jpg"
}

image = PIL.Image.open(property["image"])

content = f'As a high-end real estate image specialist, analyze this property image and provide a professional, SEO-optimized title and description. Highlights key selling points visible in the image. Uses real estate industry standard terminology, Incorporate relevant keywords naturally, Maintain a professional tone, and Focuses on unique, visible features. Provide a responce using the selected tone for each of the following versions {property["versions"]}. For additional reference here is the Property Title:{property["title"]} and Property Description: {property["description"]}. Respond in JSON format: "version": "version type", "image_title": "Brief, compelling title (max 80 chars)", "image_description": "Detailed, SEO-optimized description (max 300 chars)"'

client = genai.Client(api_key=os.getenv('GOOGLE_AI_API_KEY'))
response = client.models.generate_content(
    model="gemini-2.0-flash", 
    contents=[content, image]
)
print(response.text)

