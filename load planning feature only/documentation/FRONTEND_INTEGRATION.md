# Frontend Integration Guide

This guide explains how to integrate the Load Planning feature's frontend components into your Flask application.

## Overview

The Load Planning feature consists of:
- **HTML Template** - Main user interface
- **CSS Styling** - Responsive design and branding
- **JavaScript Logic** - Form handling, validation, calculations, and interactivity
- **External Dependencies** - Google Maps API, jQuery, Bootstrap (optional)

## Required Files

### 1. HTML Template
```
templates/load_plan.html
```

### 2. JavaScript Files
```
static/js/state_regulations.js
static/js/load_planning_complete.js
```

### 3. CSS (embedded in template)
The CSS is embedded in the HTML template's `{% block extra_head %}` section.

---

## Step-by-Step Integration

### Step 1: Copy Template Files

1. Copy `templates/load_plan.html` to your Flask app's templates directory
2. Copy `static/js/state_regulations.js` to your static/js directory
3. Copy `static/js/load_planning_complete.js` to your static/js directory

### Step 2: Update Base Template References

The load planning template extends `base.html`. Ensure your base template includes:

```html
<!-- base.html -->
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}Your App Name{% endblock %}</title>
    
    <!-- Bootstrap CSS (recommended) -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    
    <!-- Font Awesome (for icons) -->
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    
    <!-- jQuery (required) -->
    <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
    
    <!-- Additional head content -->
    {% block extra_head %}{% endblock %}
</head>
<body>
    <!-- Navigation -->
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
        <!-- Your navigation content -->
    </nav>
    
    <!-- Main content -->
    <main class="{% block main_class %}container mt-4{% endblock %}">
        {% block content %}{% endblock %}
    </main>
    
    <!-- Bootstrap JS -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    
    <!-- Additional scripts -->
    {% block extra_scripts %}{% endblock %}
</body>
</html>
```

### Step 3: Configure Google Maps API

1. **Get API Key**: Visit [Google Cloud Console](https://console.cloud.google.com/apis/credentials)
2. **Enable APIs**: Enable these APIs for your project:
   - Maps JavaScript API
   - Places API
   - Directions API
   - Geocoding API

3. **Add API Key to Template**: In your load_plan.html template, add the Google Maps script:

```html
<!-- Add to base.html or load_plan.html -->
<script>
    function initMap() {
        // This function will be called by the Google Maps API
        console.log('Google Maps API loaded');
    }
</script>
<script async defer 
        src="https://maps.googleapis.com/maps/api/js?key=YOUR_API_KEY&libraries=places&callback=initMap">
</script>
```

### Step 4: Update JavaScript References

Ensure the template includes both JavaScript files:

```html
<!-- In load_plan.html {% block extra_scripts %} -->
<script src="{{ url_for('static', filename='js/state_regulations.js') }}"></script>
<script src="{{ url_for('static', filename='js/load_planning_complete.js') }}"></script>
```

### Step 5: Customize Branding

Update the CSS variables in the template to match your brand:

```css
:root {
    --brand-primary: #your-primary-color;
    --brand-primary-light: #your-light-color;
    --brand-primary-dark: #your-dark-color;
    --brand-accent: #your-accent-color;
    --brand-border: #your-border-color;
}
```

---

## Required Dependencies

### External CDN Dependencies

The feature requires these external libraries:

```html
<!-- Required: jQuery -->
<script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>

<!-- Optional but recommended: Bootstrap -->
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>

<!-- Optional: Font Awesome Icons -->
<link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">

<!-- Required: Google Maps API -->
<script async defer src="https://maps.googleapis.com/maps/api/js?key=YOUR_API_KEY&libraries=places&callback=initMap"></script>
```

### Python Dependencies

Ensure these are in your requirements.txt:

```
Flask>=3.0.0
Flask-Mail>=0.9.1
Flask-WTF>=1.2.1
```

---

## JavaScript Integration

### Core Functions

The JavaScript provides these global functions:

```javascript
// Dimension display updates
updateDimensionDisplay(dimensionType)

// State management
removeState(stateAbbr)

// Results actions
shareResults()
printResults()
reportIssue()

// Modal management
closeShareModal()
closeReportModal()
submitReport()
```

### Event Handling

The JavaScript automatically handles:
- Form submission and validation
- State selection with autocomplete
- Real-time dimension calculations
- Google Maps integration
- Share/print/report functionality

### Custom Events

You can listen for custom events:

```javascript
// Listen for successful calculations
document.addEventListener('calculationComplete', function(e) {
    console.log('Calculation completed:', e.detail);
});

// Listen for validation errors
document.addEventListener('validationError', function(e) {
    console.log('Validation failed:', e.detail);
});
```

---

## CSS Customization

### Brand Colors

The template uses CSS custom properties for easy theming:

```css
/* Customize these variables */
:root {
    --brand-primary: #298553;      /* Main brand color */
    --brand-primary-light: #34a866; /* Lighter variant */
    --brand-primary-dark: #1e6b42;  /* Darker variant */
    --brand-accent: #f8f9fa;        /* Background accent */
    --brand-border: #e8f5e8;        /* Border color */
}
```

### Layout Customization

Key CSS classes you can customize:

```css
/* Main container */
.load-plan-container {
    /* Customize overall layout */
}

/* Form section */
.form-section {
    /* Customize form appearance */
}

/* Map section */
.map-section {
    /* Customize map container */
}

/* Results section */
.results-section {
    /* Customize results display */
}

/* State tags */
.state-tag {
    /* Customize selected state appearance */
}
```

### Mobile Responsiveness

The template includes mobile-optimized styles:

```css
@media (max-width: 768px) {
    .map-section {
        height: 450px; /* Fixed height for mobile */
    }
    
    .form-section {
        height: auto; /* Flexible height for mobile */
    }
}
```

---

## Form Integration

### Default Values

You can set default form values:

```javascript
document.addEventListener('DOMContentLoaded', function() {
    // Set default values
    document.getElementById('lengthFt').value = '75';
    document.getElementById('widthFt').value = '8';
    document.getElementById('heightFt').value = '13';
    document.getElementById('weight').value = '80000';
});
```

### Custom Validation

Add custom validation rules:

```javascript
function customValidation(formData) {
    const errors = [];
    
    // Add your custom validation logic
    if (formData.dimensions.weight > 100000) {
        errors.push({
            field: 'weight',
            message: 'Weight exceeds company limits'
        });
    }
    
    return errors;
}
```

### Pre-populate from URL Parameters

```javascript
document.addEventListener('DOMContentLoaded', function() {
    const urlParams = new URLSearchParams(window.location.search);
    
    if (urlParams.get('origin')) {
        document.getElementById('origin').value = urlParams.get('origin');
    }
    
    if (urlParams.get('destination')) {
        document.getElementById('destination').value = urlParams.get('destination');
    }
});
```

---

## Google Maps Configuration

### Basic Setup

```javascript
// Configure map options
const mapOptions = {
    zoom: 4,
    center: { lat: 39.8283, lng: -98.5795 }, // Center of US
    mapTypeId: google.maps.MapTypeId.ROADMAP
};

// Initialize map
const map = new google.maps.Map(document.getElementById('loadPlanMap'), mapOptions);
```

### Places Autocomplete

```javascript
// Configure autocomplete for city inputs
const autocompleteOptions = {
    types: ['(cities)'],
    componentRestrictions: { country: 'us' },
    fields: ['formatted_address', 'geometry', 'name']
};

const originAutocomplete = new google.maps.places.Autocomplete(
    document.getElementById('origin'), 
    autocompleteOptions
);
```

### Route Visualization

```javascript
// Display route on map
const directionsService = new google.maps.DirectionsService();
const directionsRenderer = new google.maps.DirectionsRenderer();

directionsRenderer.setMap(map);

const request = {
    origin: 'Charlotte, NC',
    destination: 'Mobile, AL',
    travelMode: google.maps.TravelMode.DRIVING
};

directionsService.route(request, function(result, status) {
    if (status === 'OK') {
        directionsRenderer.setDirections(result);
    }
});
```

---

## Error Handling

### Frontend Error Display

```javascript
function showError(message) {
    const errorDiv = document.createElement('div');
    errorDiv.className = 'alert alert-danger';
    errorDiv.innerHTML = `<i class="fas fa-exclamation-triangle"></i> ${message}`;
    
    const container = document.querySelector('.form-section');
    container.insertBefore(errorDiv, container.firstChild);
    
    // Auto-remove after 5 seconds
    setTimeout(() => errorDiv.remove(), 5000);
}
```

### Network Error Handling

```javascript
async function makeAPICall(url, data) {
    try {
        const response = await fetch(url, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });
        
        if (!response.ok) {
            throw new Error(`HTTP ${response.status}: ${response.statusText}`);
        }
        
        return await response.json();
    } catch (error) {
        console.error('API call failed:', error);
        showError('Network error. Please check your connection and try again.');
        throw error;
    }
}
```

---

## Performance Optimization

### Lazy Loading

```javascript
// Lazy load Google Maps API
function loadGoogleMaps() {
    return new Promise((resolve, reject) => {
        if (window.google && window.google.maps) {
            resolve();
            return;
        }
        
        const script = document.createElement('script');
        script.src = `https://maps.googleapis.com/maps/api/js?key=${API_KEY}&libraries=places&callback=initMap`;
        script.onerror = reject;
        
        window.initMap = resolve;
        document.head.appendChild(script);
    });
}
```

### Debounced Input

```javascript
// Debounce state search input
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Apply to state search
const debouncedSearch = debounce(handleStateSearch, 300);
stateSearchInput.addEventListener('input', debouncedSearch);
```

---

## Accessibility

### ARIA Labels

```html
<!-- Add ARIA labels for screen readers -->
<input type="text" 
       id="origin" 
       name="origin"
       aria-label="Load origin location"
       aria-describedby="origin-help">
<small id="origin-help">Enter the starting city and state</small>
```

### Keyboard Navigation

```javascript
// Ensure keyboard accessibility
function handleKeyboard(event) {
    switch(event.key) {
        case 'Enter':
        case ' ':
            event.target.click();
            break;
        case 'Escape':
            closeModal();
            break;
    }
}

// Apply to interactive elements
document.querySelectorAll('.state-tag .remove-state').forEach(button => {
    button.addEventListener('keydown', handleKeyboard);
});
```

---

## Testing

### Frontend Testing

```javascript
// Test form validation
function testValidation() {
    const testData = {
        origin: '',
        destination: 'Mobile, AL',
        roadType: 'Interstate',
        dimensions: { lengthFt: 0, lengthIn: 0, widthFt: 8, widthIn: 6, heightFt: 13, heightIn: 6, weight: 80000 },
        states: []
    };
    
    const errors = validateFormInputs(testData);
    console.assert(errors.length > 0, 'Should have validation errors');
}

// Test dimension calculations
function testDimensionDisplay() {
    document.getElementById('lengthFt').value = '12';
    document.getElementById('lengthIn').value = '15'; // Should convert to 13'3"
    
    updateDimensionDisplay('length');
    
    setTimeout(() => {
        console.assert(document.getElementById('lengthFt').value === '13', 'Feet should be 13');
        console.assert(document.getElementById('lengthIn').value === '3', 'Inches should be 3');
    }, 100);
}
```

This frontend integration guide provides everything you need to successfully integrate the Load Planning feature's user interface into your Flask application.
