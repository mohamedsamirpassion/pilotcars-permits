# Configuration Variables Required for Load Planning Feature
# Add these to your Flask app's configuration

import os

class LoadPlanningConfig:
    """
    Configuration settings needed for the Load Planning feature.
    Add these to your existing Flask configuration class.
    """
    
    # REQUIRED: Google Maps API Configuration
    # Get your API key from: https://console.cloud.google.com/apis/credentials
    GOOGLE_MAPS_API_KEY = os.environ.get('GOOGLE_MAPS_API_KEY') or 'your-google-maps-api-key-here'
    
    # Ensure you enable these APIs in Google Cloud Console:
    # - Maps JavaScript API
    # - Places API  
    # - Directions API
    # - Geocoding API
    
    # REQUIRED: Email Configuration (for feedback reports)
    MAIL_SERVER = os.environ.get('MAIL_SERVER') or 'smtp.gmail.com'
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 587)
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME') or 'your-email@gmail.com'
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD') or 'your-app-password'
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER') or 'noreply@yourdomain.com'
    
    # REQUIRED: Admin Email (receives feedback reports)
    ADMIN_EMAIL = os.environ.get('ADMIN_EMAIL') or 'admin@yourdomain.com'
    
    # OPTIONAL: CSRF Configuration (recommended for security)
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key-change-in-production'
    WTF_CSRF_TIME_LIMIT = None  # No expiration for better UX
    
    # OPTIONAL: Content Security Policy (if you use CSP headers)
    # Add these domains to your CSP if you have one:
    CSP_ADDITIONAL_DOMAINS = [
        'https://maps.googleapis.com',      # Google Maps API
        'https://cdn.jsdelivr.net',        # Bootstrap/FontAwesome CDN  
        'https://cdnjs.cloudflare.com',     # Additional CDN resources
        'https://fonts.googleapis.com',     # Google Fonts
        'https://fonts.gstatic.com'         # Google Fonts
    ]

# Example Flask App Integration:
"""
from flask import Flask
from flask_mail import Mail
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)

# Add Load Planning config to your existing config
app.config.from_object(LoadPlanningConfig)

# Initialize extensions (if not already initialized)
mail = Mail(app)
csrf = CSRFProtect(app)

# Register the load planning blueprint
from routes.load_planning_routes import bp as load_planning_bp
app.register_blueprint(load_planning_bp)
"""

# Environment Variables Template (.env file):
"""
# Google Maps API
GOOGLE_MAPS_API_KEY=your-google-maps-api-key-here

# Email Configuration
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
MAIL_DEFAULT_SENDER=noreply@yourdomain.com
ADMIN_EMAIL=admin@yourdomain.com

# Security
SECRET_KEY=your-secret-key-change-in-production
"""

# Production Notes:
"""
1. Never commit API keys to version control
2. Use environment variables for all sensitive data
3. Enable billing on Google Cloud for production use
4. Consider rate limiting for the calculation endpoints
5. Monitor Google Maps API usage to avoid unexpected charges
6. Use app-specific passwords for Gmail SMTP
"""
