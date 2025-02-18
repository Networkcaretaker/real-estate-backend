
# TEST 1
## Content:
```python
content = "Give me a Title and Description for this property image" 
```

## Response:
```
Here are a few options for the title and description:

**Option 1 (Focus on Modern Design):**

*   **Title:** Modern Oasis: Sophisticated Living
*   **Description:** A beautifully designed modern home featuring spacious balconies, a serene backyard, and clean architectural lines. Perfect for contemporary living and outdoor enjoyment.

**Option 2 (Focus on Outdoor Space):**

*   **Title:** Balcony Bliss: Entertainer's Dream Home
*   **Description:**  This stunning property boasts multiple balconies ideal for relaxation and entertaining. Enjoy the lush backyard oasis, complete with a covered patio and meticulously landscaped grounds.

**Option 3 (More Concise):**

*   **Title:** Elegant Modern Home with Outdoor Living
*   **Description:**  Features include spacious balconies and a beautifully landscaped backyard, providing a perfect blend of modern style and outdoor enjoyment.
```


# TEST 2
## Content:
```python
content = "Give me a Title and short Description for this property image"
```

## Response:
```
Here are a few options for the Title and Description of the image you sent:

**Option 1 (Focus on architecture):**

*   **Title:** Modern Home with Balconies
*   **Description:** A beautifully designed modern home featuring clean lines, multiple balconies, and a well-maintained backyard.

**Option 2 (Focus on outdoor space):**

*   **Title:** Landscaped Backyard Oasis
*   **Description:** This stunning property boasts a lush green backyard with manicured landscaping and a modern home with multiple outdoor entertaining areas.

**Option 3 (Simple and straightforward):**

*   **Title:** Contemporary Home Exterior
*   **Description:** Exterior view of a contemporary house with balconies and a landscaped lawn.
```

# TEST 3
## Content:
```python
content = 'As a high-end real estate image specialist, analyze this property image and provide a professional, SEO-optimized title and description. Highlights key selling points visible in the image. Uses real estate industry standard terminology, Incorporate relevant keywords naturally, Maintain a professional tone, and Focuses on unique, visible features. Respond in JSON format: "title": "Brief, compelling title (max 60 chars)", "description": "Detailed, SEO-optimized description (max 200 chars)"'
```

## Response:
```json
{
  "title": "Modern Estate with Balconies",
  "description": "Stunning modern home featuring sleek architectural design, multiple balconies with cable railings, and a spacious outdoor living area. Enjoy the private backyard and lush landscaping. A luxury property offering a seamless indoor-outdoor lifestyle."
}
```

# TEST 4
## Content:
```python
content = 'As a high-end real estate image specialist, analyze this property image and provide a professional, SEO-optimized title and description. Highlights key selling points visible in the image. Uses real estate industry standard terminology, Incorporate relevant keywords naturally, Maintain a professional tone, and Focuses on unique, visible features. Provide 3 versions in the responce. Respond in JSON format: "version": "version type (eg. professional, seo-optimized, concise, simple and straightforward)", "title": "Brief, compelling title (max 60 chars)", "description": "Detailed, SEO-optimized description (max 200 chars)"'
```

## Response:
```json
[
  {
    "version": "professional",
    "title": "Stunning Modern Home with Outdoor Living",
    "description": "Discover this exceptional modern home featuring dual balconies, a covered patio, and lush landscaping. Perfect for seamless indoor-outdoor living and entertaining. Experience contemporary design at its finest!"
  },
  {
    "version": "seo-optimized",
    "title": "Modern Home for Sale with Balconies & Patio",
    "description": "Find your dream home! This modern property boasts dual balconies, a covered outdoor patio, and manicured lawn. Ideal for outdoor entertaining & relaxing. Search modern homes, real estate listings, luxury properties."
  },
  {
    "version": "concise",
    "title": "Modern Home: Balconies & Patio",
    "description": "Sleek modern home featuring dual balconies and covered patio. Enjoy seamless indoor-outdoor living. Beautiful lawn and landscaping. A perfect retreat!"       
  }
]
```

# TEST 5
## Content:
```python
property = {
    "title": "Beautiful 3 Bedroom Home",
    "description": "This beautiful 3 bedroom home is located in the heart of the city. It features a spacious living room, modern kitchen, and a large backyard with a pool.",
    "versions": ["professional", "luxury", "concise"],
    "image": "property.jpg"
}

image = PIL.Image.open(property["image"])

content = f'As a high-end real estate image specialist, analyze this property image and provide a professional, SEO-optimized title and description. Highlights key selling points visible in the image. Uses real estate industry standard terminology, Incorporate relevant keywords naturally, Maintain a professional tone, and Focuses on unique, visible features. Provide a responce using the selected tone for each of the following versions {property["versions"]}. For additional reference here is the Property Title:{property["title"]} and Property Description: {property["description"]}. Respond in JSON format: "version": "version type", "image_title": "Brief, compelling title (max 80 chars)", "image_description": "Detailed, SEO-optimized description (max 300 chars)"'
```

## Response:
```json
[
  {
    "version": "professional",
    "image_title": "Modern Residence with Balconies and Outdoor Living",
    "image_description": "Exterior view of a contemporary home featuring multiple balconies with sleek cable railings. This property boasts a manicured lawn and an inviting outdoor patio area, ideal for entertaining. The modern architectural design emphasizes clean lines and ample natural light. Explore outdoor living opportunities with this residence." 
  },
  {
    "version": "luxury",
    "image_title": "Architecturally Stunning Home with Designer Balconies",
    "image_description": "An exquisite residence showcases sophisticated architectural details, including private balconies with designer cable railings offering seamless indoor/outdoor living. The impeccably landscaped grounds create a serene and private retreat. Indulge in unparalleled luxury and refined elegance in this exceptional property, where sophisticated design meets effortless style."
  },
  {
    "version": "concise",
    "image_title": "Modern Home: Balconies & Outdoor Patio",
    "image_description": "Contemporary home with multiple balconies, cable railings, and landscaped yard. Features include an outdoor patio for entertaining. Modern architecture emphasizes clean lines."
  }
]
```

# TEST 6
## Content:
```python
property = {
    "title": "Beautiful 3 Bedroom Home",
    "description": "This beautiful 3 bedroom home is located in the heart of the city. It features a spacious living room, modern kitchen, and a large backyard with a pool.",
    "versions": ["professional", "funny", "call to action"],
    "image": "property.jpg"
}

image = PIL.Image.open(property["image"])

content = f'As a high-end real estate image specialist, analyze this property image and provide a professional, SEO-optimized title and description. Highlights key selling points visible in the image. Uses real estate industry standard terminology, Incorporate relevant keywords naturally, Maintain a professional tone, and Focuses on unique, visible features. Provide a responce using the selected tone for each of the following versions {property["versions"]}. For additional reference here is the Property Title:{property["title"]} and Property Description: {property["description"]}. Respond in JSON format: "version": "version type", "image_title": "Brief, compelling title (max 80 chars)", "image_description": "Detailed, SEO-optimized description (max 300 chars)"'
```

## Response:
```json
[
  {
    "version": "professional",
    "image_title": "Contemporary Home with Balconies & Outdoor Living",
    "image_description": "Stunning contemporary home featuring multiple balconies with sleek cable railings, providing seamless indoor/outdoor living. Expansive windows flood the interior with natural light. Enjoy the meticulously landscaped grounds and inviting outdoor patio, perfect for entertaining. This architectural gem offers modern elegance and serene privacy. Ideal for discerning homebuyers seeking a sophisticated lifestyle."
  },
  {
    "version": "funny",
    "image_title": "Balconies So Nice, They Built it Twice!",
    "image_description": "Prepare for balcony overload! This modern masterpiece boasts not one, but TWO balconies – perfect for practicing your Shakespearean soliloquies or just judging the neighbors. Lush landscaping included to hide from said neighbors when necessary. Warning: May induce excessive outdoor lounging and spontaneous cocktail parties. Inquire within before you fall off this property!"
  },
  {
    "version": "call to action",
    "image_title": "Your Dream Home Awaits: Schedule a Showing Today!",
    "image_description": "Discover luxurious living in this beautifully designed home with multiple balconies and an inviting outdoor patio. Imagine yourself relaxing in this serene environment. Don't miss the opportunity to own this exquisite property! Contact us now to schedule a private showing and experience the unparalleled elegance and comfort firsthand. Make your dream a reality today."
  }
]
```

# PROPERTY TEST 1
## Content:
```python
summary = "This beautiful 3 bedroom home is located in the heart of the city. It features a spacious living room, modern kitchen, and a large backyard with a pool."
versions = ["professional", "funny", "call to action"]
feature_image = "property.jpg"
propertyType = "Villa"
propertyLocation = "Santa Ponsa, Calvia"
price = 3500000
bedrooms = 5
bathrooms =4
plotArea = "800 m2"
propertyArea = "400 m2"
interior_features = None
exterior_features = None

image = PIL.Image.open(feature_image)

propertyData = {
    "Type": propertyType,
    "Location": propertyLocation,
    "price": price,
    "bedrooms": bedrooms,
    "bathrooms": bathrooms,
    "plotArea": plotArea,
    "propertyArea": propertyArea
}

content = f'''As a high-end real estate specialist, analyze this {propertyType} in {propertyLocation} and provide a professional, SEO-optimized title, description and excerpt.

Use the Image, Property Summary and the Property Data provided.
Highlights key selling points. Uses real estate industry standard terminology.
Incorporate relevant keywords naturally.
Maintain a professional tone.
Provide a responce using the selected tone for each of the requested Versions .

Property Summary: {summary}
Property Data: {propertyData}
Versions: {versions}

Respond in JSON format with the following infomation for each version:
"version": "version type",
"title": "Brief, compelling title (max 80 chars)",
"description": "Detailed description of the property (max 1200 chars)",
"excerpt": "SEO optimized summary of the property, focus on key selling points (max 300 chars)"

Property Description Notes
The opening section should focus on the location.
The next section should focus on the property.
The final section should focus on features and key selling points.
'''

client = genai.Client(api_key=os.getenv('GOOGLE_AI_API_KEY'))
response = client.models.generate_content(
    model="gemini-2.0-flash", 
    contents=[content, image]
)
print(response.text)
```

## Response:
```json
{
  "versions": [
    {
      "version": "professional",
      "title": "Luxury Villa in Santa Ponsa | Calvia Property For Sale",
      "description": "Nestled in the prestigious locale of Santa Ponsa, Calvia, this exceptional villa offers unparalleled luxury and sophisticated living. Boasting 5 bedrooms and 4 bathrooms, this meticulously designed residence spans 400 m2 on a generous 800 m2 plot. \n\nStep inside to discover spacious and light-filled interiors, showcasing modern architectural design and premium finishes. The expansive living areas are perfect for both grand entertaining and intimate family gatherings. The gourmet kitchen is equipped with state-of-the-art appliances and custom cabinetry.\n\nOutside, the meticulously landscaped grounds feature a private swimming pool, offering a serene oasis for relaxation. Multiple terraces provide ample space for al fresco dining and enjoying the stunning Mediterranean climate. This Santa Ponsa villa represents a rare opportunity to own a piece of paradise in one of Mallorca's most sought-after locations. Key features include: expansive plot, private pool, multiple terraces and prime location.",
      "excerpt": "Luxury 5-bedroom, 4-bathroom villa for sale in Santa Ponsa, Calvia. Features a spacious 400 m2 living area, 800 m2 plot, private pool, and multiple terraces. Prime location in Mallorca. A rare real estate opportunity."
    },
    {
      "version": "funny",
      "title": "Santa Ponsa Villa: Ditch the Day Job, Embrace Island Life!",
      "description": "Escape the ordinary and dive headfirst into the good life with this fabulous villa in Santa Ponsa, Calvia! This isn't just a house; it's your ticket to endless sunshine, sangria-soaked sunsets, and bragging rights galore. With 5 bedrooms and 4 bathrooms, there's plenty of room for the whole family. \n\nSpread out in 400 m2 of pure, unadulterated luxury, or take the party outside to your sprawling 800 m2 plot. The kitchen is so fancy, it practically cooks for you (okay, maybe not, but it's close!). \n\nAnd let's talk about the pool – it's the perfect place to perfect your tan and sip on something fruity. Plus, with all those terraces, you'll have more outdoor space than you know what to do with (think: yoga, cocktails, or just plain chilling). This Santa Ponsa gem is calling your name – answer it!",
      "excerpt": "Santa Ponsa villa for sale! 5 beds, 4 baths, a pool, and enough terrace space to host a small country. Ditch the 9-to-5 and live the island dream. Warning: May cause extreme happiness."
    },
    {
      "version": "call to action",
      "title": "Santa Ponsa Villa For Sale | Enquire Today!",
      "description": "Discover your dream home in Santa Ponsa, Calvia! This stunning 5-bedroom, 4-bathroom villa offers the ultimate in luxury and Mediterranean living. Situated on an 800 m2 plot with 400 m2 of living space, this property provides ample room for relaxation and entertainment.\n\nImagine yourself lounging by your private pool, enjoying al fresco dining on one of the many terraces, or hosting unforgettable gatherings in the spacious living areas. This villa is meticulously designed with high-end finishes and modern amenities.\n\nDon't miss this incredible opportunity to own a piece of paradise in Santa Ponsa. Contact us today to schedule a private viewing and experience the luxury for yourself. Your dream home awaits! Key features include: expansive plot, private pool, multiple terraces and prime location.",
      "excerpt": "Luxury villa for sale in Santa Ponsa, Calvia. 5 bedrooms, 4 bathrooms, private pool, and multiple terraces. Enquire now to arrange a viewing and make this dream"
    }
  ]
}
```