from flask import Flask
from config.firebase import db
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

@app.route('/')
def hello():
    return {'message': 'Real Estate API'}

@app.route('/test-firebase')
def test_firebase():
    try:
        # Try to access the 'properties' collection
        properties_ref = db.collection('properties')
        # Get the first document (limit 1)
        docs = properties_ref.limit(1).stream()
        
        # Convert to list to test if we can fetch data
        properties = [doc.to_dict() for doc in docs]
        
        return {
            'status': 'success',
            'message': 'Firebase connection successful',
            'data': properties,
            'firebase_project_id': os.getenv('FIREBASE_PROJECT_ID')
        }
    except Exception as e:
        return {
            'status': 'error',
            'message': str(e)
        }

if __name__ == '__main__':
    app.run(debug=True)