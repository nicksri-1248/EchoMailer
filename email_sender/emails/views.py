from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q, Count
from .models import Recipient, EmailTemplate, EmailLog
from .forms import RecipientForm, EmailTemplateForm, SendEmailForm, BulkRecipientForm
from .utils import send_bulk_emails, import_recipients_from_csv

def dashboard(request):
    total_recipients = Recipient.objects.count()
    total_templates = EmailTemplate.objects.count()
    total_sent = EmailLog.objects.filter(status='sent').count()
    total_failed = EmailLog.objects.filter(status='failed').count()
    
    recent_logs = EmailLog.objects.all()[:10]
    
    context = {
        'total_recipients': total_recipients,
        'total_templates': total_templates,
        'total_sent': total_sent,
        'total_failed': total_failed,
        'recent_logs': recent_logs,
    }
    return render(request, 'emails/dashboard.html', context)

def recipient_list(request):
    recipients = Recipient.objects.all()
    search = request.GET.get('search', '')
    
    if search:
        recipients = recipients.filter(
            Q(email__icontains=search) |
            Q(company__icontains=search)
        )
    
    context = {'recipients': recipients, 'search': search}
    return render(request, 'emails/recipient_list.html', context)

def add_recipient(request):
    if request.method == 'POST':
        form = RecipientForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Recipient added successfully!')
            return redirect('recipient_list')
    else:
        form = RecipientForm()
    
    return render(request, 'emails/recipient_form.html', {'form': form})

def import_recipients(request):
    if request.method == 'POST':
        form = BulkRecipientForm(request.POST, request.FILES)
        if form.is_valid():
            results = import_recipients_from_csv(request.FILES['csv_file'])
            messages.success(request, f"Imported {results['success']} recipients. Failed: {results['failed']}")
            if results['errors']:
                for error in results['errors'][:5]:
                    messages.warning(request, error)
            return redirect('recipient_list')
    else:
        form = BulkRecipientForm()
    
    return render(request, 'emails/import_recipients.html', {'form': form})

def template_list(request):
    templates = EmailTemplate.objects.all()
    return render(request, 'emails/template_list.html', {'templates': templates})

def add_template(request):
    if request.method == 'POST':
        form = EmailTemplateForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Template created successfully!')
            return redirect('template_list')
    else:
        form = EmailTemplateForm()
    
    return render(request, 'emails/template_form.html', {'form': form})

def compose_email(request):
    if request.method == 'POST':
        form = SendEmailForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            body = form.cleaned_data['body']
            recipients = form.cleaned_data['recipients']
            template = form.cleaned_data.get('template')
            
            if form.cleaned_data['send_immediately']:
                results = send_bulk_emails(subject, body, recipients, template)
                messages.success(request, f"Sent {results['success']} emails. Failed: {results['failed']}")
                if results['errors']:
                    for error in results['errors'][:5]:
                        messages.error(request, error)
            
            return redirect('dashboard')
    else:
        form = SendEmailForm()
    
    return render(request, 'emails/compose.html', {'form': form})

def email_logs(request):
    logs = EmailLog.objects.all()
    status_filter = request.GET.get('status', '')
    
    if status_filter:
        logs = logs.filter(status=status_filter)
    
    context = {'logs': logs, 'status_filter': status_filter}
    return render(request, 'emails/email_logs.html', context)

def delete_recipient(request, pk):
    recipient = get_object_or_404(Recipient, pk=pk)
    if request.method == 'POST':
        recipient.delete()
        messages.success(request, f'Recipient {recipient.email} deleted successfully!')
        return redirect('recipient_list')
    return redirect('recipient_list')

def edit_recipient(request, pk):
    recipient = get_object_or_404(Recipient, pk=pk)
    if request.method == 'POST':
        form = RecipientForm(request.POST, instance=recipient)
        if form.is_valid():
            form.save()
            messages.success(request, 'Recipient updated successfully!')
            return redirect('recipient_list')
    else:
        form = RecipientForm(instance=recipient)
    
    return render(request, 'emails/recipient_form.html', {'form': form, 'edit_mode': True})