# Customization Guide

This guide explains how to customize the Load Planning feature to match your application's needs, branding, and functionality requirements.

## Overview

The Load Planning feature is designed to be highly customizable. You can modify:
- **Visual appearance** (colors, fonts, layout)
- **Functionality** (form fields, validation rules, calculations)
- **Data sources** (state regulations, additional requirements)
- **Integration** (user authentication, database storage)
- **User experience** (workflow, default values, help text)

---

## Visual Customization

### 1. Brand Colors

The template uses CSS custom properties for easy theming. Update these variables:

```css
/* In templates/load_plan.html or your main CSS file */
:root {
    --brand-primary: #298553;        /* Main brand color */
    --brand-primary-light: #34a866;  /* Lighter shade */
    --brand-primary-dark: #1e6b42;   /* Darker shade */
    --brand-accent: #f8f9fa;         /* Background accent */
    --brand-border: #e8f5e8;         /* Border color */
}
```

**Example - Blue Theme:**
```css
:root {
    --brand-primary: #007bff;
    --brand-primary-light: #3395ff;
    --brand-primary-dark: #0056cc;
    --brand-accent: #f8f9ff;
    --brand-border: #e8f0ff;
}
```

**Example - Red Theme:**
```css
:root {
    --brand-primary: #dc3545;
    --brand-primary-light: #e85b6b;
    --brand-primary-dark: #a71e2a;
    --brand-accent: #fff8f8;
    --brand-border: #ffe8e8;
}
```

### 2. Typography

Customize fonts and text styling:

```css
/* Font family */
.load-plan-container {
    font-family: 'Your-Font', Arial, sans-serif;
}

/* Header styling */
.load-plan-header h1 {
    font-family: 'Your-Header-Font', Georgia, serif;
    font-size: 2.5rem;
    font-weight: 800;
}

/* Form labels */
.form-label {
    font-weight: 600;
    color: var(--brand-primary-dark);
}
```

### 3. Layout Modifications

**Change column layout:**
```html
<!-- Default: 50/50 split -->
<div class="col-lg-6"> <!-- Map --> </div>
<div class="col-lg-6"> <!-- Form --> </div>

<!-- Alternative: 40/60 split favoring form -->
<div class="col-lg-5"> <!-- Map --> </div>
<div class="col-lg-7"> <!-- Form --> </div>

<!-- Alternative: Stacked layout -->
<div class="col-12"> <!-- Map full width --> </div>
<div class="col-12"> <!-- Form full width --> </div>
```

**Adjust section heights:**
```css
.map-section {
    height: 500px; /* Default: 600px */
}

.form-section {
    height: 500px; /* Default: 600px */
    max-height: 80vh; /* Responsive height */
}
```

### 4. Custom Icons

Replace Font Awesome icons with your own:

```html
<!-- Replace Font Awesome icons -->
<h1><i class="your-icon-class"></i>Load Plan Service</h1>

<!-- Or use SVG icons -->
<h1>
    <svg width="24" height="24" viewBox="0 0 24 24">
        <!-- Your SVG path -->
    </svg>
    Load Plan Service
</h1>
```

---

## Functional Customization

### 5. Form Fields

**Add custom fields:**
```html
<!-- Add after existing dimensions -->
<div class="mb-4">
    <h5 class="section-title"><i class="fas fa-truck"></i> Vehicle Information</h5>
    
    <div class="row">
        <div class="col-md-6 mb-3">
            <label for="vehicleType" class="form-label">Vehicle Type</label>
            <select class="form-control" id="vehicleType" name="vehicleType">
                <option value="">Select vehicle type...</option>
                <option value="flatbed">Flatbed</option>
                <option value="lowboy">Lowboy</option>
                <option value="step-deck">Step Deck</option>
            </select>
        </div>
        
        <div class="col-md-6 mb-3">
            <label for="driverExperience" class="form-label">Driver Experience</label>
            <select class="form-control" id="driverExperience" name="driverExperience">
                <option value="">Select experience level...</option>
                <option value="novice">Less than 1 year</option>
                <option value="experienced">1-5 years</option>
                <option value="expert">5+ years</option>
            </select>
        </div>
    </div>
</div>
```

**Update JavaScript to handle new fields:**
```javascript
// In the form submission handler
const formData = {
    // ... existing fields ...
    vehicleInfo: {
        type: document.getElementById('vehicleType')?.value || '',
        driverExperience: document.getElementById('driverExperience')?.value || ''
    }
};
```

**Remove unwanted fields:**
```html
<!-- To remove overhang section, delete this entire block -->
<div class="mb-4">
    <h5 class="section-title"><i class="fas fa-arrows-alt-h"></i> Overhang (Optional)</h5>
    <!-- ... overhang content ... -->
</div>
```

### 6. Validation Rules

**Add custom validation:**
```javascript
function validateFormInputs(formData) {
    const errors = [];
    
    // Existing validation...
    
    // Custom validation rules
    if (formData.vehicleInfo && formData.vehicleInfo.type === 'lowboy' && 
        formData.dimensions.heightFt > 11) {
        errors.push({
            field: 'height',
            message: 'Lowboy trailers cannot handle loads over 11 feet high'
        });
    }
    
    // Business rule validation
    if (formData.dimensions.weight > 80000 && !formData.vehicleInfo.driverExperience === 'expert') {
        errors.push({
            field: 'driverExperience',
            message: 'Loads over 80,000 lbs require an experienced driver'
        });
    }
    
    return errors;
}
```

### 7. Default Values

**Set form defaults:**
```javascript
document.addEventListener('DOMContentLoaded', function() {
    // Set default dimensions for common load
    document.getElementById('lengthFt').value = '75';
    document.getElementById('widthFt').value = '8';
    document.getElementById('heightFt').value = '13';
    document.getElementById('weight').value = '80000';
    
    // Set default road type
    document.getElementById('interstate').checked = true;
    
    // Pre-select common states
    selectState({ name: 'North Carolina', abbr: 'NC' });
    selectState({ name: 'South Carolina', abbr: 'SC' });
});
```

---

## Data Customization

### 8. State Regulations

**Add custom regulations:**
```javascript
// Add to static/js/state_regulations.js
const customRegulations = [
    {
        "state": "Your State",
        "road_type": "Interstate",
        "width_min": "12'1\"",
        "width_max": "14'0\"",
        "width_escorts": "1 Rear",
        "notes": "Your custom requirements"
    }
];

// Merge with existing regulations
const stateRegulations = [...originalRegulations, ...customRegulations];
```

**Modify existing regulations:**
```javascript
// Override specific state regulations
function customizeRegulations() {
    // Find and update specific regulations
    stateRegulations.forEach(reg => {
        if (reg.state === 'California' && reg.road_type === 'Interstate') {
            reg.notes = 'Updated requirements as of 2025';
            reg.width_escorts = '1 Front + 1 Rear'; // Updated requirement
        }
    });
}

// Call after regulations are loaded
customizeRegulations();
```

### 9. Additional Requirements

**Add company-specific requirements:**
```javascript
function processStateRegulations(formData) {
    const results = processStandardRegulations(formData); // Original function
    
    // Add company-specific requirements
    results.forEach(result => {
        // Add insurance requirements
        if (formData.dimensions.weight > 100000) {
            result.additionalRequirements = 'Additional insurance required';
        }
        
        // Add equipment requirements
        if (formData.dimensions.widthFt > 12) {
            result.equipmentRequired = 'Load must have reflective markings';
        }
        
        // Add seasonal restrictions
        const currentMonth = new Date().getMonth();
        if (currentMonth >= 10 || currentMonth <= 2) { // Nov-Feb
            result.seasonalNotes = 'Winter weather restrictions may apply';
        }
    });
    
    return results;
}
```

---

## Integration Customization

### 10. User Authentication

**Require login for calculations:**
```python
# In routes/load_planning_routes.py
from flask_login import login_required, current_user

@bp.route('/api/calculate-escorts', methods=['POST'])
@login_required  # Add this decorator
def calculate_escorts():
    # Log user activity
    user_id = current_user.id
    # ... rest of function
```

**Show different content for authenticated users:**
```html
<!-- In template -->
{% if current_user.is_authenticated %}
    <div class="alert alert-info">
        Welcome back, {{ current_user.name }}! Your calculation history is saved.
    </div>
{% else %}
    <div class="alert alert-warning">
        <a href="/register">Sign up</a> to save your calculations and access premium features.
    </div>
{% endif %}
```

### 11. Database Integration

**Save calculations to database:**
```python
# Add to your models.py
class LoadCalculation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    origin = db.Column(db.String(200))
    destination = db.Column(db.String(200))
    dimensions = db.Column(db.JSON)
    states = db.Column(db.JSON)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# In your route
@bp.route('/api/calculate-escorts', methods=['POST'])
def calculate_escorts():
    data = request.get_json()
    
    # Save calculation
    calculation = LoadCalculation(
        user_id=current_user.id if current_user.is_authenticated else None,
        origin=data.get('origin'),
        destination=data.get('destination'),
        dimensions=data.get('dimensions'),
        states=data.get('states')
    )
    db.session.add(calculation)
    db.session.commit()
    
    # ... rest of function
```

### 12. API Integration

**Connect to external services:**
```python
# Add weather service integration
import requests

def get_weather_conditions(states):
    """Get weather conditions for route states"""
    weather_data = {}
    for state in states:
        try:
            response = requests.get(f'https://api.weather.com/v1/current/conditions?key={WEATHER_API_KEY}&state={state}')
            weather_data[state] = response.json()
        except:
            weather_data[state] = {'conditions': 'Unknown'}
    return weather_data

# Use in calculations
def calculate_escorts_with_weather(formData):
    results = processStateRegulations(formData)
    weather = get_weather_conditions(formData.states)
    
    for result in results:
        state_weather = weather.get(result.state, {})
        if 'snow' in state_weather.get('conditions', '').lower():
            result.weatherNotes = 'Snow conditions - extra caution required'
    
    return results
```

---

## User Experience Customization

### 13. Guided Workflow

**Add step-by-step wizard:**
```html
<!-- Add progress indicator -->
<div class="progress mb-4">
    <div class="progress-bar" id="progressBar" style="width: 25%"></div>
</div>

<!-- Add step navigation -->
<div class="step-navigation mb-4">
    <button class="btn btn-outline-primary" id="prevStep">Previous</button>
    <span class="step-indicator">Step 1 of 4: Trip Information</span>
    <button class="btn btn-primary" id="nextStep">Next</button>
</div>
```

**Implement step logic:**
```javascript
let currentStep = 1;
const totalSteps = 4;

function showStep(step) {
    // Hide all steps
    document.querySelectorAll('.form-step').forEach(s => s.style.display = 'none');
    
    // Show current step
    document.getElementById(`step${step}`).style.display = 'block';
    
    // Update progress
    const progress = (step / totalSteps) * 100;
    document.getElementById('progressBar').style.width = progress + '%';
}

document.getElementById('nextStep').addEventListener('click', function() {
    if (validateCurrentStep()) {
        currentStep = Math.min(currentStep + 1, totalSteps);
        showStep(currentStep);
    }
});
```

### 14. Help and Tooltips

**Add contextual help:**
```html
<!-- Add help tooltips -->
<label for="lengthFt" class="form-label">
    Length
    <i class="fas fa-question-circle" 
       data-bs-toggle="tooltip" 
       title="Total length including tractor and trailer"></i>
</label>

<!-- Add expandable help sections -->
<div class="help-section">
    <button class="btn btn-link" data-bs-toggle="collapse" data-bs-target="#dimensionHelp">
        <i class="fas fa-question-circle"></i> Need help with dimensions?
    </button>
    <div class="collapse" id="dimensionHelp">
        <div class="card card-body">
            <p>Measure the total dimensions including:</p>
            <ul>
                <li>Tractor + trailer + load</li>
                <li>Any overhanging equipment</li>
                <li>Height from ground to highest point</li>
            </ul>
        </div>
    </div>
</div>
```

### 15. Saved Templates

**Add load templates:**
```javascript
const loadTemplates = {
    'wind-turbine-blade': {
        name: 'Wind Turbine Blade',
        dimensions: { lengthFt: 180, lengthIn: 0, widthFt: 12, widthIn: 0, heightFt: 15, heightIn: 0, weight: 25000 },
        roadType: 'Interstate'
    },
    'mobile-home': {
        name: 'Mobile Home',
        dimensions: { lengthFt: 76, lengthIn: 0, widthFt: 16, widthIn: 0, heightFt: 13, heightIn: 6, weight: 80000 },
        roadType: 'Non-Interstate'
    }
};

// Add template selector
function addTemplateSelector() {
    const html = `
        <div class="mb-3">
            <label class="form-label">Load Templates</label>
            <select class="form-control" id="loadTemplate" onchange="applyTemplate()">
                <option value="">Custom Load</option>
                ${Object.entries(loadTemplates).map(([key, template]) => 
                    `<option value="${key}">${template.name}</option>`
                ).join('')}
            </select>
        </div>
    `;
    
    document.querySelector('.form-section').insertAdjacentHTML('afterbegin', html);
}

function applyTemplate() {
    const templateKey = document.getElementById('loadTemplate').value;
    if (!templateKey) return;
    
    const template = loadTemplates[templateKey];
    
    // Apply template values
    Object.entries(template.dimensions).forEach(([key, value]) => {
        const input = document.getElementById(key);
        if (input) input.value = value;
    });
    
    // Update road type
    document.querySelector(`input[value="${template.roadType}"]`).checked = true;
    
    // Update dimension displays
    updateDimensionDisplay('length');
    updateDimensionDisplay('width');
    updateDimensionDisplay('height');
}
```

---

## Advanced Customization

### 16. Custom Calculations

**Override calculation logic:**
```javascript
// Custom calculation function
function customProcessStateRegulations(formData) {
    // Start with standard calculations
    let results = processStateRegulations(formData);
    
    // Apply custom business rules
    results = results.map(result => {
        // Add time-of-day restrictions
        const currentHour = new Date().getHours();
        if (currentHour >= 6 && currentHour <= 18) {
            result.timeRestrictions = 'Daylight hours only';
        } else {
            result.timeRestrictions = 'Night travel permitted';
        }
        
        // Add distance-based requirements
        const totalDistance = calculateRouteDistance(formData.origin, formData.destination);
        if (totalDistance > 500) {
            result.longHaulNotes = 'Long haul - additional rest stops required';
        }
        
        // Add cost estimates
        result.estimatedCost = calculateEscortCost(result.escortRequirements, totalDistance);
        
        return result;
    });
    
    return results;
}

// Use custom function instead of standard one
function calculateEscortRequirements(formData) {
    // ... loading state code ...
    
    setTimeout(() => {
        try {
            const results = customProcessStateRegulations(formData); // Use custom function
            showResults(formData, results);
        } catch (error) {
            console.error('Error calculating escort requirements:', error);
            alert('Error calculating requirements. Please check your inputs and try again.');
        }
        
        // ... reset button code ...
    }, 500);
}
```

### 17. Export Capabilities

**Add PDF export:**
```javascript
// Add jsPDF library
// <script src="https://cdnjs.cloudflare.com/ajax/libs/jspdf/2.5.1/jspdf.umd.min.js"></script>

function exportToPDF() {
    const { jsPDF } = window.jspdf;
    const doc = new jsPDF();
    
    // Add title
    doc.setFontSize(20);
    doc.text('Load Planning Report', 20, 30);
    
    // Add route summary
    doc.setFontSize(12);
    doc.text(`Origin: ${lastCalculatedLoad.origin}`, 20, 50);
    doc.text(`Destination: ${lastCalculatedLoad.destination}`, 20, 60);
    
    // Add table data
    let yPosition = 80;
    lastCalculatedResults.forEach(result => {
        doc.text(`${result.state}: ${result.escortRequirements}`, 20, yPosition);
        yPosition += 10;
    });
    
    // Save PDF
    doc.save('load-planning-report.pdf');
}

// Add export button
function addExportButton() {
    const exportButton = `
        <button class="btn btn-success" onclick="exportToPDF()">
            <i class="fas fa-file-pdf"></i> Export to PDF
        </button>
    `;
    
    document.querySelector('.results-actions').insertAdjacentHTML('beforeend', exportButton);
}
```

---

## Mobile Customization

### 18. Mobile-Specific Features

**Add mobile-optimized interface:**
```css
@media (max-width: 768px) {
    /* Larger touch targets */
    .state-tag {
        min-height: 44px;
        font-size: 16px;
    }
    
    /* Simplified layout */
    .dimension-input-group {
        flex-direction: column;
        gap: 10px;
    }
    
    /* Full-width buttons */
    .btn {
        width: 100%;
        margin-bottom: 10px;
    }
    
    /* Sticky form sections */
    .form-section {
        position: sticky;
        top: 10px;
        z-index: 100;
    }
}
```

**Add touch gestures:**
```javascript
// Add swipe gestures for mobile
function addTouchGestures() {
    let startX, startY;
    
    document.addEventListener('touchstart', e => {
        startX = e.touches[0].clientX;
        startY = e.touches[0].clientY;
    });
    
    document.addEventListener('touchend', e => {
        const endX = e.changedTouches[0].clientX;
        const endY = e.changedTouches[0].clientY;
        
        const deltaX = endX - startX;
        const deltaY = endY - startY;
        
        // Swipe left/right to navigate between form sections
        if (Math.abs(deltaX) > Math.abs(deltaY) && Math.abs(deltaX) > 50) {
            if (deltaX > 0) {
                // Swipe right - previous section
                navigateSection('prev');
            } else {
                // Swipe left - next section
                navigateSection('next');
            }
        }
    });
}
```

This customization guide provides comprehensive options for adapting the Load Planning feature to your specific needs. You can implement any combination of these customizations to create a unique experience that matches your application's requirements.
