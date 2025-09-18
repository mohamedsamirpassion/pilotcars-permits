# API Endpoints Documentation

This document describes all the API endpoints needed for the Load Planning feature.

## Overview

The Load Planning feature provides the following API endpoints:

1. **Main Page Route** - Serves the load planning interface
2. **Calculation API** - Processes escort requirement calculations  
3. **Report Submission API** - Handles user feedback reports
4. **State Regulations API** (Optional) - Serves regulation data

## Base URL

All endpoints are prefixed with `/load-planning` (configurable in the blueprint registration).

---

## 1. Load Planning Page

**Endpoint:** `GET /load-planning/`

**Description:** Serves the main load planning HTML page with form and map interface.

**Authentication:** None (public access)

**Response:** HTML page

**Example:**
```bash
GET https://yourdomain.com/load-planning/
```

**Response:**
```html
<!DOCTYPE html>
<html>
<!-- Load planning page with form, map, and results sections -->
</html>
```

---

## 2. Calculate Escorts

**Endpoint:** `POST /load-planning/api/calculate-escorts`

**Description:** API endpoint to calculate escort requirements based on load specifications. Currently returns success confirmation; actual calculations are performed on the frontend using JavaScript.

**Authentication:** None (but can be modified to require login)

**Content-Type:** `application/json`

**Request Body:**
```json
{
  "origin": "Charlotte, NC",
  "destination": "Mobile, AL",
  "roadType": "Interstate",
  "dimensions": {
    "lengthFt": 75,
    "lengthIn": 0,
    "widthFt": 8,
    "widthIn": 6,
    "heightFt": 13,
    "heightIn": 6,
    "weight": 80000
  },
  "overhang": {
    "frontFt": 0,
    "frontIn": 0,
    "rearFt": 5,
    "rearIn": 0
  },
  "states": ["NC", "SC", "GA", "FL", "AL"]
}
```

**Request Parameters:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `origin` | string | Yes | Origin city, state, or address |
| `destination` | string | Yes | Destination city, state, or address |
| `roadType` | string | Yes | "Interstate" or "Non-Interstate" |
| `dimensions` | object | Yes | Load dimensions in feet and inches |
| `dimensions.lengthFt` | integer | Yes | Length in feet |
| `dimensions.lengthIn` | integer | Yes | Length in inches (0-11) |
| `dimensions.widthFt` | integer | Yes | Width in feet |
| `dimensions.widthIn` | integer | Yes | Width in inches (0-11) |
| `dimensions.heightFt` | integer | Yes | Height in feet |
| `dimensions.heightIn` | integer | Yes | Height in inches (0-11) |
| `dimensions.weight` | integer | Yes | Weight in pounds |
| `overhang` | object | No | Overhang dimensions |
| `overhang.frontFt` | integer | No | Front overhang in feet |
| `overhang.frontIn` | integer | No | Front overhang in inches |
| `overhang.rearFt` | integer | No | Rear overhang in feet |
| `overhang.rearIn` | integer | No | Rear overhang in inches |
| `states` | array | Yes | Array of state abbreviations (e.g., ["NC", "SC"]) |

**Success Response (200):**
```json
{
  "success": true,
  "message": "Calculation request received",
  "route_summary": {
    "origin": "Charlotte, NC",
    "destination": "Mobile, AL",
    "road_type": "Interstate",
    "states": ["NC", "SC", "GA", "FL", "AL"],
    "dimensions": {
      "lengthFt": 75,
      "lengthIn": 0,
      "widthFt": 8,
      "widthIn": 6,
      "heightFt": 13,
      "heightIn": 6,
      "weight": 80000
    },
    "overhang": {
      "frontFt": 0,
      "frontIn": 0,
      "rearFt": 5,
      "rearIn": 0
    }
  }
}
```

**Error Response (400):**
```json
{
  "success": false,
  "error": "Origin and destination are required"
}
```

**Error Response (500):**
```json
{
  "success": false,
  "error": "Internal server error"
}
```

---

## 3. Submit Report

**Endpoint:** `POST /load-planning/api/submit-report`

**Description:** Handles user feedback reports about regulation accuracy or calculation errors. Sends email notifications to administrators.

**Authentication:** None (but user info is included if authenticated)

**Content-Type:** `application/json`

**CSRF Protection:** Exempt (API endpoint)

**Request Body:**
```json
{
  "issueType": "incorrect_escort",
  "affectedStates": "NC, SC",
  "description": "The escort requirements for NC seem outdated. According to the state website, the requirements have changed.",
  "reporterEmail": "user@example.com",
  "loadData": {
    "origin": "Charlotte, NC",
    "destination": "Columbia, SC",
    "roadType": "Interstate",
    "customRoute": ["NC", "SC"],
    "lengthFt": "75",
    "lengthIn": "0",
    "widthFt": "8",
    "widthIn": "6",
    "heightFt": "13",
    "heightIn": "6",
    "weight": "80000"
  },
  "timestamp": "2025-09-15T10:30:00Z"
}
```

**Request Parameters:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `issueType` | string | Yes | Type of issue: "incorrect_escort", "missing_state", "outdated_rule", "calculation_error", "other" |
| `affectedStates` | string | No | Comma-separated list of affected state abbreviations |
| `description` | string | Yes | Detailed description of the issue |
| `reporterEmail` | string | No | Contact email for follow-up |
| `loadData` | object | No | Load information for context |
| `timestamp` | string | No | ISO timestamp of when report was created |

**Success Response (200):**
```json
{
  "success": true,
  "message": "Report submitted successfully. Thank you for your feedback!"
}
```

**Error Response (400):**
```json
{
  "success": false,
  "error": "Description is required"
}
```

**Error Response (500):**
```json
{
  "success": false,
  "error": "Failed to submit report. Please try again or contact support."
}
```

---

## 4. State Regulations (Optional)

**Endpoint:** `GET /load-planning/api/state-regulations`

**Description:** Optional endpoint to serve state regulations data via API instead of static JavaScript file.

**Authentication:** None

**Success Response (200):**
```json
{
  "success": true,
  "message": "State regulations are served via static JavaScript file",
  "file_path": "/static/js/state_regulations.js"
}
```

**Note:** This endpoint is currently a placeholder. To fully implement it, you would need to parse the JavaScript file and return the regulation data as JSON.

---

## Error Handling

All endpoints implement consistent error handling:

### HTTP Status Codes

- **200 OK** - Request successful
- **400 Bad Request** - Invalid input data or missing required fields
- **404 Not Found** - Endpoint not found
- **500 Internal Server Error** - Server-side error

### Error Response Format

All error responses follow this format:
```json
{
  "success": false,
  "error": "Human-readable error message"
}
```

---

## Rate Limiting

Consider implementing rate limiting for production use:

```python
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

@bp.route('/api/calculate-escorts', methods=['POST'])
@limiter.limit("10 per minute")
def calculate_escorts():
    # ... implementation
```

---

## CORS Configuration

If serving the API from a different domain than your frontend:

```python
from flask_cors import CORS

# Enable CORS for the blueprint
CORS(bp, origins=['https://yourdomain.com'])
```

---

## Authentication Integration

To require authentication for certain endpoints:

```python
from flask_login import login_required, current_user

@bp.route('/api/calculate-escorts', methods=['POST'])
@login_required
def calculate_escorts():
    # Only authenticated users can access
    user_id = current_user.id
    # ... implementation
```

---

## Example Integration

### JavaScript Example

```javascript
// Calculate escort requirements
async function submitCalculation(formData) {
    try {
        const response = await fetch('/load-planning/api/calculate-escorts', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(formData)
        });
        
        const result = await response.json();
        
        if (result.success) {
            console.log('Calculation logged:', result.route_summary);
        } else {
            console.error('Calculation failed:', result.error);
        }
    } catch (error) {
        console.error('Network error:', error);
    }
}

// Submit feedback report
async function submitReport(reportData) {
    try {
        const response = await fetch('/load-planning/api/submit-report', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(reportData)
        });
        
        const result = await response.json();
        
        if (result.success) {
            alert(result.message);
        } else {
            alert('Error: ' + result.error);
        }
    } catch (error) {
        alert('Failed to submit report. Please try again.');
    }
}
```

### Python Example

```python
import requests

# Calculate escorts
response = requests.post('https://yourdomain.com/load-planning/api/calculate-escorts', 
    json={
        'origin': 'Charlotte, NC',
        'destination': 'Mobile, AL',
        'roadType': 'Interstate',
        'dimensions': {
            'lengthFt': 75, 'lengthIn': 0,
            'widthFt': 8, 'widthIn': 6,
            'heightFt': 13, 'heightIn': 6,
            'weight': 80000
        },
        'overhang': {
            'frontFt': 0, 'frontIn': 0,
            'rearFt': 5, 'rearIn': 0
        },
        'states': ['NC', 'SC', 'GA', 'FL', 'AL']
    })

if response.status_code == 200:
    result = response.json()
    print(f"Success: {result['message']}")
else:
    print(f"Error: {response.status_code}")
```

---

## Testing

### Unit Tests Example

```python
import unittest
from your_app import app

class LoadPlanningAPITestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_calculate_escorts_success(self):
        response = self.app.post('/load-planning/api/calculate-escorts',
            json={
                'origin': 'Charlotte, NC',
                'destination': 'Mobile, AL',
                'roadType': 'Interstate',
                'dimensions': {
                    'lengthFt': 75, 'lengthIn': 0,
                    'widthFt': 8, 'widthIn': 6,
                    'heightFt': 13, 'heightIn': 6,
                    'weight': 80000
                },
                'states': ['NC', 'SC']
            })
        
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertTrue(data['success'])

    def test_calculate_escorts_missing_data(self):
        response = self.app.post('/load-planning/api/calculate-escorts',
            json={})
        
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertFalse(data['success'])
```

This API documentation provides a complete reference for integrating with the Load Planning feature endpoints.
