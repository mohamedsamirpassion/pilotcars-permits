"""
Load Planning Routes - Flask Blueprint
=====================================

This module contains all the backend routes needed for the Load Planning feature.
Copy this file to your Flask app's routes folder and register the blueprint.

Features:
- Load planning form page
- Escort requirements calculation API
- User feedback/report submission API
- Email notifications for feedback reports

Dependencies:
- Flask
- Flask-Mail (for email functionality)
- Flask-WTF (for CSRF protection)
- Flask-Login (optional - for user authentication)
"""

from flask import Blueprint, render_template, request, jsonify, current_app
from flask_mail import Message
import json
import os
from datetime import datetime

# Optional imports (remove if not using authentication)
try:
    from flask_login import current_user
    USER_AUTH_AVAILABLE = True
except ImportError:
    USER_AUTH_AVAILABLE = False
    current_user = None

# Create the blueprint
bp = Blueprint('load_planning', __name__, url_prefix='/load-planning')

@bp.route('/')
def load_plan():
    """
    Load planning page for calculating escort requirements.
    
    This route serves the main load planning form and interface.
    No authentication required - public access.
    
    Returns:
        Rendered HTML template with form and map interface
    """
    return render_template('load_plan.html', 
                         title='Load Planning',
                         meta_title='Load Planning - Calculate Escort Requirements',
                         meta_description='Plan your oversized load route and calculate pilot car escort requirements by state.')

@bp.route('/api/calculate-escorts', methods=['POST'])
def calculate_escorts():
    """
    API endpoint to calculate escort requirements based on load specifications.
    
    This endpoint processes the load data and returns escort requirements
    calculated using the state regulations database.
    
    Expected POST data:
    {
        "origin": "Charlotte, NC",
        "destination": "Mobile, AL", 
        "roadType": "Interstate",
        "dimensions": {
            "lengthFt": 75, "lengthIn": 0,
            "widthFt": 8, "widthIn": 6,
            "heightFt": 13, "heightIn": 6,
            "weight": 80000
        },
        "overhang": {
            "frontFt": 0, "frontIn": 0,
            "rearFt": 5, "rearIn": 0
        },
        "states": ["NC", "SC", "GA", "FL", "AL"]
    }
    
    Returns:
        JSON response with calculation results or error message
    """
    try:
        data = request.get_json()
        
        # Validate input data
        if not data:
            return jsonify({'success': False, 'error': 'No data provided'}), 400
        
        # Get load specifications from request
        origin = data.get('origin', '').strip()
        destination = data.get('destination', '').strip()
        road_type = data.get('roadType', 'Interstate')
        dimensions = data.get('dimensions', {})
        overhang = data.get('overhang', {})
        states = data.get('states', [])
        
        # Basic validation
        if not origin or not destination:
            return jsonify({'success': False, 'error': 'Origin and destination are required'}), 400
            
        if not states:
            return jsonify({'success': False, 'error': 'At least one state must be selected'}), 400
        
        # Note: The actual calculation logic would be implemented on the frontend
        # using the state_regulations.js file. This endpoint can be used for
        # additional server-side processing, logging, or database storage.
        
        # Log the calculation request (optional)
        current_app.logger.info(f"Load planning calculation requested: {origin} -> {destination}, States: {states}")
        
        # Return success response (actual calculations done on frontend)
        return jsonify({
            'success': True,
            'message': 'Calculation request received',
            'route_summary': {
                'origin': origin,
                'destination': destination,
                'road_type': road_type,
                'states': states,
                'dimensions': dimensions,
                'overhang': overhang
            }
        })
        
    except Exception as e:
        current_app.logger.error(f"Error in calculate_escorts: {str(e)}")
        return jsonify({'success': False, 'error': 'Internal server error'}), 500

# Import CSRF for exemption (if using Flask-WTF)
try:
    from app import csrf
    CSRF_AVAILABLE = True
except ImportError:
    CSRF_AVAILABLE = False

@bp.route('/api/submit-report', methods=['POST'])
def submit_report():
    """
    API endpoint to handle load planning feedback reports via email.
    
    This endpoint allows users to report issues with regulation data,
    calculation errors, or suggest improvements. Reports are sent via email
    to the admin team.
    
    Expected POST data:
    {
        "issueType": "incorrect_escort",
        "affectedStates": "NC, SC",
        "description": "The escort requirements for NC seem outdated...",
        "reporterEmail": "user@example.com",
        "loadData": {...},
        "timestamp": "2025-09-15T10:30:00Z"
    }
    
    Returns:
        JSON response with success/error status
    """
    # Exempt from CSRF protection if available (for API endpoint)
    if CSRF_AVAILABLE:
        csrf.exempt
    
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'success': False, 'error': 'No data provided'}), 400
        
        # Extract report data
        issue_type = data.get('issueType', 'Unknown')
        affected_states = data.get('affectedStates', 'Not specified')
        description = data.get('description', '').strip()
        reporter_email = data.get('reporterEmail', 'Anonymous')
        load_data = data.get('loadData', {})
        timestamp = data.get('timestamp', datetime.now().isoformat())
        
        # Validate required fields
        if not description:
            return jsonify({'success': False, 'error': 'Description is required'}), 400
        
        # Get user info if authentication is available
        user_info = "Anonymous User"
        if USER_AUTH_AVAILABLE and current_user and current_user.is_authenticated:
            user_info = f"{current_user.email} (ID: {current_user.id})"
        
        # Format load information for email
        load_info = "No load data provided"
        if load_data:
            try:
                load_info = f"""
Origin: {load_data.get('origin', 'Not specified')}
Destination: {load_data.get('destination', 'Not specified')}
Road Type: {load_data.get('roadType', 'Not specified')}
States: {', '.join(load_data.get('customRoute', []))}
Dimensions: {load_data.get('lengthFt', 0)}'{load_data.get('lengthIn', 0)}" L × {load_data.get('widthFt', 0)}'{load_data.get('widthIn', 0)}" W × {load_data.get('heightFt', 0)}'{load_data.get('heightIn', 0)}" H
Weight: {load_data.get('weight', 0)} lbs
                """.strip()
            except Exception:
                load_info = "Load data format error"
        
        # Create email content
        email_subject = f"Load Planning Report: {issue_type}"
        email_body = f"""
A new load planning regulation report has been submitted:

REPORT DETAILS:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Issue Type: {issue_type}
Affected States: {affected_states}
Submitted By: {user_info}
Reporter Contact: {reporter_email}
Timestamp: {timestamp}

DESCRIPTION:
{description}

LOAD INFORMATION:
{load_info}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Please review this report and update the state_regulations.js file if needed.

This report was automatically generated by the Load Planning system.
        """.strip()
        
        # Send email to admin
        try:
            from app import mail
            
            msg = Message(
                subject=email_subject,
                sender=current_app.config['MAIL_DEFAULT_SENDER'],
                recipients=[current_app.config.get('ADMIN_EMAIL', current_app.config['MAIL_DEFAULT_SENDER'])],
                body=email_body
            )
            
            mail.send(msg)
            
            # Log the report submission
            current_app.logger.info(f"Load planning report submitted: {issue_type} for states: {affected_states}")
            
        except Exception as e:
            current_app.logger.error(f"Failed to send report email: {str(e)}")
            return jsonify({
                'success': False, 
                'error': 'Failed to send report. Please try again or contact support directly.'
            }), 500
        
        return jsonify({
            'success': True, 
            'message': 'Report submitted successfully. Thank you for your feedback!'
        })
        
    except Exception as e:
        current_app.logger.error(f"Error in submit_report: {str(e)}")
        return jsonify({
            'success': False, 
            'error': 'Failed to submit report. Please try again or contact support.'
        }), 500

# Optional: Add route for getting state regulations (if you want to serve them via API)
@bp.route('/api/state-regulations')
def get_state_regulations():
    """
    Optional API endpoint to serve state regulations data.
    
    This can be useful if you want to serve the regulations from the backend
    instead of loading them from a static JavaScript file.
    
    Returns:
        JSON response with state regulations data
    """
    try:
        # Load state regulations from JavaScript file
        regulations_path = os.path.join(current_app.static_folder, 'js', 'state_regulations.js')
        
        if not os.path.exists(regulations_path):
            return jsonify({'success': False, 'error': 'Regulations file not found'}), 404
        
        # Note: This would require parsing the JavaScript file to extract the data
        # For now, return a placeholder response
        return jsonify({
            'success': True,
            'message': 'State regulations are served via static JavaScript file',
            'file_path': '/static/js/state_regulations.js'
        })
        
    except Exception as e:
        current_app.logger.error(f"Error serving state regulations: {str(e)}")
        return jsonify({'success': False, 'error': 'Failed to load regulations'}), 500

# Error handlers for the blueprint
@bp.errorhandler(404)
def not_found(error):
    """Handle 404 errors within the load planning blueprint."""
    return jsonify({'success': False, 'error': 'Endpoint not found'}), 404

@bp.errorhandler(500)
def internal_error(error):
    """Handle 500 errors within the load planning blueprint."""
    current_app.logger.error(f"Internal error in load planning: {str(error)}")
    return jsonify({'success': False, 'error': 'Internal server error'}), 500

# Blueprint registration example (add this to your main app file):
"""
from routes.load_planning_routes import bp as load_planning_bp
app.register_blueprint(load_planning_bp)
"""
