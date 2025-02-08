import os
import firebase_admin
from firebase_admin import credentials
from dotenv import load_dotenv
from app.services.batch_processor import BatchPropertyProcessor

def initialize_firebase():
    """Initialize Firebase with credentials from environment variables"""
    try:
        # Load environment variables
        load_dotenv()
        
        # Get the path to the service account file
        cred_path = os.getenv('FIREBASE_SERVICE_ACCOUNT')
        if not cred_path:
            raise ValueError("FIREBASE_SERVICE_ACCOUNT environment variable not set")
            
        # Initialize Firebase
        cred = credentials.Certificate(cred_path)
        firebase_admin.initialize_app(cred, {
            'storageBucket': os.getenv('FIREBASE_STORAGE_BUCKET')
        })
        print("Firebase initialized successfully")
        
    except Exception as e:
        print(f"Error initializing Firebase: {str(e)}")
        raise

def main():
    try:
        # Initialize Firebase first
        initialize_firebase()
        
        # Initialize the processor
        processor = BatchPropertyProcessor()
        
        # CSV file path
        csv_path = 'properties.csv'  # Update this path to your CSV file location
        
        # Validate CSV format
        print("Validating CSV format...")
        is_valid, missing_columns = processor.validate_csv_format(csv_path)
        
        if not is_valid:
            print("\nError: CSV file is missing required columns:")
            for column in missing_columns:
                print(f"- {column}")
            return
        
        print("\nStarting batch processing...")
        
        # Process the CSV file
        results = processor.process_csv(csv_path)
        
        # Print results summary
        print("\nCSV Processing Results:")
        print(f"Total properties: {results['total']}")
        print(f"Successfully processed: {results['successful']}")
        print(f"Failed to process: {results['failed']}")
        
        # Print errors if any
        if results['errors']:
            print("\nErrors encountered:")
            for error in results['errors']:
                print(f"Property {error['property_id']}: {error['error']}")
                
    except Exception as e:
        print(f"\nError: {str(e)}")
        raise

if __name__ == "__main__":
    main()