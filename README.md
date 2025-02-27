# Real Estate Platform Backend

## Description
A Flask-based backend service that serves as a bridge between a CRM system and Firebase for a real estate platform. This service handles property data synchronization, processes webhook events, and maintains a reliable data pipeline between systems.

## Key Features
- Webhook integration with CRM system
- Firebase data storage and management
- Secure authentication and data validation
- Real-time property data synchronization
- Modular and scalable architecture

## Tech Stack
- Python/Flask
- Firebase Admin SDK
- Structured Logging
- RESTful APIs

## Getting Started

### Prerequisites
- Python 3.8+
- Firebase account and credentials
- CRM webhook configuration

### Installation
1. Clone the repository
2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate
```
3. Install dependencies:
```bash
pip install -r requirements.txt
```
4. Configure environment variables (copy .env.example to .env and fill in values)
5. Run the application:
```bash
python run.py
```

## Project Structure
The backend follows a modular design pattern, separating concerns into routes, services, and utilities for maintainable and testable code.

## ToDo
Sort property features section 
Create function to upload data to firebase from csv
Improve CRM connection with RestAPI