from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Firebase configuration
FIREBASE_CONFIG = {
    'apiKey': os.getenv('FIREBASE_API_KEY'),
    'authDomain': os.getenv('FIREBASE_AUTH_DOMAIN'),
    'projectId': os.getenv('FIREBASE_PROJECT_ID')
}

# Flask configuration
FLASK_CONFIG = {
    'DEBUG': os.getenv('FLASK_ENV') == 'development',
    'SECRET_KEY': os.getenv('FLASK_SECRET_KEY', 'dev-key-for-development')
}