import csv
from django.core.mail import send_mail, EmailMessage
from django.template import Template, Context
from django.conf import settings
from .models import Recipient, EmailLog
import logging

logger = logging.getLogger(__name__)

def personalize_message(template_text, recipient):
    """Personalize email message with recipient data"""
    template = Template(template_text)
    context = Context({
        'email': recipient.email,
        'company': recipient.company,
    })
    return template.render(context)

def send_bulk_emails(subject, body, recipients, template=None):
    """Send personalized emails to multiple recipients"""
    results = {
        'success': 0,
        'failed': 0,
        'errors': []
    }
    
    for recipient in recipients:
        try:
            # Personalize subject and body
            personalized_subject = personalize_message(subject, recipient)
            personalized_body = personalize_message(body, recipient)
            
            # Send email
            send_mail(
                subject=personalized_subject,
                message=personalized_body,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[recipient.email],
                fail_silently=False,
            )
            
            # Log success
            EmailLog.objects.create(
                recipient=recipient,
                template=template,
                subject=personalized_subject,
                body=personalized_body,
                status='sent'
            )
            results['success'] += 1
            logger.info(f"Email sent successfully to {recipient.email}")
            
        except Exception as e:
            # Log failure
            EmailLog.objects.create(
                recipient=recipient,
                template=template,
                subject=subject,
                body=body,
                status='failed',
                error_message=str(e)
            )
            results['failed'] += 1
            results['errors'].append(f"{recipient.email}: {str(e)}")
            logger.error(f"Failed to send email to {recipient.email}: {str(e)}")
    
    return results

def import_recipients_from_csv(csv_file):
    """Import recipients from CSV file"""
    results = {
        'success': 0,
        'failed': 0,
        'errors': []
    }
    
    try:
        decoded_file = csv_file.read().decode('utf-8').splitlines()
        reader = csv.DictReader(decoded_file)
        
        for row in reader:
            try:
                recipient, created = Recipient.objects.get_or_create(
                    email=row['email'],
                    defaults={
                        'company': row.get('company', ''),
                    }
                )
                if created:
                    results['success'] += 1
                else:
                    results['failed'] += 1
                    results['errors'].append(f"{row['email']} already exists")
            except Exception as e:
                results['failed'] += 1
                results['errors'].append(f"Error importing {row.get('email', 'unknown')}: {str(e)}")
    
    except Exception as e:
        results['errors'].append(f"File processing error: {str(e)}")
    
    return results