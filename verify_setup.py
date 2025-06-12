#!/usr/bin/env python3
"""
My PEVO Setup Verification Script
This script verifies that all components are correctly installed and configured.
"""

import os
import sys
import json
from pathlib import Path

def check_file_exists(file_path, description):
    """Check if a file exists and print status."""
    if os.path.exists(file_path):
        print(f"✓ {description}: {file_path}")
        return True
    else:
        print(f"✗ {description}: {file_path} - NOT FOUND")
        return False

def check_python_packages():
    """Check if required Python packages are installed."""
    print("\n=== Python Package Check ===")
    packages = ['flask', 'flask_sqlalchemy', 'werkzeug']
    all_good = True
    
    for package in packages:
        try:
            __import__(package)
            print(f"✓ {package} - installed")
        except ImportError:
            print(f"✗ {package} - NOT INSTALLED")
            all_good = False
    
    return all_good

def check_file_structure():
    """Check if all required files and directories exist."""
    print("\n=== File Structure Check ===")
    
    required_files = [
        ('app.py', 'Main Flask application'),
        ('requirements.txt', 'Python dependencies'),
        ('README.md', 'Documentation'),
        ('templates/base.html', 'Base template'),
        ('templates/login.html', 'Login template'),
        ('templates/register.html', 'Register template'),
        ('templates/dashboard.html', 'Dashboard template'),
        ('templates/load_plan.html', 'Load plan template'),
        ('templates/my_routes.html', 'My routes template'),
        ('templates/admin.html', 'Admin template'),
        ('static/css/style.css', 'Main stylesheet'),
        ('static/js/state_regulations.js', 'State regulations data'),
    ]
    
    all_good = True
    for file_path, description in required_files:
        if not check_file_exists(file_path, description):
            all_good = False
    
    return all_good

def check_state_regulations():
    """Check if state regulations file is properly formatted."""
    print("\n=== State Regulations Check ===")
    
    try:
        with open('static/js/state_regulations.js', 'r') as f:
            content = f.read()
            
        # Extract JSON from the JS file
        start = content.find('{')
        end = content.rfind('}') + 1
        
        if start == -1 or end == 0:
            print("✗ State regulations file format is invalid")
            return False
            
        json_data = content[start:end]
        regulations = json.loads(json_data)
        
        # Check if major states are present
        required_states = ['VA', 'NC', 'SC', 'GA', 'AL']
        missing_states = []
        
        for state in required_states:
            if state not in regulations:
                missing_states.append(state)
        
        if missing_states:
            print(f"✗ Missing states in regulations: {', '.join(missing_states)}")
            return False
        
        print(f"✓ State regulations file is valid with {len(regulations)} states")
        return True
        
    except Exception as e:
        print(f"✗ Error reading state regulations: {e}")
        return False

def check_app_configuration():
    """Check basic app configuration."""
    print("\n=== Application Configuration Check ===")
    
    try:
        # Import app without running it
        import app
        
        # Check if the app object exists
        if hasattr(app, 'app'):
            print("✓ Flask app object created successfully")
        else:
            print("✗ Flask app object not found")
            return False
            
        # Check if database models are defined
        if hasattr(app, 'User') and hasattr(app, 'SavedRoute'):
            print("✓ Database models defined")
        else:
            print("✗ Database models not properly defined")
            return False
            
        print("✓ Application configuration looks good")
        return True
        
    except Exception as e:
        print(f"✗ Error importing application: {e}")
        return False

def main():
    """Run all verification checks."""
    print("My PEVO Setup Verification")
    print("=" * 50)
    
    checks = [
        check_python_packages,
        check_file_structure,
        check_state_regulations,
        check_app_configuration
    ]
    
    all_passed = True
    
    for check in checks:
        if not check():
            all_passed = False
    
    print("\n" + "=" * 50)
    
    if all_passed:
        print("🎉 ALL CHECKS PASSED! Your My PEVO application is ready to run.")
        print("\nTo start the application:")
        print("  python app.py")
        print("\nThen open your browser to: http://localhost:5000")
        print("\nDefault admin login:")
        print("  Email: admin@mypevo.com")
        print("  Password: admin123")
    else:
        print("❌ SOME CHECKS FAILED! Please fix the issues above before running the application.")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main()) 