from google import genai
import os
import PIL

# Example Property Inormation for image AI Assistant
property = {
    "title": "Beautiful 3 Bedroom Home",
    "description": "This beautiful 3 bedroom home is located in the heart of the city. It features a spacious living room, modern kitchen, and a large backyard with a pool.",
    "versions": ["professional", "funny", "call to action"],
    "image": "property.jpg"
}

# Example Property Inormation for property AI Assistant
title = "Land in Santa Ponsa"
#summary = "This beautiful 3 bedroom home is located in the heart of the city. It features a spacious living room, modern kitchen, and a large backyard with a pool."
summary = "large plot of land in developed area with a full building license"
versions = ["concise", "professional", "funny"]
feature_image = "land.jpg"
propertyType = "Land"
propertyLocation = "Santa Ponsa, Calvia"
price = 200000
bedrooms = 6
bathrooms =4
plotArea = "1200 m2"
propertyArea = "400 m2"
interior_features = None
exterior_features = None

image = PIL.Image.open(feature_image)

propertyData = {
    "Type": propertyType,
    "Location": propertyLocation,
    "Price": price,
    "Plot Area": plotArea,
    "Build Area": propertyArea
}

content = f'''As a high-end real estate specialist, analyze this {propertyType} located in {propertyLocation} and using the image and the information provided, create an engaging title, description and excerpt for this real estate. Highlight key selling points using real estate industry standard terminology, incorporate relevant keywords naturally and maintain a professional tone.

Property Category: {propertyType}
Primary Location: {propertyLocation}
Property Summary: {summary}
Property Details: {propertyData}
Versions Requiered: {versions}
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
   - Highlight one standout feature
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

Respond with a JSON array of objects containing: "version": str, "title": str, "description": str, "excerpt": str
'''

# content = f'As a high-end real estate image specialist, analyze this property image and provide a professional, SEO-optimized title and description. Highlights key selling points visible in the image. Uses real estate industry standard terminology, Incorporate relevant keywords naturally, Maintain a professional tone, and Focuses on unique, visible features. Provide a responce using the selected tone for each of the following versions {property["versions"]}. For additional reference here is the Property Title:{property["title"]} and Property Description: {property["description"]}. Respond in JSON format: "version": "version type", "image_title": "Brief, compelling title (max 80 chars)", "image_description": "Detailed, SEO-optimized description (max 300 chars)"'

client = genai.Client(api_key=os.getenv('GOOGLE_AI_API_KEY'))
response = client.models.generate_content(
    model="gemini-2.0-flash", 
    contents=[content, image]
)
print(response.text)
