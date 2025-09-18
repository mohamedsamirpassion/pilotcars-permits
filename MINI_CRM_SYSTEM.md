# Mini CRM System - Pilot Cars & Permits

## Overview

The Mini CRM (Customer Relationship Management) system is designed to help Pilot Cars & Permits admins track and convert leads generated from free services into paying customers for pilot car services.

## Business Logic

### Lead Generation Flow
1. **Free Service Usage** → **Lead Creation**
   - When trucking companies use load planning or get quotes
   - System automatically creates sales leads
   - Multiple activities within 30-60 minutes are combined into one lead

2. **Lead Assignment** → **Sales Process**
   - Admins manually assign leads to themselves (first-come-first-serve)
   - Super admins can assign leads to any admin
   - Leads never expire automatically

3. **Sales Actions** → **Conversion Tracking**
   - Admins track calls, emails, meetings with prospects
   - Record outcomes and schedule follow-ups
   - Mark leads as converted or lost

## Database Schema

### SalesLead Table
- `id`: Primary key
- `company_id`: Reference to User (trucking company)
- `lead_source`: Source of lead ('load_plan', 'quote', 'location_share', 'order_attempt')
- `lead_data`: JSON data with service details
- `estimated_value`: Potential revenue
- `status`: 'pending', 'assigned', 'in_progress', 'converted', 'lost'
- `assigned_admin_id`: Admin responsible for this lead
- `assigned_at`: When lead was assigned
- `created_at`, `updated_at`: Timestamps

### SalesAction Table
- `id`: Primary key
- `lead_id`: Reference to SalesLead
- `admin_id`: Admin who took the action
- `action_type`: 'call', 'email', 'text', 'meeting'
- `action_description`: Brief description
- `outcome`: 'answered', 'voicemail', 'no_answer', 'interested', 'not_interested'
- `notes`: Detailed notes
- `follow_up_date`: When to follow up next
- `created_at`: Timestamp

### SalesConversion Table
- `id`: Primary key
- `lead_id`: Reference to SalesLead
- `order_id`: Reference to PilotCarOrder (if applicable)
- `conversion_value`: Actual revenue generated
- `conversion_type`: 'order_placed', 'manual_mark', 'registration'
- `admin_id`: Admin who converted the lead
- `notes`: Conversion details
- `created_at`: Timestamp

## Features

### 1. Automatic Lead Generation
- **Load Planning Service**: Creates leads when companies save routes
- **Quote Service**: Creates leads when companies request quotes
- **Activity Consolidation**: Multiple activities within 30-60 minutes = 1 lead

### 2. Lead Management Dashboard
- **Pending Leads**: Available leads for assignment
- **My Active Leads**: Leads assigned to current admin
- **Performance Metrics**: Conversion rates and revenue tracking
- **Team Performance**: Super admin view of all admin performance

### 3. Lead Assignment System
- **Manual Assignment**: Admins assign leads to themselves
- **Super Admin Assignment**: Can assign to any admin
- **First-Come-First-Serve**: No automatic assignments

### 4. Sales Action Tracking
- **Action Types**: Call, Email, Text, Meeting
- **Outcomes**: Answered, Voicemail, No Answer, Interested, Not Interested
- **Follow-up Scheduling**: Set dates for next contact
- **Detailed Notes**: Track conversation details

### 5. Conversion Management
- **Mark as Converted**: Record successful sales
- **Conversion Value**: Track actual revenue
- **Mark as Lost**: Record unsuccessful leads with reasons
- **Performance Analytics**: Calculate conversion rates

## User Interface

### Admin CRM Dashboard (`/admin/crm`)
- Performance overview cards
- Quick actions
- Recent pending leads table
- Active leads table
- Team performance (super admin only)

### All Leads Page (`/admin/crm/leads`)
- Filterable leads table
- Search by company name
- Filter by status, assigned admin
- Bulk actions

### Lead Detail Page (`/admin/crm/lead/<id>`)
- Complete lead information
- Service details from original activity
- Action history
- Quick action buttons
- Add new actions

## Integration Points

### Automatic Lead Creation
```python
# In save-route function
create_sales_lead(session['user_id'], 'load_plan', lead_data, estimated_value=500.0)

# In calculate-quote function
create_sales_lead(session['user_id'], 'quote', lead_data, estimated_value=result['total_cost'])
```

### Navigation Integration
- Added "Mini CRM" link to admin dropdown menu
- Accessible from `/admin/crm`

## Performance Metrics

### Individual Admin Metrics
- **Total Leads**: Number of leads assigned
- **Conversions**: Number of successful conversions
- **Conversion Rate**: Percentage of leads converted
- **Total Value**: Revenue generated
- **Average Value**: Revenue per conversion

### Team Performance
- Comparative view of all admin performance
- Ranking by conversion rate
- Total team revenue tracking

## API Endpoints

### Lead Management
- `GET /admin/crm` - CRM dashboard
- `GET /admin/crm/leads` - All leads with filtering
- `GET /admin/crm/lead/<id>` - Lead details
- `POST /admin/crm/assign-lead/<id>` - Assign lead to admin
- `POST /admin/crm/add-action/<id>` - Add sales action
- `POST /admin/crm/convert-lead/<id>` - Mark as converted
- `POST /admin/crm/lost-lead/<id>` - Mark as lost

## Security & Permissions

### Access Control
- **Admin Required**: All CRM routes require admin login
- **Lead Assignment**: Only pending leads can be assigned
- **Action Permissions**: Only assigned admin or super admin can add actions
- **Conversion Rights**: Only assigned admin or super admin can convert/mark lost

### Data Privacy
- Lead data contains only business information
- No personal customer data stored beyond what's already in the system
- Links to existing user records for complete information

## Installation & Setup

### 1. Database Migration
```bash
python create_crm_tables.py
```

### 2. Test System
```bash
python test_crm_system.py
```

### 3. Verification
- Login as admin
- Navigate to Admin Panel → Mini CRM
- Verify dashboard loads correctly

## Usage Examples

### Example Admin Workflow
1. **Check Dashboard**: See pending leads and performance
2. **Assign Lead**: Click "Assign to Me" on pending lead
3. **Contact Customer**: Use phone/email links
4. **Record Action**: Add call/email with outcome
5. **Follow Up**: Set follow-up date for next contact
6. **Convert**: Mark as converted when customer orders service

### Example Performance Review
- Super admin reviews team performance monthly
- Identifies top-performing admins
- Reassigns leads if needed
- Tracks revenue attribution

## Lead Sources Explained

### Load Plan
- Customer saves a route using the load planning tool
- Estimated value: $500 (typical pilot car service cost)
- Data includes: route details, load dimensions, road types

### Quote
- Customer requests a quote for pilot car services
- Estimated value: Quote total cost
- Data includes: pickup/delivery locations, dates, car types

### Location Share (Future)
- When customers request pilot locations
- Shows interest in booking services
- Estimated value: Based on historical data

### Order Attempt (Future)
- Customer starts but doesn't complete order process
- High-value lead requiring immediate follow-up
- Estimated value: Based on order details

## Reporting & Analytics

### Available Metrics
- Leads by source (load plan, quote, etc.)
- Conversion rates by admin
- Revenue attribution
- Time to conversion
- Follow-up effectiveness

### Future Enhancements
- Lead scoring based on activity patterns
- Automated follow-up reminders
- Integration with email systems
- Advanced reporting dashboard

## Support & Troubleshooting

### Common Issues
1. **CRM not showing in admin menu**: Check admin permissions
2. **Leads not generating**: Verify integration in save-route/quote functions
3. **Performance not calculating**: Check date ranges and lead assignments

### Database Maintenance
- Leads are never automatically deleted
- Historical data preserved for reporting
- Regular backups recommended

## Technical Notes

### Lead Consolidation Logic
```python
# Check for recent lead from same company (within 60 minutes)
cutoff_time = datetime.utcnow() - timedelta(minutes=60)
existing_lead = SalesLead.query.filter(
    SalesLead.company_id == user_id,
    SalesLead.created_at >= cutoff_time,
    SalesLead.status.in_(['pending', 'assigned'])
).first()
```

### Performance Calculation
```python
# Calculate conversion rate for admin
total_leads = SalesLead.query.filter_by(assigned_admin_id=admin_id).count()
conversions = SalesConversion.query.join(SalesLead).filter(
    SalesLead.assigned_admin_id == admin_id
).count()
conversion_rate = (conversions / total_leads * 100) if total_leads > 0 else 0
```

This CRM system provides My PEVO with a comprehensive tool to track, manage, and convert leads generated from their free services into paying customers, ultimately increasing revenue and improving sales team performance.