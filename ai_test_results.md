
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