# Email Setup Guide for My PEVO Production Deployment

## Overview
The My PEVO application includes a professional email notification system that handles critical business communications. This guide will help you configure email services for production deployment.

## Current Email Features

### Critical Email Notifications:
1. **🚨 Admin Notifications (URGENT)**
   - New pilot car orders (immediate notification)
   - Professional HTML templates with branding
   - Automatic admin distribution

2. **⏰ Pilot Location Expiry Warnings**
   - 48-hour location share reminders
   - Professional branded emails
   - Call-to-action buttons

## Production Email Service Options

### Option 1: Amazon SES (Recommended)
**Best for: Production deployments, high reliability, cost-effective**

**Setup Steps:**
```bash
# 1. Install AWS CLI and configure
pip install boto3

# 2. Set environment variables in production
export MAIL_SERVER="email-smtp.us-east-1.amazonaws.com"
export MAIL_PORT="587"
export MAIL_USE_TLS="true"
export MAIL_USERNAME="your-ses-smtp-username"
export MAIL_PASSWORD="your-ses-smtp-password"
export MAIL_DEFAULT_SENDER="noreply@yourdomain.com"
export MAIL_ADMIN_EMAIL="dispatch@yourdomain.com"
export FLASK_ENV="production"
```

**AWS SES Configuration:**
1. Verify your domain in AWS SES console
2. Create SMTP credentials
3. Move out of sandbox mode for production
4. Set up SPF/DKIM records for deliverability

### Option 2: SendGrid
**Best for: Easy setup, good deliverability**

```bash
# Environment variables for SendGrid
export MAIL_SERVER="smtp.sendgrid.net"
export MAIL_PORT="587"
export MAIL_USE_TLS="true"
export MAIL_USERNAME="apikey"
export MAIL_PASSWORD="your-sendgrid-api-key"
export MAIL_DEFAULT_SENDER="noreply@yourdomain.com"
export MAIL_ADMIN_EMAIL="dispatch@yourdomain.com"
export FLASK_ENV="production"
```

### Option 3: Gmail SMTP (Development/Small Scale)
**Best for: Testing, small-scale deployments**

```bash
# Environment variables for Gmail
export MAIL_SERVER="smtp.gmail.com"
export MAIL_PORT="587"
export MAIL_USE_TLS="true"
export MAIL_USERNAME="your-gmail@gmail.com"
export MAIL_PASSWORD="your-app-password"
export MAIL_DEFAULT_SENDER="your-gmail@gmail.com"
export MAIL_ADMIN_EMAIL="dispatch@yourdomain.com"
export FLASK_ENV="production"
```

## Local Development vs Production

### Local Development (Current Setup)
- Emails are printed to console with professional formatting
- No actual emails sent
- All templates work and can be tested
- Perfect for development and testing

### Production Deployment
- Real emails sent via configured SMTP service
- Automatic environment detection
- Fallback to console logging if email fails
- Professional HTML and text templates

## Environment Variables Reference

| Variable | Purpose | Example |
|----------|---------|---------|
| `MAIL_SERVER` | SMTP server hostname | `email-smtp.us-east-1.amazonaws.com` |
| `MAIL_PORT` | SMTP server port | `587` |
| `MAIL_USE_TLS` | Enable TLS encryption | `true` |
| `MAIL_USERNAME` | SMTP username | `AKIAIOSFODNN7EXAMPLE` |
| `MAIL_PASSWORD` | SMTP password/API key | `wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY` |
| `MAIL_DEFAULT_SENDER` | From email address | `noreply@mypevo.com` |
| `MAIL_ADMIN_EMAIL` | Admin notifications email | `dispatch@mypevo.com` |
| `FLASK_ENV` | Application environment | `production` |

## Testing Email Configuration

### 1. Test Email Sending Function
```python
# Add this to your Python console for testing
from app import EmailService

# Test basic email functionality
result = EmailService.send_email_notification(
    "test@example.com",
    "location_expired",
    {
        'pilot_name': 'Test Pilot',
        'location_city': 'Atlanta',
        'location_state': 'GA',
        'share_location_url': 'https://yourdomain.com/vendor/share-location'
    }
)
print(f"Email test result: {result}")
```

### 2. Test Critical Admin Notification
```python
# Test critical admin notification
result = EmailService.send_email_notification(
    "admin@yourdomain.com",
    "admin_new_order_critical",
    {
        'company_name': 'Test Company',
        'order_id': '123',
        'pickup_date': 'January 15, 2024',
        'pickup_address': '123 Main St, Atlanta, GA',
        'delivery_address': '456 Oak Ave, Birmingham, AL',
        'contact_name': 'John Doe',
        'phone_number': '(555) 123-4567',
        'driver_name': 'Mike Smith',
        'driver_phone': '(555) 987-6543',
        'length': '53 ft',
        'width': '12 ft',
        'height': '13.5 ft',
        'weight': '80,000 lbs',
        'pilot_positions': 'Front Escort, Rear Escort',
        'load_description': 'Oversized construction equipment',
        'order_detail_url': 'https://yourdomain.com/admin/order/123'
    }
)
```

## Email Templates Available

1. **location_expired** - Pilot location share expiry warning
2. **admin_new_order_critical** - URGENT admin notification for new orders
3. **order_status_changed** - Customer order status updates
4. **admin_new_quote** - Admin notification for new quotes
5. **admin_new_load_plan** - Admin notification for new load plans

## Security Best Practices

### 1. Environment Variables
- Never commit email credentials to version control
- Use environment variables or secure secrets management
- Rotate credentials regularly

### 2. Email Authentication
- Set up SPF records: `v=spf1 include:amazonses.com ~all`
- Configure DKIM signing
- Set up DMARC policy for domain protection

### 3. Rate Limiting
- Implement email rate limiting for production
- Monitor email sending quotas
- Set up bounce and complaint handling

## Deployment Checklist

### Before Going Live:
- [ ] Domain verified with email service provider
- [ ] DNS records configured (SPF, DKIM, DMARC)
- [ ] Environment variables set in production
- [ ] Email templates tested with real data
- [ ] Admin email addresses configured
- [ ] Rate limits and quotas reviewed
- [ ] Backup email service configured (optional)

### Production Monitoring:
- [ ] Email delivery monitoring
- [ ] Bounce rate monitoring
- [ ] Complaint handling setup
- [ ] Error logging and alerting

## Cost Considerations

### Amazon SES Pricing (Estimated):
- $0.10 per 1,000 emails
- $0.12 per GB of attachments
- Very cost-effective for business applications

### SendGrid Pricing:
- Free tier: 100 emails/day
- Essentials: $14.95/month for 50,000 emails
- Pro: $89.95/month for 1.5M emails

## Troubleshooting

### Common Issues:
1. **Emails not sending**: Check environment variables and SMTP credentials
2. **Emails in spam**: Verify SPF/DKIM/DMARC records
3. **Rate limiting**: Check service provider quotas
4. **Template errors**: Verify all template variables are provided

### Debug Mode:
Set `MAIL_DEBUG=true` to see detailed SMTP communication logs.

## Support

For email configuration assistance, contact:
- AWS SES: AWS Support Console
- SendGrid: SendGrid Support
- Application: Check logs for detailed error messages

---

**Note**: The application automatically detects the environment and handles email sending appropriately. In development, emails are logged to console. In production with proper configuration, emails are sent via SMTP. 