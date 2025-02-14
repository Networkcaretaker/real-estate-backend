import asyncio
from app.services.ai_service import AIService
import os
import firebase_admin
from firebase_admin import credentials

async def run_test():
    # Initialize Firebase
    cred = credentials.Certificate('real-estate-firebase-serviceAccount.json')
    firebase_admin.initialize_app(cred, {
        'storageBucket': os.getenv('FIREBASE_STORAGE_BUCKET')
    })

    # Test with real property and image from database
    property_id = "CP000208"  # Your actual property ID
    image_id = "2291dd45-d3af-4894-9a8c-a296f6dee432"  # Your actual image ID
    versions = ["professional", "funny", "call to action"]

    # Run AI analysis
    ai_service = AIService()
    response = await ai_service.analyze_property_image(property_id, image_id, versions)
    print("AI Response:", response)

if __name__ == "__main__":
    asyncio.run(run_test())