# User Audit Trail & History System

## Overview

The My PEVO application now includes a comprehensive user audit trail and activity tracking system that allows administrators to view detailed user histories and track changes.

## Features

### 1. User Change History
- **Profile Updates**: Tracks changes to user profile information (company name, contact name, email, phone, DOT number)
- **Admin Actions**: Records when admins approve, suspend, or unsuspend users
- **Password Changes**: Logs password changes (without storing actual passwords)
- **Login Activity**: Tracks user login attempts with IP addresses and timestamps

### 2. Activity Statistics
- **For Pilots (Vendors)**:
  - Total location shares
  - Active location shares
  - Location sharing history with coverage areas and expiration dates
  - Last location shared timestamp

- **For Trucking Companies**:
  - Total quotes generated
  - Total pilot car orders placed
  - Saved routes count
  - Recent quote and order history

### 3. Admin View Features
- **Comprehensive User Details Modal**: Accessible from the "View" button in user management
- **Tabbed Interface** with sections for:
  - Account Information
  - Activity Statistics
  - Change History
  - Login History
  - Location History (for pilots)
  - Recent Activity (for trucking companies)

## How to Access

### For Admins:
1. Navigate to **Admin Dashboard** → **Manage Users**
2. Find the user you want to view
3. Click the **"View"** button next to their name
4. Browse through the different tabs to see:
   - **Change History**: All profile changes and admin actions
   - **Login History**: Recent logins with IP addresses
   - **Location History**: (Pilots only) Location sharing activity
   - **Recent Activity**: (Trucking Companies only) Quotes and orders

## Data Tracked

### Audit Log Fields:
- **Action Type**: login, profile_update, status_change, password_change, location_share
- **Description**: Human-readable description of the action
- **Field Changed**: Specific field that was modified
- **Old/New Values**: Before and after values for changes
- **Admin Actions**: Whether the change was made by an admin
- **IP Address**: Client IP where the action originated
- **Timestamp**: When the action occurred
- **Time Ago**: Human-friendly relative time display

### Activity Statistics:
- **Login Count**: Total number of logins
- **Last Login**: Most recent login timestamp
- **Account Age**: Days since account creation
- **User-Type Specific Metrics**: Different stats for pilots vs trucking companies

## Security & Privacy

- **Password Security**: Password changes are logged but actual passwords are never stored in audit logs
- **IP Tracking**: Client IP addresses are recorded for security auditing
- **Admin Attribution**: All admin actions are attributed to the specific admin who performed them
- **Data Retention**: Audit logs are kept for historical tracking (currently no automatic purging)

## Technical Implementation

### Database Schema:
```sql
user_audit_log (
    id: Primary key
    user_id: Foreign key to user
    action_type: Type of action performed
    action_description: Human readable description
    field_changed: Specific field modified
    old_value: Previous value
    new_value: New value
    changed_by_admin: Boolean flag
    admin_user_id: Foreign key to admin user
    ip_address: Client IP address
    user_agent: Browser/client information
    created_at: Timestamp
)
```

### Key Functions:
- `create_audit_log()`: Creates new audit entries
- `get_user_details()`: API endpoint for comprehensive user data
- `viewUserDetails()`: JavaScript function for modal display

## Usage Examples

### Viewing User Changes:
1. Admin sees a user's email was changed
2. Audit log shows: "Profile updated: email changed from 'old@email.com' to 'new@email.com'"
3. Timestamp and IP address are recorded
4. If admin made the change, admin's name is recorded

### Tracking Pilot Activity:
1. Admin views pilot user details
2. Location History tab shows all location shares
3. Statistics show total locations shared vs currently active
4. Each location entry shows coverage radius and expiration status

### Monitoring Login Activity:
1. Admin can see user's login patterns
2. Multiple IP addresses might indicate account sharing
3. Long periods without login might indicate inactive users
4. Successful login attempts are recorded (failed attempts are not currently tracked)

## Benefits

- **Accountability**: All user and admin actions are tracked
- **Troubleshooting**: Easier to diagnose user issues
- **Security**: Monitor for suspicious activity
- **Insights**: Understand user engagement patterns
- **Compliance**: Maintain audit trails for business requirements

## Future Enhancements

Potential improvements could include:
- Failed login attempt tracking
- Automatic audit log archiving/purging
- Email notifications for suspicious activity
- Export functionality for audit reports
- Advanced filtering and search within audit logs 