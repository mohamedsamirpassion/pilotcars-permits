# My PEVO - Load Plan Service

A comprehensive web application for pilot car escort services that helps trucking companies plan routes and determine escort requirements for oversized loads.

## Overview

My PEVO is a professional load planning service designed specifically for trucking companies that transport oversized loads. The application provides:

- **Route Planning**: Interactive mapping with state-by-state route customization
- **Regulatory Compliance**: Automated escort requirement calculations based on load dimensions
- **State Regulations**: Comprehensive database of escort requirements by state
- **User Management**: Multi-user system with company-based accounts
- **Route History**: Save and manage previously planned routes

## Features

### For Trucking Companies
- Plan routes with custom state selection
- Calculate escort requirements (Front, Rear, Height Pole, Police, Route Survey)
- View detailed state-specific regulations and notes
- Save and manage route history
- Interactive map visualization

### For Administrators
- User management and analytics
- System monitoring and maintenance
- Route data oversight
- Comprehensive admin dashboard

## Technology Stack

- **Backend**: Python 3.10 + Flask 2.3.3
- **Database**: SQLite (development) / PostgreSQL (production ready)
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap 5
- **Mapping**: Leaflet.js with OpenStreetMap
- **Authentication**: Session-based with secure password hashing

## Installation

### Prerequisites
- Python 3.10 (Note: Not compatible with Python 3.13)
- pip (Python package manager)

### Setup Instructions

1. **Clone or download the application files**

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   python app.py
   ```

4. **Access the application**
   - Open your web browser
   - Navigate to: `http://localhost:5000`

## Default Login Credentials

**Admin Account:**
- Email: `admin@mypevo.com`
- Password: `admin123`

## User Guide

### Getting Started

1. **Create an Account**
   - Click "Create Account" on the login page
   - Enter your company name, email, and password
   - Log in with your new credentials

2. **Plan Your First Route**
   - Navigate to "Load Plan" from the dashboard
   - Enter trip information (origin and destination)
   - Select road type (Interstate or Non-Interstate)
   - Input load dimensions (length, width, height, weight)
   - Optionally add overhang measurements
   - Select custom route states if needed
   - Click "Calculate Escort Requirements"

3. **Review Results**
   - View the route summary
   - Check escort requirements for each state
   - Read state-specific notes and regulations
   - Save the route for future reference

### Load Dimensions Input

**Dimensions should include the complete unit:**
- **Length**: Total length including tractor and trailer
- **Width**: Maximum width of the load
- **Height**: Total height from ground to highest point
- **Weight**: Gross vehicle weight including load
- **Overhang**: Front and rear overhang from truck centers (optional)

### Escort Types Explained

- **None Required**: Load is within legal limits
- **Rear**: Pilot car following the load
- **Front**: Pilot car preceding the load
- **Height Pole**: Height measuring device required
- **Police**: Police escort required
- **Route Survey**: Pre-trip route analysis required

## State Regulations

The application includes comprehensive regulations for major states including:
- Virginia (VA)
- North Carolina (NC)
- South Carolina (SC)
- Georgia (GA)
- Alabama (AL)
- Florida (FL)
- Texas (TX)
- California (CA)

Each state entry includes:
- Width, height, length, and weight limits
- Corresponding escort requirements
- Special notes and permit information

## File Structure

```
mypevo/
├── app.py                      # Main Flask application
├── requirements.txt            # Python dependencies
├── README.md                  # This file
├── templates/                 # HTML templates
│   ├── base.html             # Base template
│   ├── login.html            # Login page
│   ├── register.html         # Registration page
│   ├── dashboard.html        # User dashboard
│   ├── load_plan.html        # Main load planning interface
│   ├── my_routes.html        # Route history
│   └── admin.html            # Admin dashboard
└── static/                   # Static assets
    ├── css/
    │   └── style.css         # Custom styles
    └── js/
        └── state_regulations.js  # State regulations database
```

## API Endpoints

### Authentication
- `GET /` - Login page
- `POST /login` - User authentication
- `POST /register` - User registration
- `GET /logout` - User logout

### Application Routes
- `GET /dashboard` - User dashboard
- `GET /load-plan` - Load planning interface
- `POST /calculate-route` - Calculate escort requirements
- `POST /save-route` - Save route to database
- `GET /my-routes` - View saved routes
- `GET /admin` - Admin dashboard (admin only)

## Database Schema

### Users Table
- `id`: Primary key
- `company_name`: Company name
- `email`: Login email (unique)
- `password_hash`: Hashed password
- `is_admin`: Admin flag
- `created_at`: Registration timestamp

### SavedRoute Table
- `id`: Primary key
- `user_id`: Foreign key to Users
- `route_name`: User-defined route name
- `origin/destination`: Trip endpoints
- `road_type`: Interstate or Non-Interstate
- `length/width/height/weight`: Load dimensions
- `front_overhang/rear_overhang`: Overhang measurements
- `custom_route`: JSON array of state codes
- `route_results`: JSON array of calculated results
- `created_at`: Save timestamp

## Development Notes

### Adding New States
To add new state regulations:

1. Edit `static/js/state_regulations.js`
2. Add new state object with appropriate limits
3. Include all escort types and notes
4. Update state selector in load plan template

### Security Considerations
- Change the secret key in production
- Use HTTPS in production
- Consider implementing rate limiting
- Regular backup of user data
- Update dependencies regularly

## Production Deployment

For production deployment:

1. **Database**: Switch to PostgreSQL
   ```python
   app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://user:pass@localhost/mypevo'
   ```

2. **Security**: Update the secret key
   ```python
   app.config['SECRET_KEY'] = 'your-secure-production-key'
   ```

3. **Web Server**: Use Gunicorn or similar WSGI server
   ```bash
   pip install gunicorn
   gunicorn -w 4 app:app
   ```

4. **Reverse Proxy**: Configure Nginx or Apache
5. **SSL Certificate**: Implement HTTPS
6. **Environment Variables**: Use environment-based configuration

## Support and Maintenance

### Regular Maintenance Tasks
- Update state regulations as laws change
- Monitor user activity and system performance
- Regular database backups
- Security updates for dependencies

### Troubleshooting
- Check browser console for JavaScript errors
- Verify all form fields are completed
- Ensure state regulations file is properly formatted
- Check database connectivity

## Future Enhancements

Planned features for future releases:
- **Vendor Service**: Pilot car availability and booking
- **Quote Service**: Automated pricing for escort services
- **Mobile App**: Native iOS and Android applications
- **API Integration**: Third-party mapping and traffic services
- **Advanced Analytics**: Route optimization and cost analysis

## License

Copyright © 2024 My PEVO. All rights reserved.

This software is proprietary and confidential. Unauthorized copying, distribution, or use is strictly prohibited.

## Contact

For technical support or business inquiries:
- Website: [Your Website]
- Email: [Your Email]
- Phone: [Your Phone]

---

**My PEVO** - Professional Pilot Car Escort Services 