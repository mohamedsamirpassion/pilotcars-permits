# Step-by-Step Implementation Guide

This guide walks you through implementing the Load Planning feature in your Flask application from start to finish.

## Prerequisites

Before starting, ensure you have:
- Flask application running
- Python 3.8+ installed
- Basic knowledge of Flask, HTML, CSS, and JavaScript
- Google Maps API access (free tier available)
- Email service configured (Gmail, SendGrid, etc.)

---

## Phase 1: Environment Setup

### Step 1: Install Dependencies

Add these to your `requirements.txt`:

```txt
# Core dependencies (if not already installed)
Flask>=3.0.0
Flask-Mail>=0.9.1
Flask-WTF>=1.2.1
WTForms>=3.1.1
email-validator>=2.1.0
python-dotenv>=1.0.0
```

Install dependencies:
```bash
pip install -r requirements.txt
```

### Step 2: Configure Environment Variables

Create or update your `.env` file:

```env
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
```

### Step 3: Get Google Maps API Key

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing one
3. Enable these APIs:
   - Maps JavaScript API
   - Places API
   - Directions API
   - Geocoding API
4. Create credentials → API key
5. Restrict the API key to your domain (for production)

---

## Phase 2: Backend Implementation

### Step 4: Update Flask Configuration

Add to your `config.py`:

```python
import os

class Config:
    # Existing configuration...
    
    # Google Maps API
    GOOGLE_MAPS_API_KEY = os.environ.get('GOOGLE_MAPS_API_KEY')
    
    # Email configuration
    MAIL_SERVER = os.environ.get('MAIL_SERVER') or 'smtp.gmail.com'
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 587)
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER')
    ADMIN_EMAIL = os.environ.get('ADMIN_EMAIL')
```

### Step 5: Initialize Flask Extensions

In your main app file (`app.py`):

```python
from flask import Flask
from flask_mail import Mail
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)
app.config.from_object('config.Config')

# Initialize extensions
mail = Mail(app)
csrf = CSRFProtect(app)

# Register the load planning blueprint
from routes.load_planning_routes import bp as load_planning_bp
app.register_blueprint(load_planning_bp)

if __name__ == '__main__':
    app.run(debug=True)
```

### Step 6: Create Routes File

Copy `routes/load_planning_routes.py` to your `routes/` directory.

If you don't have a routes directory:
```bash
mkdir routes
touch routes/__init__.py
```

### Step 7: Test Backend Routes

Start your Flask app and test the routes:

```bash
python app.py
```

Test endpoints:
- `http://localhost:5000/load-planning/` (should show 404 for now - that's expected)
- Check that the blueprint is registered without errors

---

## Phase 3: Frontend Implementation

### Step 8: Copy Static Files

Create directories and copy files:

```bash
mkdir -p static/js
```

Copy these files to your project:
- `static/js/state_regulations.js` (complete version from original project)
- `static/js/load_planning_complete.js`

### Step 9: Update Base Template

Ensure your `templates/base.html` includes required dependencies:

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}Your App{% endblock %}</title>
    
    <!-- Bootstrap CSS -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    
    <!-- Font Awesome -->
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    
    <!-- jQuery (required) -->
    <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
    
    {% block extra_head %}{% endblock %}
</head>
<body>
    <!-- Your navigation -->
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
        <div class="container">
            <a class="navbar-brand" href="/">Your App</a>
            <div class="navbar-nav">
                <a class="nav-link" href="/load-planning/">Load Planning</a>
            </div>
        </div>
    </nav>
    
    <!-- Main content -->
    <main class="{% block main_class %}container mt-4{% endblock %}">
        {% block content %}{% endblock %}
    </main>
    
    <!-- Bootstrap JS -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    
    {% block extra_scripts %}{% endblock %}
</body>
</html>
```

### Step 10: Copy Template File

Copy `templates/load_plan.html` to your `templates/` directory.

### Step 11: Add Google Maps Script

Add to your base template or the load planning template:

```html
<!-- Add to base.html before closing </body> tag -->
<script>
    function initMap() {
        console.log('Google Maps API loaded successfully');
    }
    
    // Load Google Maps API
    function loadGoogleMaps() {
        if (typeof $ !== 'undefined') {
            const script = document.createElement('script');
            script.src = 'https://maps.googleapis.com/maps/api/js?key={{ config.GOOGLE_MAPS_API_KEY }}&libraries=places&callback=initMap';
            script.onerror = function() { console.error('Failed to load Google Maps API'); };
            document.head.appendChild(script);
        } else {
            setTimeout(loadGoogleMaps, 100);
        }
    }
    
    // Initialize when page loads
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', loadGoogleMaps);
    } else {
        loadGoogleMaps();
    }
</script>
```

---

## Phase 4: Testing and Debugging

### Step 12: Test the Basic Interface

1. Start your Flask app:
   ```bash
   python app.py
   ```

2. Navigate to `http://localhost:5000/load-planning/`

3. Verify you can see:
   - Load planning form
   - Map container (may be empty if Google Maps isn't loading)
   - State selection input

### Step 13: Debug Common Issues

**Issue: Google Maps not loading**
- Check browser console for API key errors
- Verify API key has correct permissions
- Ensure billing is enabled in Google Cloud (even for free tier)

**Issue: JavaScript errors**
- Check browser console for missing jQuery or other dependencies
- Verify static files are loading correctly
- Check for typos in script URLs

**Issue: Form not submitting**
- Check browser console for JavaScript errors
- Verify CSRF token is working
- Check Flask logs for backend errors

### Step 14: Test Core Functionality

Test each component:

1. **State Selection:**
   - Type state names in the search box
   - Verify autocomplete works
   - Test adding and removing states

2. **Form Validation:**
   - Try submitting empty form
   - Test with invalid dimensions
   - Verify error messages appear

3. **Dimension Calculations:**
   - Enter dimensions and verify real-time totals
   - Test inch-to-feet conversion (enter 15 inches, should become 1'3")

4. **Map Integration:**
   - Enter origin and destination
   - Verify route appears on map
   - Test map controls (satellite view, reset)

---

## Phase 5: Email Configuration

### Step 15: Configure Email Service

For Gmail (recommended for testing):

1. Enable 2-factor authentication on your Google account
2. Generate an app password:
   - Go to Google Account settings
   - Security → App passwords
   - Select "Mail" and generate password
3. Use the app password in your `.env` file

For production, consider using:
- SendGrid
- Amazon SES
- Mailgun

### Step 16: Test Email Functionality

1. Fill out the load planning form
2. Click "Calculate Escort Requirements"
3. Click "Report Issue" button
4. Fill out report form and submit
5. Check that email is received at `ADMIN_EMAIL`

---

## Phase 6: Production Deployment

### Step 17: Security Configuration

Update your configuration for production:

```python
import os

class ProductionConfig:
    SECRET_KEY = os.environ.get('SECRET_KEY')  # Must be set in production
    GOOGLE_MAPS_API_KEY = os.environ.get('GOOGLE_MAPS_API_KEY')
    
    # Email configuration
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 587)
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER')
    ADMIN_EMAIL = os.environ.get('ADMIN_EMAIL')
    
    # Security settings
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
```

### Step 18: Environment Variables for Production

Set these environment variables on your production server:

```bash
export SECRET_KEY="your-production-secret-key"
export GOOGLE_MAPS_API_KEY="your-production-api-key"
export MAIL_SERVER="your-mail-server"
export MAIL_USERNAME="your-email@domain.com"
export MAIL_PASSWORD="your-app-password"
export ADMIN_EMAIL="admin@yourdomain.com"
```

### Step 19: Google Maps API Security

For production:

1. Restrict your API key to your domain:
   - Go to Google Cloud Console
   - APIs & Services → Credentials
   - Edit your API key
   - Set "Application restrictions" to "HTTP referrers"
   - Add your domain (e.g., `yourdomain.com/*`)

2. Monitor API usage to avoid unexpected charges

### Step 20: Performance Optimization

Consider these optimizations:

1. **Enable Gzip compression** in your web server
2. **Use a CDN** for static files
3. **Implement caching** for API responses
4. **Minify CSS and JavaScript** for production
5. **Enable browser caching** for static assets

---

## Phase 7: Customization

### Step 21: Customize Branding

Update CSS variables in the template:

```css
:root {
    --brand-primary: #your-primary-color;
    --brand-primary-light: #your-light-color;
    --brand-primary-dark: #your-dark-color;
    --brand-accent: #your-accent-color;
    --brand-border: #your-border-color;
}
```

### Step 22: Add Navigation

Add a link to your navigation:

```html
<!-- In your navigation template -->
<a href="/load-planning/" class="nav-link">
    <i class="fas fa-calculator"></i> Load Planning
</a>
```

### Step 23: Customize Footer

Update the results footer in the template:

```html
<div class="results-footer">
    <strong>Your Company Name</strong> - Professional Load Planning | 
    <small>Generated by Your App Name</small>
</div>
```

---

## Testing Checklist

Before going live, test:

- [ ] Load planning page loads without errors
- [ ] Google Maps displays correctly
- [ ] State selection autocomplete works
- [ ] Form validation shows appropriate errors
- [ ] Dimension calculations work correctly
- [ ] Route displays on map when origin/destination entered
- [ ] Calculate button processes form data
- [ ] Results display properly
- [ ] Share functionality works
- [ ] Print functionality works
- [ ] Report submission sends email
- [ ] Mobile responsiveness works
- [ ] All external dependencies load correctly

---

## Troubleshooting

### Common Issues and Solutions

**Problem:** Google Maps shows "For development purposes only"
**Solution:** Enable billing in Google Cloud Console (even for free tier)

**Problem:** Email not sending
**Solution:** Check SMTP credentials, firewall settings, and email provider restrictions

**Problem:** JavaScript errors in console
**Solution:** Ensure jQuery loads before other scripts, check for missing dependencies

**Problem:** CSRF token errors
**Solution:** Verify Flask-WTF is installed and configured correctly

**Problem:** Form submission fails
**Solution:** Check Flask logs, verify routes are registered correctly

---

## Next Steps

After successful implementation:

1. **Monitor usage** with Google Analytics
2. **Collect user feedback** for improvements
3. **Update state regulations** as they change
4. **Add more features** like saved routes or user accounts
5. **Implement analytics** to track feature usage
6. **Consider mobile app** version

## Support

For additional help:
- Check the API documentation
- Review the frontend integration guide
- Examine the customization guide
- Test with the provided examples

This implementation guide should get your Load Planning feature up and running successfully!
