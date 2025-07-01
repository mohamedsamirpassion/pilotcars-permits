# My PEVO - Comprehensive Pilot Car Escort Service Platform

A professional web application providing complete pilot car escort services, load planning, customer relationship management, and business operations for trucking companies and pilot car vendors.

## 🌟 Overview

My PEVO is a full-featured business platform designed for the pilot car escort industry. It serves trucking companies, pilot car vendors, and administrative teams with comprehensive tools for:

- **Load Planning & Route Analysis**
- **Pilot Car Service Coordination** 
- **Customer Relationship Management (CRM)**
- **Quote Generation & Management**
- **Vendor Location Sharing**
- **Multi-role User Management**
- **Email Notifications & Communications**

## 🚀 Features

### 👥 User Types & Roles

#### **Trucking Companies**
- Plan routes with escort requirement calculations
- Generate and manage quotes for pilot car services
- Order pilot car services
- View service history and manage profiles
- Access to load planning tools

#### **Pilot Car Vendors**
- Share location and service availability
- Manage service coverage areas
- Receive service requests and notifications
- Update contact information and services offered

#### **Administrative Teams**
**Super Admins:**
- Complete system access and oversight
- User management and role assignment
- System-wide CRM and analytics
- Admin user management
- Email system configuration

**Regular Admins/Lead Dispatchers:**
- CRM lead management and assignment
- Customer quote and order oversight
- Vendor location management
- Performance tracking

**Dispatchers:**
- Load planning assistance
- Vendor location access
- Limited administrative functions

### 🔧 Core Functionality

#### **Load Planning System**
- Interactive route mapping with state-by-state analysis
- Automated escort requirement calculations
- Comprehensive state regulations database
- Custom route planning with dimension analysis
- Save and manage route history

#### **Mini CRM System**
- Automatic lead generation from customer activities
- Lead assignment and status tracking
- Action logging and follow-up management
- Performance metrics and conversion tracking
- Team collaboration tools

#### **Quote Management**
- Real-time quote generation with distance calculation
- Regional pricing with premium/standard rates
- Quote history and customer management
- Automated lead creation from quote requests

#### **Pilot Car Services**
- Service ordering with detailed load information
- Vendor matching and assignment
- Order status tracking and management
- Communication between customers and vendors

#### **Communication & Notifications**
- Email notification system
- In-app notification management
- CRM action tracking
- System alerts and updates

#### **Profile & User Management**
- Comprehensive user profiles with audit logging
- Password management and security
- Role-based access control
- User activity tracking

## 🛠 Technology Stack

- **Backend**: Python 3.10 + Flask 2.3.3
- **Database**: SQLite (development) / PostgreSQL (production ready)
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap 5
- **Mapping**: Leaflet.js with OpenStreetMap
- **Email**: Flask-Mail with SMTP support
- **Authentication**: Session-based with bcrypt password hashing
- **Deployment**: Heroku-ready with Gunicorn

## ⚡ Quick Start

### Prerequisites
- Python 3.10+ (Note: Not compatible with Python 3.13)
- pip (Python package manager)
- SMTP email server (for notifications)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd mypevo
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Environment Setup** (Optional - for email features)
   Create a `.env` file:
   ```env
   MAIL_SERVER=your-smtp-server.com
   MAIL_PORT=587
   MAIL_USE_TLS=True
   MAIL_USERNAME=your-email@domain.com
   MAIL_PASSWORD=your-email-password
   ADMIN_EMAIL=admin@yourdomain.com
   ```

4. **Run the application**
   ```bash
   python app.py
   ```

5. **Access the application**
   - Open browser to: `http://localhost:5000`

## 👤 Getting Started

### Initial Setup
1. **Register** as a trucking company or vendor
2. **Admin Approval** - Contact system administrator for account approval
3. **Profile Setup** - Complete your company profile and contact information
4. **Start Using** - Begin with load planning, quotes, or vendor services

### For Trucking Companies
1. **Plan Routes** - Use the load planning tool to calculate escort requirements
2. **Get Quotes** - Request quotes for pilot car services
3. **Order Services** - Place orders for pilot car escort services
4. **Track History** - Monitor quotes, orders, and route plans

### For Vendors
1. **Share Location** - Register your service area and availability
2. **Update Services** - Specify services offered and coverage radius
3. **Manage Availability** - Keep location information current

### For Administrators
1. **CRM Management** - Assign and track customer leads
2. **User Oversight** - Manage user accounts and permissions
3. **System Monitoring** - Monitor quotes, orders, and vendor activity

## 📊 CRM System Guide

### Lead Management
- **Automatic Lead Creation** - Leads generated from quotes and load plans
- **Lead Assignment** - Assign leads to team members
- **Status Tracking** - Monitor lead progression (Pending → Assigned → In Progress → Converted/Lost)
- **Action Logging** - Track all customer interactions and follow-ups

### Performance Metrics
- **Individual Performance** - Personal conversion rates for each admin
- **Team Overview** - System-wide performance for super admins
- **Revenue Tracking** - Monitor converted lead values

### Follow-up Management
- **Scheduled Follow-ups** - Set and track follow-up dates
- **Overdue Alerts** - Identify missed follow-up opportunities
- **Team Coordination** - Collaborative lead management

## 🗂 File Structure

```
mypevo/
├── app.py                          # Main Flask application
├── admin_roles.py                  # Admin role management utilities
├── requirements.txt                # Python dependencies
├── Procfile                       # Heroku deployment configuration
├── README.md                      # Documentation (this file)
├── templates/                     # HTML templates
│   ├── base.html                 # Base template with navigation
│   ├── index.html                # Landing page
│   ├── login.html & register.html # Authentication
│   ├── dashboard.html            # User dashboard
│   ├── get_quote.html            # Quote request form
│   ├── load_plan.html            # Load planning interface
│   ├── order_pilot_car.html      # Service ordering
│   ├── my_*.html                 # User history pages
│   ├── admin/                    # Admin interface templates
│   │   ├── crm_dashboard.html    # CRM overview
│   │   ├── crm_leads.html        # Lead management
│   │   ├── crm_lead_detail.html  # Individual lead details
│   │   ├── admin_management.html # Admin user management
│   │   └── *.html                # Other admin interfaces
│   ├── vendor/                   # Vendor interface templates
│   ├── profile/                  # Profile management templates
│   └── errors/                   # Error page templates
├── static/                       # Static assets
│   ├── css/style.css            # Custom styles
│   ├── js/state_regulations.js  # State regulations database
│   └── images/                   # Application images
└── Documentation Files:
    ├── EMAIL_SYSTEM_SUMMARY.md     # Email system documentation
    ├── MINI_CRM_SYSTEM.md          # CRM system guide
    ├── NOTIFICATION_SYSTEM.md      # Notification system details
    ├── USER_AUDIT_SYSTEM.md        # User audit documentation
    └── ERROR_PAGES_SUMMARY.md      # Error handling guide
```

## 🔐 Security Features

- **Role-based Access Control** - Granular permissions by user type
- **Password Security** - Bcrypt hashing with salt
- **Session Management** - Secure session handling
- **User Audit Logging** - Complete activity tracking
- **Input Validation** - Protection against common vulnerabilities
- **CSRF Protection** - Built-in Flask security features

## 📧 Email System

### Features
- **Welcome Emails** - New user registration notifications
- **Lead Notifications** - Automated CRM alerts
- **Order Updates** - Service status notifications
- **Admin Alerts** - System and user activity notifications

### Configuration
See `email_setup_production.md` for detailed email system setup instructions.

## 🚀 Deployment

### Heroku Deployment
The application is Heroku-ready with:
- `Procfile` configured for Gunicorn
- Environment variable support
- PostgreSQL database compatibility
- Static file handling

### Production Considerations
- Set up proper SMTP email service
- Configure environment variables
- Use PostgreSQL for production database
- Enable HTTPS/SSL
- Set up backup procedures

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is proprietary software. All rights reserved.

## 📞 Support

For technical support or questions, please contact the development team or system administrator. 