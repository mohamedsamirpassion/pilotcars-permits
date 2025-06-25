from dotenv import load_dotenv
load_dotenv()
from flask import Flask, render_template, request, jsonify, session, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, date, timedelta
import os
import json
import requests
import math
import re
from geopy.geocoders import Nominatim

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


# Add custom Jinja filters
@app.template_filter('from_json')
def from_json(value):
    """Parse JSON string to Python object"""
    if value:
        try:
            return json.loads(value)
        except:
            return []
    return []

@app.template_global()
def moment():
    """Make datetime available in templates"""
    return datetime

# Helper function for reverse geocoding
def get_city_state_from_coordinates(latitude, longitude):
    """Get city and state from latitude and longitude coordinates in English"""
    try:
        # Use direct API call with SSL verification disabled to avoid macOS SSL issues
        import urllib3
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        
        # First try with English language preference
        url = f"https://nominatim.openstreetmap.org/reverse?lat={latitude}&lon={longitude}&format=json&addressdetails=1&accept-language=en"
        headers = {
            'User-Agent': 'mypevo-pilot-car-app/1.0 (contact@mypevo.com)',
            'Accept-Language': 'en-US,en;q=0.9'
        }
        
        response = requests.get(url, headers=headers, verify=False, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            
            if 'address' in data:
                address_parts = data['address']
                
                # Try multiple possible keys for city
                city = (address_parts.get('city') or 
                       address_parts.get('town') or 
                       address_parts.get('village') or 
                       address_parts.get('hamlet') or 
                       address_parts.get('county') or
                       address_parts.get('municipality') or
                       address_parts.get('suburb'))
                
                # Try multiple possible keys for state
                state = (address_parts.get('state') or 
                        address_parts.get('state_district') or 
                        address_parts.get('region') or
                        address_parts.get('province') or
                        address_parts.get('country'))  # Use country as fallback for state
                
                # Handle case where we have city but no state/region info
                if city and not state:
                    # Try to get country as state fallback
                    state = address_parts.get('country', 'Unknown Region')
                
                # If we got non-English results, try to get English names
                if city:  # Only require city, state is optional
                    # Check if the result contains non-Latin characters (likely non-English)
                    import re
                    if re.search(r'[^\x00-\x7F]', city) or (state and re.search(r'[^\x00-\x7F]', state)):
                        # Try to get English name from alternative sources
                        english_city, english_state = get_english_place_names(latitude, longitude, city, state)
                        if english_city:
                            city = english_city
                        if english_state:
                            state = english_state
                
                return city, state
                
    except Exception as e:
        print(f"Geocoding error: {e}")
    
    return None, None

def get_english_place_names(latitude, longitude, original_city, original_state):
    """Try to get English names for places using additional methods"""
    try:
        import urllib3
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        
        # Try different approaches to get English names
        
        # Method 1: Try with different zoom levels to get broader region names
        url = f"https://nominatim.openstreetmap.org/reverse?lat={latitude}&lon={longitude}&format=json&zoom=10&accept-language=en"
        headers = {
            'User-Agent': 'mypevo-pilot-car-app/1.0 (contact@mypevo.com)',
            'Accept-Language': 'en-US,en;q=0.9'
        }
        
        response = requests.get(url, headers=headers, verify=False, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if 'address' in data:
                address_parts = data['address']
                
                city = (address_parts.get('city') or 
                       address_parts.get('town') or 
                       address_parts.get('village') or 
                       address_parts.get('hamlet') or 
                       address_parts.get('county') or
                       address_parts.get('municipality') or
                       address_parts.get('suburb'))
                
                state = (address_parts.get('state') or 
                        address_parts.get('state_district') or 
                        address_parts.get('region') or
                        address_parts.get('province'))
                
                # Check if we got English results this time
                import re
                if city and not re.search(r'[^\x00-\x7F]', city):
                    if state and not re.search(r'[^\x00-\x7F]', state):
                        return city, state
        
        # Method 2: Try manual mapping for common non-English place names
        english_mappings = {
            # Arabic locations
            'مدينة نصر': 'Nasr City',
            'القاهرة': 'Cairo',
            'الجيزة': 'Giza',
            'الإسكندرية': 'Alexandria',
            'شبرا الخيمة': 'Shubra El Kheima',
            'المنصورة': 'Mansoura',
            'أسوان': 'Aswan',
            'الأقصر': 'Luxor',
            'الرياض': 'Riyadh',
            'جدة': 'Jeddah',
            'الدمام': 'Dammam',
            
            # Spanish locations
            'Ciudad de México': 'Mexico City',
            'Ciudad Autónoma de Buenos Aires': 'Buenos Aires',
            
            # French locations
            'Île-de-France': 'Île-de-France',
            
            # Chinese locations  
            '北京': 'Beijing',
            '上海': 'Shanghai',
            '广州': 'Guangzhou',
            '深圳': 'Shenzhen',
            '杭州': 'Hangzhou',
            
            # Japanese locations
            '東京': 'Tokyo',
            '大阪': 'Osaka',
            '京都': 'Kyoto',
            '横浜': 'Yokohama',
            
            # Russian locations
            'Москва': 'Moscow',
            'Санкт-Петербург': 'Saint Petersburg',
            
            # Korean locations
            '서울': 'Seoul',
            '부산': 'Busan',
            
            # Add more mappings as needed
        }
        
        english_city = english_mappings.get(original_city)
        english_state = english_mappings.get(original_state)
        
        # Method 3: If we still have non-English names, try transliteration
        if not english_city and original_city:
            # For places not in our mapping, use a fallback strategy
            import re
            if re.search(r'[^\x00-\x7F]', original_city):
                # Keep the original non-English name but add a note
                # This preserves the data while indicating it needs manual review
                english_city = f"{original_city}"
        
        if not english_state and original_state:
            import re
            if re.search(r'[^\x00-\x7F]', original_state):
                english_state = f"{original_state}"
        
        return english_city, english_state
        
    except Exception as e:
        print(f"English name lookup error: {e}")
        return None, None

# Database Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone_number = db.Column(db.String(20), nullable=True)  # Will be required for new registrations
    dot_number = db.Column(db.String(20), nullable=True)    # Only required for trucking companies
    password_hash = db.Column(db.String(128))
    is_admin = db.Column(db.Boolean, default=False)
    user_type = db.Column(db.String(20), default='trucking_company')  # 'trucking_company' or 'vendor'
    is_approved = db.Column(db.Boolean, default=False)  # For trucking companies
    is_suspended = db.Column(db.Boolean, default=False)  # For suspension feature
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    routes = db.relationship('SavedRoute', backref='user', lazy=True)
    quotes = db.relationship('Quote', backref='user', lazy=True)
    vendor_locations = db.relationship('VendorLocation', backref='user', lazy=True)
    pilot_car_orders = db.relationship('PilotCarOrder', backref='user', lazy=True)

class SavedRoute(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    route_name = db.Column(db.String(100), nullable=False)
    origin = db.Column(db.String(200), nullable=False)
    destination = db.Column(db.String(200), nullable=False)
    road_type = db.Column(db.String(50), nullable=False)
    length = db.Column(db.Float)
    width = db.Column(db.Float)
    height = db.Column(db.Float)
    weight = db.Column(db.Float)
    front_overhang = db.Column(db.Float)
    rear_overhang = db.Column(db.Float)
    custom_route = db.Column(db.Text)
    route_results = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Quote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    pickup_date = db.Column(db.Date, nullable=False)
    pickup_time = db.Column(db.String(10), nullable=False)
    pickup_location = db.Column(db.String(200), nullable=False)
    pickup_state = db.Column(db.String(50), nullable=False)
    delivery_location = db.Column(db.String(200), nullable=False)
    delivery_state = db.Column(db.String(50), nullable=False)
    car_types = db.Column(db.Text, nullable=False)  # JSON array
    is_superload = db.Column(db.Boolean, default=False)
    distance_miles = db.Column(db.Float)
    rate_type = db.Column(db.String(20))  # 'standard' or 'premium'
    region = db.Column(db.String(50))
    total_cost = db.Column(db.Float)
    quote_breakdown = db.Column(db.Text)  # JSON object
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class VendorLocation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)  # Nullable for guest vendors
    company_name = db.Column(db.String(100), nullable=False)  # For guest vendors
    contact_name = db.Column(db.String(100), nullable=True)
    email = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    location_city = db.Column(db.String(100), nullable=False)
    location_state = db.Column(db.String(50), nullable=False)
    latitude = db.Column(db.Float, nullable=True)
    longitude = db.Column(db.Float, nullable=True)
    coverage_radius = db.Column(db.Integer, default=100)  # Miles
    services_provided = db.Column(db.Text, nullable=False)  # JSON array
    notes = db.Column(db.Text, nullable=True)
    is_registered_vendor = db.Column(db.Boolean, default=False)
    expires_at = db.Column(db.DateTime, nullable=False)  # 48 hours from creation
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class PilotCarOrder(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)  # Nullable for guest orders
    
    # Company Information
    company_name = db.Column(db.String(100), nullable=False)
    dot_number = db.Column(db.String(20), nullable=True)
    
    # Pickup & Delivery Locations
    pickup_address = db.Column(db.Text, nullable=False)
    delivery_address = db.Column(db.Text, nullable=False)
    
    # Pickup & Service Details
    pickup_date = db.Column(db.Date, nullable=False)
    pickup_time = db.Column(db.String(10), nullable=False)
    pilot_car_positions = db.Column(db.Text, nullable=False)  # JSON array
    
    # Driver Information
    driver_name = db.Column(db.String(100), nullable=False)
    driver_phone = db.Column(db.String(20), nullable=False)
    
    # Load Information
    length = db.Column(db.String(20), nullable=False)
    width = db.Column(db.String(20), nullable=False)
    height = db.Column(db.String(20), nullable=False)
    weight = db.Column(db.String(20), nullable=False)
    truck_number = db.Column(db.String(50), nullable=True)
    load_number = db.Column(db.String(50), nullable=True)
    load_description = db.Column(db.Text, nullable=True)
    additional_notes = db.Column(db.Text, nullable=True)
    
    # Contact Information
    contact_name = db.Column(db.String(100), nullable=False)
    preferred_contact = db.Column(db.String(20), nullable=False)
    phone_number = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    
    # Payment Information
    po_number = db.Column(db.String(50), nullable=True)
    payment_method = db.Column(db.String(20), nullable=False)  # 'credit_card'
    terms_agreed = db.Column(db.Boolean, nullable=False, default=False)
    
    # Order Management
    status = db.Column(db.String(20), default='pending')  # pending, confirmed, in_progress, completed, cancelled
    admin_notes = db.Column(db.Text, nullable=True)
    assigned_vendor_id = db.Column(db.Integer, nullable=True)
    estimated_cost = db.Column(db.Float, nullable=True)
    final_cost = db.Column(db.Float, nullable=True)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

def load_state_regulations():
    """Load state regulations from the JavaScript file"""
    try:
        with open('static/js/state_regulations.js', 'r') as f:
            content = f.read()
            
            # Find the array start after the const declaration
            const_start = content.find('const stateRegulations = [')
            if const_start == -1:
                const_start = content.find('stateRegulations = [')
            if const_start == -1:
                start = content.find('[')
            else:
                start = content.find('[', const_start)
            
            end = content.rfind('];')
            if end == -1:
                end = content.rfind(']') + 1
            else:
                end += 1
                
            json_data = content[start:end]
            
            # Clean up JavaScript comments
            lines = json_data.split('\n')
            cleaned_lines = []
            for line in lines:
                # Remove JavaScript comments but keep the line structure
                if '//' in line and not line.strip().startswith('"'):
                    # Only remove comments that are not inside strings
                    comment_pos = line.find('//')
                    # Simple check - if // is not inside quotes
                    quote_count = line[:comment_pos].count('"') - line[:comment_pos].count('\\"')
                    if quote_count % 2 == 0:  # Even number of quotes means // is outside strings
                        line = line[:comment_pos].rstrip()
                
                if line.strip():
                    cleaned_lines.append(line)
            
            cleaned_json = '\n'.join(cleaned_lines)
            regulations_array = json.loads(cleaned_json)
            
            # Convert array to dictionary organized by state
            regulations_dict = {}
            for reg in regulations_array:
                state = reg.get('state', '').upper()
                # Use state abbreviation for consistency
                state_abbrev = get_state_abbreviation(state)
                if state_abbrev not in regulations_dict:
                    regulations_dict[state_abbrev] = []
                regulations_dict[state_abbrev].append(reg)
            
            return regulations_dict
    except Exception as e:
        print(f"Error loading state regulations: {e}")
        import traceback
        traceback.print_exc()
        return {}

def get_state_abbreviation(state_name):
    """Convert state name to abbreviation"""
    state_mapping = {
        'ALABAMA': 'AL', 'ALASKA': 'AK', 'ARIZONA': 'AZ', 'ARKANSAS': 'AR', 'CALIFORNIA': 'CA',
        'COLORADO': 'CO', 'CONNECTICUT': 'CT', 'DELAWARE': 'DE', 'FLORIDA': 'FL', 'GEORGIA': 'GA',
        'HAWAII': 'HI', 'IDAHO': 'ID', 'ILLINOIS': 'IL', 'INDIANA': 'IN', 'IOWA': 'IA',
        'KANSAS': 'KS', 'KENTUCKY': 'KY', 'LOUISIANA': 'LA', 'MAINE': 'ME', 'MARYLAND': 'MD',
        'MASSACHUSETTS': 'MA', 'MICHIGAN': 'MI', 'MINNESOTA': 'MN', 'MISSISSIPPI': 'MS', 'MISSOURI': 'MO',
        'MONTANA': 'MT', 'NEBRASKA': 'NE', 'NEVADA': 'NV', 'NEW HAMPSHIRE': 'NH', 'NEW JERSEY': 'NJ',
        'NEW MEXICO': 'NM', 'NEW YORK': 'NY', 'NORTH CAROLINA': 'NC', 'NORTH DAKOTA': 'ND', 'OHIO': 'OH',
        'OKLAHOMA': 'OK', 'OREGON': 'OR', 'PENNSYLVANIA': 'PA', 'RHODE ISLAND': 'RI', 'SOUTH CAROLINA': 'SC',
        'SOUTH DAKOTA': 'SD', 'TENNESSEE': 'TN', 'TEXAS': 'TX', 'UTAH': 'UT', 'VERMONT': 'VT',
        'VIRGINIA': 'VA', 'WASHINGTON': 'WA', 'WEST VIRGINIA': 'WV', 'WISCONSIN': 'WI', 'WYOMING': 'WY'
    }
    return state_mapping.get(state_name.upper(), state_name)

def calculate_escort_requirements(load_data, states):
    """Calculate escort requirements based on load data and state regulations"""
    regulations = load_state_regulations()
    results = []
    
    for state in states:
        state_code = state.upper()
        if state_code in regulations:
            state_regs = regulations[state_code]
            escort_req = determine_escort_type(load_data, state_regs)
            
            # Get notes from the first matching regulation
            notes = ""
            for reg in state_regs:
                if reg.get('road_type') == load_data.get('road_type', 'Interstate') and reg.get('notes'):
                    notes = reg.get('notes')
                    break
            
            results.append({
                'state': state,
                'road_type': load_data.get('road_type', 'Interstate'),
                'escort_requirements': escort_req['requirements'],
                'notes': notes
            })
        else:
            results.append({
                'state': state,
                'road_type': load_data.get('road_type', 'Interstate'),
                'escort_requirements': 'No data available',
                'notes': 'State regulations not found'
            })
    
    return results

def parse_dimension(dimension_str):
    """Parse dimension string like '14'3\"' to decimal feet"""
    if not dimension_str:
        return 0
    
    # Remove quotes and split by apostrophe
    dimension_str = dimension_str.replace('"', '').replace("'", "'")
    
    if "'" in dimension_str:
        parts = dimension_str.split("'")
        feet = float(parts[0]) if parts[0] else 0
        inches = float(parts[1]) if len(parts) > 1 and parts[1] else 0
        return feet + (inches / 12)
    else:
        return float(dimension_str)

def determine_escort_type(load_data, state_regs):
    """Determine the type of escort required based on load dimensions and state regulations"""
    requirements = []
    
    width = float(load_data.get('width', 0))
    height = float(load_data.get('height', 0))
    length = float(load_data.get('length', 0))
    weight = float(load_data.get('weight', 0))
    road_type = load_data.get('road_type', 'Interstate')
    
    # Find the best matching regulation for this road type and dimensions
    best_match = None
    
    for reg in state_regs:
        if reg.get('road_type') != road_type:
            continue
            
        # Check width requirements
        if reg.get('width_min') or reg.get('width_max'):
            width_min = parse_dimension(reg.get('width_min', '0'))
            width_max = parse_dimension(reg.get('width_max', '999')) if reg.get('width_max') else 999
            
            if width_min <= width <= width_max:
                if reg.get('width_escorts'):
                    requirements.append(reg.get('width_escorts'))
        
        # Check height requirements
        if reg.get('height_min') or reg.get('height_max'):
            height_min = parse_dimension(reg.get('height_min', '0'))
            height_max = parse_dimension(reg.get('height_max', '999')) if reg.get('height_max') else 999
            
            if height_min <= height <= height_max:
                if reg.get('height_escorts'):
                    requirements.append(reg.get('height_escorts'))
        
        # Check length requirements
        if reg.get('length_min') or reg.get('length_max'):
            length_min = parse_dimension(reg.get('length_min', '0'))
            length_max = parse_dimension(reg.get('length_max', '999')) if reg.get('length_max') else 999
            
            if length_min <= length <= length_max:
                if reg.get('length_escorts'):
                    requirements.append(reg.get('length_escorts'))
        
        # Check weight requirements
        if reg.get('weight_min') or reg.get('weight_max'):
            weight_min = float(reg.get('weight_min', 0))
            weight_max = float(reg.get('weight_max', 999999999)) if reg.get('weight_max') else 999999999
            
            if weight_min <= weight <= weight_max:
                if reg.get('weight_escorts'):
                    requirements.append(reg.get('weight_escorts'))
    
    # Remove duplicates and return
    unique_requirements = list(set(filter(None, requirements)))
    return {
        'requirements': ', '.join(unique_requirements) if unique_requirements else 'None Required'
    }

# Quote calculation functions
def get_region_by_state(state_abbrev):
    """Get region for a given state abbreviation"""
    regions = {
        'Northeast': ['ME', 'NH', 'VT', 'MA', 'RI', 'CT', 'NY', 'NJ', 'PA', 'DE', 'DC', 'MD'],
        'Midwest': ['OH', 'MI', 'IL', 'IN', 'IA', 'MO', 'MN', 'WI', 'ND', 'SD', 'NE'],
        'Southeast': ['AR', 'LA', 'MS', 'AL', 'FL', 'GA', 'TN', 'SC', 'NC', 'VA', 'WV', 'KY'],
        'Southwest': ['TX', 'OK', 'KS', 'CO', 'UT', 'NM', 'NV', 'AZ'],
        'Pacific Northwest': ['CA', 'OR', 'WA', 'ID', 'MT', 'WY']
    }
    
    for region, states in regions.items():
        if state_abbrev.upper() in states:
            return region
    return 'Southeast'  # Default region

def get_regional_rates():
    """Get pricing rates by region and car type"""
    return {
        'Northeast': {
            'Lead / Chase': {'standard_mile': 1.90, 'premium_mile': 2.00, 'standard_day': 550, 'premium_day': 600},
            'High Pole': {'standard_mile': 2.15, 'premium_mile': 2.25, 'standard_day': 650, 'premium_day': 750},
            'Steerman': {'standard_mile': 2.15, 'premium_mile': 2.50, 'standard_day': 650, 'premium_day': 750},
            'Route Survey': {'standard_mile': 2.25, 'premium_mile': 2.50, 'standard_day': 800, 'premium_day': 800}
        },
        'Midwest': {
            'Lead / Chase': {'standard_mile': 1.90, 'premium_mile': 2.00, 'standard_day': 550, 'premium_day': 600},
            'High Pole': {'standard_mile': 2.10, 'premium_mile': 2.25, 'standard_day': 650, 'premium_day': 750},
            'Steerman': {'standard_mile': 2.10, 'premium_mile': 2.50, 'standard_day': 650, 'premium_day': 750},
            'Route Survey': {'standard_mile': 2.25, 'premium_mile': 2.50, 'standard_day': 800, 'premium_day': 800}
        },
        'Southeast': {
            'Lead / Chase': {'standard_mile': 1.90, 'premium_mile': 2.00, 'standard_day': 550, 'premium_day': 600},
            'High Pole': {'standard_mile': 2.10, 'premium_mile': 2.25, 'standard_day': 650, 'premium_day': 750},
            'Steerman': {'standard_mile': 2.10, 'premium_mile': 2.50, 'standard_day': 650, 'premium_day': 750},
            'Route Survey': {'standard_mile': 2.25, 'premium_mile': 2.50, 'standard_day': 800, 'premium_day': 800}
        },
        'Southwest': {
            'Lead / Chase': {'standard_mile': 1.90, 'premium_mile': 2.00, 'standard_day': 550, 'premium_day': 600},
            'High Pole': {'standard_mile': 2.10, 'premium_mile': 2.25, 'standard_day': 650, 'premium_day': 750},
            'Steerman': {'standard_mile': 2.10, 'premium_mile': 2.50, 'standard_day': 650, 'premium_day': 750},
            'Route Survey': {'standard_mile': 2.25, 'premium_mile': 2.50, 'standard_day': 800, 'premium_day': 800}
        },
        'Pacific Northwest': {
            'Lead / Chase': {'standard_mile': 2.00, 'premium_mile': 2.15, 'standard_day': 600, 'premium_day': 650},
            'High Pole': {'standard_mile': 2.25, 'premium_mile': 2.50, 'standard_day': 650, 'premium_day': 750},
            'Steerman': {'standard_mile': 2.25, 'premium_mile': 2.50, 'standard_day': 650, 'premium_day': 750},
            'Route Survey': {'standard_mile': 2.25, 'premium_mile': 2.50, 'standard_day': 800, 'premium_day': 800}
        }
    }

def calculate_distance_google_api(origin, destination):
    """Calculate distance using Google Maps Distance Matrix API"""
    try:
        api_key = os.environ.get('GOOGLE_MAPS_API_KEY') # changed 
        url = f"https://maps.googleapis.com/maps/api/distancematrix/json"
        
        params = {
            'origins': origin,
            'destinations': destination,
            'units': 'imperial',
            'key': api_key
        }
        
        response = requests.get(url, params=params, timeout=10)
        data = response.json()
        
        if data['status'] == 'OK' and data['rows'][0]['elements'][0]['status'] == 'OK':
            distance_text = data['rows'][0]['elements'][0]['distance']['text']
            # Extract miles from text like "123 mi"
            distance_miles = float(distance_text.replace(' mi', '').replace(',', ''))
            # Add 20% buffer
            return distance_miles * 1.2
        else:
            return None
            
    except Exception as e:
        print(f"Google API error: {e}")
        return None

def calculate_distance_fallback(origin_state, destination_state):
    """Fallback distance calculation using haversine formula"""
    # State coordinates (approximate center points)
    state_coords = {
        'AL': (32.806671, -86.791130), 'AK': (61.370716, -152.404419), 'AZ': (33.729759, -111.431221),
        'AR': (34.969704, -92.373123), 'CA': (36.116203, -119.681564), 'CO': (39.059811, -105.311104),
        'CT': (41.767, -72.677), 'DE': (39.161921, -75.526755), 'FL': (27.4518, -81.5158),
        'GA': (32.9866, -83.6487), 'HI': (21.1098, -157.5311), 'ID': (44.2394, -114.5103),
        'IL': (40.3363, -89.0022), 'IN': (39.8647, -86.2604), 'IA': (42.0046, -93.214),
        'KS': (38.5111, -96.8005), 'KY': (37.669, -84.6514), 'LA': (31.1801, -91.8749),
        'ME': (44.323535, -69.765261), 'MD': (39.0458, -76.6413), 'MA': (42.2373, -71.5314),
        'MI': (43.3504, -84.5603), 'MN': (45.7326, -93.9196), 'MS': (32.7673, -89.6812),
        'MO': (38.4623, -92.302), 'MT': (47.0527, -110.2854), 'NE': (41.1289, -98.2883),
        'NV': (38.4199, -117.1219), 'NH': (43.4108, -71.5653), 'NJ': (40.314, -74.5089),
        'NM': (34.8375, -106.2371), 'NY': (42.9538, -75.5268), 'NC': (35.630066, -79.806419),
        'ND': (47.5362, -99.793), 'OH': (40.3963, -82.7755), 'OK': (35.5376, -96.9247),
        'OR': (44.931109, -120.767178), 'PA': (40.269789, -76.875613), 'RI': (41.82355, -71.422132),
        'SC': (33.836082, -81.163727), 'SD': (44.299782, -99.438828), 'TN': (35.747845, -86.692345),
        'TX': (31.106, -97.6475), 'UT': (40.1135, -111.8535), 'VT': (44.0407, -72.7093),
        'VA': (37.768, -78.2057), 'WA': (47.3917, -121.5708), 'WV': (38.468, -80.9696),
        'WI': (44.2563, -89.6385), 'WY': (42.7475, -107.2085)
    }
    
    def haversine(lat1, lon1, lat2, lon2):
        R = 3959  # Earth's radius in miles
        dlat = math.radians(lat2 - lat1)
        dlon = math.radians(lon2 - lon1)
        a = (math.sin(dlat/2) * math.sin(dlat/2) + 
             math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * 
             math.sin(dlon/2) * math.sin(dlon/2))
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
        return R * c
    
    try:
        origin_coords = state_coords.get(origin_state.upper())
        dest_coords = state_coords.get(destination_state.upper())
        
        if origin_coords and dest_coords:
            distance = haversine(origin_coords[0], origin_coords[1], 
                               dest_coords[0], dest_coords[1])
            # Apply driving factor and buffer
            return distance * 1.3 * 1.2
        else:
            # Default distance if states not found
            return 500
    except:
        return 500

def determine_rate_type(pickup_date, pickup_state, is_superload):
    """Determine if standard or premium rates apply"""
    try:
        # Convert pickup_date string to date object if needed
        if isinstance(pickup_date, str):
            pickup_date = datetime.strptime(pickup_date, '%Y-%m-%d').date()
        
        days_until_pickup = (pickup_date - date.today()).days
        
        # Superload always gets premium rates
        if is_superload:
            return 'premium'
        
        # Special rules for NC, VA, SC
        if pickup_state.upper() in ['NC', 'VA', 'SC']:
            # Same day = premium
            if days_until_pickup <= 0:
                return 'premium'
            # Next day after 6 PM = premium (simplified to next day)
            elif days_until_pickup == 1:
                return 'premium'
            else:
                return 'standard'
        
        # General rule: less than 2 days = premium
        if days_until_pickup < 2:
            return 'premium'
        else:
            return 'standard'
            
    except:
        return 'standard'

def calculate_trip_days(distance_miles, pickup_time):
    """Calculate number of trip days based on distance and pickup time"""
    try:
        # Convert pickup time to hour
        pickup_hour = int(pickup_time.split(':')[0])
        
        # If pickup is after 1 PM, first day is limited to 150 miles
        if pickup_hour >= 13:
            first_day_miles = min(distance_miles, 150)
            remaining_miles = max(0, distance_miles - 150)
            additional_days = math.ceil(remaining_miles / 400) if remaining_miles > 0 else 0
            total_days = 1 + additional_days
        else:
            total_days = max(1, math.ceil(distance_miles / 400))
        
        return total_days
    except:
        return max(1, math.ceil(distance_miles / 400))

def calculate_quote(quote_data):
    """Calculate quote based on provided data"""
    try:
        # Extract data
        pickup_location = f"{quote_data['pickup_location']}, {quote_data['pickup_state']}"
        delivery_location = f"{quote_data['delivery_location']}, {quote_data['delivery_state']}"
        pickup_state = quote_data['pickup_state']
        car_types = quote_data['car_types']
        is_superload = quote_data.get('is_superload', False)
        pickup_date = quote_data['pickup_date']
        pickup_time = quote_data['pickup_time']
        
        # Calculate distance
        distance = calculate_distance_google_api(pickup_location, delivery_location)
        if distance is None:
            distance = calculate_distance_fallback(pickup_state, quote_data['delivery_state'])
        
        # Determine rate type and region
        rate_type = determine_rate_type(pickup_date, pickup_state, is_superload)
        region = get_region_by_state(pickup_state)
        rates = get_regional_rates()[region]
        
        # Calculate trip days
        trip_days = calculate_trip_days(distance, pickup_time)
        
        # Calculate costs for each car type
        quote_breakdown = {}
        total_cost = 0
        
        for car_type in car_types:
            if car_type in rates:
                car_rates = rates[car_type]
                
                # Get appropriate rates
                mile_rate = car_rates[f'{rate_type}_mile']
                day_rate = car_rates[f'{rate_type}_day']
                
                # Calculate daily costs
                daily_breakdown = []
                car_total = 0
                
                for day in range(trip_days):
                    if day == 0:  # First day
                        if pickup_time and int(pickup_time.split(':')[0]) >= 13:
                            day_miles = min(distance, 150)
                        else:
                            day_miles = min(distance, 400)
                    else:
                        remaining_distance = distance - (400 * day if pickup_time and int(pickup_time.split(':')[0]) < 13 else 150 + 400 * (day - 1))
                        day_miles = min(remaining_distance, 400) if remaining_distance > 0 else 0
                    
                    # Calculate costs
                    mileage_cost = day_miles * mile_rate
                    daily_cost = max(mileage_cost, day_rate)
                    
                    # Add overnight fee for all days except last
                    if day < trip_days - 1:
                        daily_cost += 125
                    
                    daily_breakdown.append({
                        'day': day + 1,
                        'miles': round(day_miles, 1),
                        'mileage_cost': round(mileage_cost, 2),
                        'day_rate': day_rate,
                        'daily_cost': round(daily_cost, 2),
                        'overnight_fee': 125 if day < trip_days - 1 else 0
                    })
                    
                    car_total += daily_cost
                
                quote_breakdown[car_type] = {
                    'total': round(car_total, 2),
                    'daily_breakdown': daily_breakdown,
                    'mile_rate': mile_rate,
                    'day_rate': day_rate
                }
                
                total_cost += car_total
        
        return {
            'success': True,
            'distance': round(distance, 1),
            'rate_type': rate_type,
            'region': region,
            'trip_days': trip_days,
            'total_cost': round(total_cost, 2),
            'breakdown': quote_breakdown
        }
        
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }

# Authentication decorator
def login_required(f):
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        
        # Check if user is suspended
        user = User.query.get(session['user_id'])
        if user and user.is_suspended:
            session.clear()
            flash('Your account has been suspended. Please contact support.')
            return redirect(url_for('login'))
            
        return f(*args, **kwargs)
    decorated_function.__name__ = f.__name__
    return decorated_function

def trucking_company_required(f):
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        
        user = User.query.get(session['user_id'])
        if not user:
            session.clear()
            return redirect(url_for('login'))
            
        if user.is_suspended:
            session.clear()
            flash('Your account has been suspended. Please contact support.')
            return redirect(url_for('login'))
            
        if user.user_type != 'trucking_company':
            flash('This feature is only available to trucking companies.')
            return redirect(url_for('dashboard'))
            
        if not user.is_approved and not user.is_admin:
            flash('Your account is pending approval. Please wait for admin approval.')
            return redirect(url_for('dashboard'))
            
        return f(*args, **kwargs)
    decorated_function.__name__ = f.__name__
    return decorated_function

def vendor_required(f):
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        
        user = User.query.get(session['user_id'])
        if not user:
            session.clear()
            return redirect(url_for('login'))
            
        if user.is_suspended:
            session.clear()
            flash('Your account has been suspended. Please contact support.')
            return redirect(url_for('login'))
            
        if user.user_type != 'vendor':
            flash('This feature is only available to vendors.')
            return redirect(url_for('dashboard'))
            
        return f(*args, **kwargs)
    decorated_function.__name__ = f.__name__
    return decorated_function

def admin_required(f):
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        user = User.query.get(session['user_id'])
        if not user or not user.is_admin:
            flash('Admin access required')
            return redirect(url_for('dashboard'))
        return f(*args, **kwargs)
    decorated_function.__name__ = f.__name__
    return decorated_function

# Routes
@app.route('/', methods=['GET', 'POST'])
def index():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        # Redirect POST requests to login handler
        return login()
    
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password_hash, password):
            # Check if user is suspended
            if user.is_suspended:
                flash('Your account has been suspended. Please contact support.')
                return render_template('login.html')
            
            session['user_id'] = user.id
            session['company_name'] = user.company_name
            session['is_admin'] = user.is_admin
            session['user_type'] = user.user_type
            session['is_approved'] = user.is_approved
            
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid email or password')
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        company_name = request.form['company_name']
        email = request.form['email']
        phone_number = request.form['phone_number']
        password = request.form['password']
        user_type = request.form.get('user_type', 'trucking_company')
        
        if User.query.filter_by(email=email).first():
            flash('Email already registered')
            return render_template('register.html')
        
        # For trucking companies, DOT number is required
        if user_type == 'trucking_company':
            dot_number = request.form.get('dot_number')
            if not dot_number:
                flash('DOT number is required for trucking companies')
                return render_template('register.html')
                
            # Check if DOT number already exists
            if User.query.filter_by(dot_number=dot_number).first():
                flash('DOT number already registered')
                return render_template('register.html')
        else:
            dot_number = None
        
        # Trucking companies need approval, vendors are auto-approved
        is_approved = True if user_type == 'vendor' else False
        
        user = User(
            company_name=company_name,
            email=email,
            phone_number=phone_number,
            dot_number=dot_number,
            password_hash=generate_password_hash(password),
            user_type=user_type,
            is_approved=is_approved
        )
        db.session.add(user)
        db.session.commit()
        
        if user_type == 'trucking_company':
            flash('Registration successful! Your account is pending approval. You will be notified once approved.')
        else:
            flash('Registration successful! Please log in.')
            
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    user = User.query.get(session['user_id'])
    if not user:
        # User not found, clear session and redirect to login
        session.clear()
        return redirect(url_for('login'))
    
    # Redirect vendor users to their vendor dashboard
    if user.user_type == 'vendor':
        return redirect('/vendor/dashboard')
    
    # For trucking companies, get recent routes if approved
    if user.user_type == 'trucking_company' and user.is_approved:
        recent_routes = SavedRoute.query.filter_by(user_id=user.id).order_by(SavedRoute.created_at.desc()).limit(5).all()
    else:
        recent_routes = []
    
    return render_template('dashboard.html', user=user, recent_routes=recent_routes)

@app.route('/load-plan')
@trucking_company_required
def load_plan():
    return render_template('load_plan.html')

@app.route('/calculate-route', methods=['POST'])
@login_required
def calculate_route():
    try:
        data = request.get_json()
        
        # Extract load data
        load_data = {
            'origin': data.get('origin'),
            'destination': data.get('destination'),
            'road_type': data.get('road_type'),
            'length': data.get('length'),
            'width': data.get('width'),
            'height': data.get('height'),
            'weight': data.get('weight'),
            'front_overhang': data.get('front_overhang', 0),
            'rear_overhang': data.get('rear_overhang', 0),
            'custom_route': data.get('custom_route', [])
        }
        
        # Use custom route if provided, otherwise use default states
        states = load_data['custom_route'] if load_data['custom_route'] else ['VA', 'NC', 'SC', 'GA', 'AL']
        
        # Calculate escort requirements
        results = calculate_escort_requirements(load_data, states)
        
        # Auto-save the load plan calculation for admin visibility
        # Generate an auto-save route name in the same format as quotes
        def extract_city_state(address):
            """Extract city and state from full address"""
            if not address:
                return "Unknown Location"
            
            # Split by comma and take the first part as city
            parts = address.split(',')
            if len(parts) >= 2:
                city = parts[0].strip()
                # Look for state in the second part
                state_part = parts[1].strip()
                # Extract state abbreviation (2 letters)
                state_match = re.search(r'\b([A-Z]{2})\b', state_part)
                if state_match:
                    state = state_match.group(1)
                    return f"{city}, {state}"
                else:
                    # If no state abbreviation found, use the state part as is
                    return f"{city}, {state_part}"
            else:
                # If no comma, just return the address as is
                return address
        
        origin_clean = extract_city_state(load_data['origin'])
        destination_clean = extract_city_state(load_data['destination'])
        auto_route_name = f"{origin_clean} > {destination_clean}"
        
        auto_saved_route = SavedRoute(
            user_id=session['user_id'],
            route_name=auto_route_name,
            origin=load_data['origin'],
            destination=load_data['destination'],
            road_type=load_data['road_type'],
            length=load_data['length'],
            width=load_data['width'],
            height=load_data['height'],
            weight=load_data['weight'],
            front_overhang=load_data['front_overhang'],
            rear_overhang=load_data['rear_overhang'],
            custom_route=json.dumps(states),
            route_results=json.dumps(results)
        )
        
        db.session.add(auto_saved_route)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'route_summary': {
                'origin': load_data['origin'],
                'destination': load_data['destination'],
                'road_type': load_data['road_type'],
                'states': ' → '.join(states)
            },
            'results': results
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/save-route', methods=['POST'])
@login_required
def save_route():
    try:
        data = request.get_json()
        
        route = SavedRoute(
            user_id=session['user_id'],
            route_name=data.get('route_name'),
            origin=data.get('origin'),
            destination=data.get('destination'),
            road_type=data.get('road_type'),
            length=data.get('length'),
            width=data.get('width'),
            height=data.get('height'),
            weight=data.get('weight'),
            front_overhang=data.get('front_overhang'),
            rear_overhang=data.get('rear_overhang'),
            custom_route=json.dumps(data.get('custom_route', [])),
            route_results=json.dumps(data.get('results', []))
        )
        
        db.session.add(route)
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'Route saved successfully'})
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/my-routes')
@login_required
def my_routes():
    routes = SavedRoute.query.filter_by(user_id=session['user_id']).order_by(SavedRoute.created_at.desc()).all()
    return render_template('my_routes.html', routes=routes)

@app.route('/get-quote')
@trucking_company_required
def get_quote():
    return render_template('get_quote.html')

@app.route('/calculate-quote', methods=['POST'])
@trucking_company_required
def calculate_quote_route():
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['pickup_date', 'pickup_time', 'pickup_location', 'pickup_state', 
                          'delivery_location', 'delivery_state', 'car_types']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'success': False, 'error': f'Missing required field: {field}'}), 400
        
        # Calculate quote
        result = calculate_quote(data)
        
        if result['success']:
            # Save quote to database
            quote = Quote(
                user_id=session['user_id'],
                pickup_date=datetime.strptime(data['pickup_date'], '%Y-%m-%d').date(),
                pickup_time=data['pickup_time'],
                pickup_location=data['pickup_location'],
                pickup_state=data['pickup_state'],
                delivery_location=data['delivery_location'],
                delivery_state=data['delivery_state'],
                car_types=json.dumps(data['car_types']),
                is_superload=data.get('is_superload', False),
                distance_miles=result['distance'],
                rate_type=result['rate_type'],
                region=result['region'],
                total_cost=result['total_cost'],
                quote_breakdown=json.dumps(result['breakdown'])
            )
            
            db.session.add(quote)
            db.session.commit()
            
            return jsonify({
                'success': True,
                'quote_id': quote.id,
                'result': result
            })
        else:
            return jsonify(result), 400
            
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/my-quotes')
@trucking_company_required
def my_quotes():
    quotes = Quote.query.filter_by(user_id=session['user_id']).order_by(Quote.created_at.desc()).all()
    return render_template('my_quotes.html', quotes=quotes)

@app.route('/admin')
@admin_required
def admin_dashboard():
    users = User.query.all()
    total_routes = SavedRoute.query.count()
    total_quotes = Quote.query.count()
    
    # Calculate total revenue from quotes
    total_revenue = db.session.query(db.func.sum(Quote.total_cost)).scalar() or 0
    
    # Get vendor location statistics
    total_vendor_locations = VendorLocation.query.count()
    active_vendor_locations = VendorLocation.query.filter(
        VendorLocation.expires_at > datetime.utcnow()
    ).count()
    
    # Fetch all saved routes for admin viewing
    all_routes = db.session.query(SavedRoute, User)\
        .join(User, SavedRoute.user_id == User.id)\
        .order_by(SavedRoute.created_at.desc())\
        .all()
    
    # Fetch all quotes for admin viewing
    all_quotes = db.session.query(Quote, User)\
        .join(User, Quote.user_id == User.id)\
        .order_by(Quote.created_at.desc())\
        .all()
    
    # Get current time
    current_time = datetime.now().strftime('%m/%d/%Y %I:%M %p')
    
    return render_template('admin.html', users=users, total_routes=total_routes, 
                         total_quotes=total_quotes, total_revenue=total_revenue,
                         total_vendor_locations=total_vendor_locations, 
                         active_vendor_locations=active_vendor_locations,
                         all_routes=all_routes, all_quotes=all_quotes, current_time=current_time)

@app.route('/admin/customers')
@admin_required
def admin_customers():
    users = User.query.filter_by(is_admin=False).order_by(User.created_at.desc()).all()
    return render_template('admin_customers.html', users=users)

@app.route('/admin/quotes')
@admin_required
def admin_quotes():
    quotes = db.session.query(Quote, User)\
        .join(User, Quote.user_id == User.id)\
        .order_by(Quote.created_at.desc())\
        .all()
    return render_template('admin_quotes.html', quotes=quotes)

@app.route('/admin/load-plans')
@admin_required
def admin_load_plans():
    routes = db.session.query(SavedRoute, User)\
        .join(User, SavedRoute.user_id == User.id)\
        .order_by(SavedRoute.created_at.desc())\
        .all()
    return render_template('admin_load_plans.html', routes=routes)

# Vendor Routes
@app.route('/vendor/share-location')
def vendor_share_location():
    """Public route for guest vendors to share location"""
    user = None
    if 'user_id' in session:
        user = User.query.get(session['user_id'])
    return render_template('vendor/share_location.html', user=user)

@app.route('/vendor/dashboard')
@vendor_required
def vendor_dashboard():
    """Dashboard for registered vendors"""
    user = User.query.get(session['user_id'])
    active_locations = VendorLocation.query.filter(
        VendorLocation.user_id == user.id,
        VendorLocation.expires_at > datetime.utcnow()
    ).order_by(VendorLocation.created_at.desc()).all()
    
    return render_template('vendor/dashboard.html', user=user, active_locations=active_locations)

@app.route('/vendor/submit-location', methods=['POST'])
def submit_vendor_location():
    """Handle location submission from both guest and registered vendors"""
    try:
        data = request.get_json()
        
        # Get latitude and longitude from the data
        latitude = data.get('latitude')
        longitude = data.get('longitude')
        
        # Calculate city and state from coordinates if not provided
        location_city = data.get('location_city')
        location_state = data.get('location_state')
        
        if latitude and longitude and (not location_city or not location_state):
            calculated_city, calculated_state = get_city_state_from_coordinates(latitude, longitude)
            if not location_city and calculated_city:
                location_city = calculated_city
            if not location_state and calculated_state:
                location_state = calculated_state
        
        # Calculate expiration time (48 hours from now)
        expires_at = datetime.utcnow() + timedelta(hours=48)
        
        # Determine if this is a registered vendor
        user_id = session.get('user_id') if 'user_id' in session else None
        is_registered = False
        
        if user_id:
            user = User.query.get(user_id)
            if user and user.user_type == 'vendor':
                is_registered = True
        
        location = VendorLocation(
            user_id=user_id,
            company_name=data.get('company_name'),
            contact_name=data.get('contact_name'),
            email=data.get('email'),
            phone=data.get('phone'),
            location_city=location_city,
            location_state=location_state,
            latitude=latitude,
            longitude=longitude,
            coverage_radius=int(data.get('coverage_radius', 100)),
            services_provided=json.dumps(data.get('services_provided', [])),
            notes=data.get('notes', ''),
            is_registered_vendor=is_registered,
            expires_at=expires_at
        )
        
        db.session.add(location)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Location shared successfully! Your location will be visible for 48 hours.',
            'expires_at': expires_at.strftime('%m/%d/%Y %I:%M %p')
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/vendor/register-as-vendor')
def register_as_vendor():
    """Registration form specifically for vendors"""
    return render_template('vendor/register.html')

@app.route('/admin/vendor-locations')
@admin_required
def admin_vendor_locations():
    """Admin view for vendor locations and trip assignment"""
    # Get active vendor locations (not expired)
    active_locations_query = VendorLocation.query.filter(
        VendorLocation.expires_at > datetime.utcnow()
    ).order_by(VendorLocation.created_at.desc()).all()
    
    # Convert to dictionaries for JSON serialization
    active_locations = []
    for location in active_locations_query:
        try:
            services = json.loads(location.services_provided) if location.services_provided else []
        except:
            services = []
            
        active_locations.append({
            'id': location.id,
            'user_id': location.user_id,
            'company_name': location.company_name,
            'contact_name': location.contact_name,
            'email': location.email,
            'phone': location.phone,
            'location_city': location.location_city,
            'location_state': location.location_state,
            'latitude': location.latitude,
            'longitude': location.longitude,
            'coverage_radius': location.coverage_radius,
            'services_provided': services,
            'notes': location.notes,
            'is_registered_vendor': location.is_registered_vendor,
            'expires_at': location.expires_at.strftime('%m/%d/%Y %I:%M %p'),
            'created_at': location.created_at.strftime('%m/%d/%Y %I:%M %p')
        })
    
    return render_template('admin/vendor_locations.html', locations=active_locations)

@app.route('/admin/search-vendors', methods=['POST'])
@admin_required
def search_vendors():
    """Search for vendors near a location"""
    try:
        data = request.get_json()
        search_location = data.get('location')
        latitude = data.get('latitude')
        longitude = data.get('longitude')
        radius = int(data.get('radius', 100))  # Default 100 miles
        
        # Get active vendor locations
        active_locations = VendorLocation.query.filter(
            VendorLocation.expires_at > datetime.utcnow()
        ).all()
        
        # Filter by distance if coordinates provided
        nearby_vendors = []
        if latitude and longitude:
            for location in active_locations:
                if location.latitude and location.longitude:
                    distance = calculate_distance_haversine(
                        latitude, longitude, 
                        location.latitude, location.longitude
                    )
                    if distance <= radius:
                        nearby_vendors.append({
                            'id': location.id,
                            'company_name': location.company_name,
                            'contact_name': location.contact_name,
                            'email': location.email,
                            'phone': location.phone,
                            'location': f"{location.location_city}, {location.location_state}",
                            'distance': round(distance, 1),
                            'services': json.loads(location.services_provided),
                            'coverage_radius': location.coverage_radius,
                            'is_registered': location.is_registered_vendor,
                            'expires_at': location.expires_at.strftime('%m/%d/%Y %I:%M %p')
                        })
            
            # Sort by distance
            nearby_vendors.sort(key=lambda x: x['distance'])
        else:
            # If no coordinates, return all active vendors
            for location in active_locations:
                nearby_vendors.append({
                    'id': location.id,
                    'company_name': location.company_name,
                    'contact_name': location.contact_name,
                    'email': location.email,
                    'phone': location.phone,
                    'location': f"{location.location_city}, {location.location_state}",
                    'distance': None,
                    'services': json.loads(location.services_provided),
                    'coverage_radius': location.coverage_radius,
                    'is_registered': location.is_registered_vendor,
                    'expires_at': location.expires_at.strftime('%m/%d/%Y %I:%M %p')
                })
        
        return jsonify({
            'success': True,
            'vendors': nearby_vendors,
            'total_found': len(nearby_vendors)
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/admin/manage-users')
@admin_required
def admin_manage_users():
    """Enhanced user management with approval and suspension"""
    trucking_companies = User.query.filter_by(user_type='trucking_company', is_admin=False).order_by(User.created_at.desc()).all()
    vendors = User.query.filter_by(user_type='vendor', is_admin=False).order_by(User.created_at.desc()).all()
    
    return render_template('admin/manage_users.html', 
                         trucking_companies=trucking_companies, 
                         vendors=vendors)

@app.route('/admin/trucking-companies')
@admin_required
def admin_trucking_companies():
    """Manage trucking companies with approval functionality"""
    trucking_companies = User.query.filter_by(user_type='trucking_company', is_admin=False).order_by(User.created_at.desc()).all()
    return render_template('admin/trucking_companies.html', trucking_companies=trucking_companies)

@app.route('/admin/vendors')
@admin_required
def admin_vendors():
    """Manage vendors"""
    vendors = User.query.filter_by(user_type='vendor', is_admin=False).order_by(User.created_at.desc()).all()
    return render_template('admin/vendors.html', vendors=vendors)

@app.route('/admin/approve-user/<int:user_id>', methods=['POST'])
@admin_required
def approve_user(user_id):
    """Approve a trucking company user"""
    user = User.query.get_or_404(user_id)
    if user.user_type == 'trucking_company':
        user.is_approved = True
        db.session.commit()
        return jsonify({'success': True, 'message': f'{user.company_name} has been approved'})
    else:
        return jsonify({'success': False, 'error': 'Only trucking companies require approval'}), 400

@app.route('/admin/suspend-user/<int:user_id>', methods=['POST'])
@admin_required
def suspend_user(user_id):
    """Suspend a user"""
    user = User.query.get_or_404(user_id)
    user.is_suspended = True
    db.session.commit()
    return jsonify({'success': True, 'message': f'{user.company_name} has been suspended'})

@app.route('/admin/unsuspend-user/<int:user_id>', methods=['POST'])
@admin_required
def unsuspend_user(user_id):
    """Unsuspend a user"""
    user = User.query.get_or_404(user_id)
    user.is_suspended = False
    db.session.commit()
    return jsonify({'success': True, 'message': f'{user.company_name} has been unsuspended'})

def calculate_distance_haversine(lat1, lon1, lat2, lon2):
    """Calculate distance between two points using haversine formula"""
    R = 3959  # Earth's radius in miles
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (math.sin(dlat/2) * math.sin(dlat/2) + 
         math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * 
         math.sin(dlon/2) * math.sin(dlon/2))
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    return R * c

# Pilot Car Order Routes
@app.route('/order-pilot-car')
def order_pilot_car():
    """Pilot car order form - accessible to both registered and guest users"""
    user = None
    if 'user_id' in session:
        user = User.query.get(session['user_id'])
        # Check if trucking company user is approved
        if user and user.user_type == 'trucking_company' and not user.is_approved and not user.is_admin:
            flash('Your account is pending approval. You can still place orders as a guest.')
            user = None
    
    return render_template('order_pilot_car.html', user=user)

@app.route('/submit-pilot-car-order', methods=['POST'])
def submit_pilot_car_order():
    """Handle pilot car order submission"""
    try:
        data = request.get_json()
        
        # Determine user_id for registered users
        user_id = session.get('user_id') if 'user_id' in session else None
        
        # Create the order
        order = PilotCarOrder(
            user_id=user_id,
            # Company Information
            company_name=data.get('company_name'),
            dot_number=data.get('dot_number'),
            # Pickup & Delivery
            pickup_address=data.get('pickup_address'),
            delivery_address=data.get('delivery_address'),
            # Service Details
            pickup_date=datetime.strptime(data.get('pickup_date'), '%Y-%m-%d').date(),
            pickup_time=data.get('pickup_time'),
            pilot_car_positions=json.dumps(data.get('pilot_car_positions', [])),
            # Driver Information
            driver_name=data.get('driver_name'),
            driver_phone=data.get('driver_phone'),
            # Load Information
            length=data.get('length'),
            width=data.get('width'),
            height=data.get('height'),
            weight=data.get('weight'),
            truck_number=data.get('truck_number'),
            load_number=data.get('load_number'),
            load_description=data.get('load_description'),
            additional_notes=data.get('additional_notes'),
            # Contact Information
            contact_name=data.get('contact_name'),
            preferred_contact=data.get('preferred_contact'),
            phone_number=data.get('phone_number'),
            email=data.get('email'),
            # Payment Information
            po_number=data.get('po_number'),
            payment_method=data.get('payment_method'),
            terms_agreed=data.get('terms_agreed', False)
        )
        
        db.session.add(order)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'order_id': order.id,
            'message': f'Order #{order.id} submitted successfully! You will be contacted within 1 hour.'
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/my-orders')
@login_required
def my_orders():
    """View user's pilot car orders"""
    orders = PilotCarOrder.query.filter_by(user_id=session['user_id']).order_by(PilotCarOrder.created_at.desc()).all()
    return render_template('my_orders.html', orders=orders)

@app.route('/admin/orders')
@admin_required
def admin_orders():
    """Admin view for all pilot car orders"""
    orders = PilotCarOrder.query.order_by(PilotCarOrder.created_at.desc()).all()
    
    # Calculate statistics
    total_orders = len(orders)
    pending_orders = len([o for o in orders if o.status == 'pending'])
    confirmed_orders = len([o for o in orders if o.status == 'confirmed'])
    completed_orders = len([o for o in orders if o.status == 'completed'])
    cancelled_orders = len([o for o in orders if o.status == 'cancelled'])
    
    stats = {
        'total': total_orders,
        'pending': pending_orders,
        'confirmed': confirmed_orders,
        'completed': completed_orders,
        'cancelled': cancelled_orders
    }
    
    return render_template('admin/orders.html', orders=orders, stats=stats)

@app.route('/admin/order/<int:order_id>')
@admin_required
def admin_order_detail(order_id):
    """Admin view for order details"""
    order = PilotCarOrder.query.get_or_404(order_id)
    return render_template('admin/order_detail.html', order=order)

@app.route('/admin/update-order-status/<int:order_id>', methods=['POST'])
@admin_required
def update_order_status(order_id):
    """Update order status and notes"""
    try:
        data = request.get_json()
        order = PilotCarOrder.query.get_or_404(order_id)
        
        order.status = data.get('status', order.status)
        if data.get('admin_notes'):
            order.admin_notes = data.get('admin_notes')
        if data.get('estimated_cost'):
            order.estimated_cost = float(data.get('estimated_cost'))
        if data.get('final_cost'):
            order.final_cost = float(data.get('final_cost'))
        
        order.updated_at = datetime.utcnow()
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': f'Order #{order.id} updated successfully'
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        
        # Create default admin user if it doesn't exist
        admin = User.query.filter_by(email='admin@mypevo.com').first()
        if not admin:
            admin = User(
                company_name='My PEVO Admin',
                email='admin@mypevo.com',
                password_hash=generate_password_hash('admin123'),
                is_admin=True,
                user_type='trucking_company',
                is_approved=True
            )
            db.session.add(admin)
            db.session.commit()
    
    app.run(debug=True)