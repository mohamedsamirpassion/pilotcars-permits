# Role-based access control decorators for My PEVO admin system

from functools import wraps
from flask import session, redirect, url_for, flash
from app import User

def admin_or_super_admin_required(f):
    """Allow access to admin and super admin roles only (excludes dispatchers)"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        user = User.query.get(session['user_id'])
        if not user or not user.is_admin or user.admin_role not in ['admin', 'super_admin']:
            flash('Admin access required')
            return redirect(url_for('dashboard'))
        return f(*args, **kwargs)
    return decorated_function

def dispatcher_or_higher_required(f):
    """Allow access to dispatcher, admin, and super admin roles"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        user = User.query.get(session['user_id'])
        if not user or not user.is_admin or user.admin_role not in ['dispatcher', 'admin', 'super_admin']:
            flash('Staff access required')
            return redirect(url_for('dashboard'))
        return f(*args, **kwargs)
    return decorated_function

def dispatcher_or_trucking_company_required(f):
    """Allow access to dispatchers and approved trucking companies for load planning"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        user = User.query.get(session['user_id'])
        
        # Allow trucking companies OR admin staff (dispatcher, admin, super_admin)
        if user and ((user.user_type == 'trucking_company' and user.is_approved) or 
                    (user.is_admin and user.admin_role in ['dispatcher', 'admin', 'super_admin'])):
            return f(*args, **kwargs)
        
        if user and user.user_type == 'trucking_company' and not user.is_approved:
            flash('Your account is pending approval. Please wait for admin approval to access this feature.', 'warning')
            return redirect(url_for('dashboard'))
        
        flash('Access denied. This feature is only available to trucking companies and staff members.', 'error')
        return redirect(url_for('dashboard'))
    
    return decorated_function 