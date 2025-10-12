from django.contrib import admin
from .models import Recipient, EmailTemplate, EmailLog

@admin.register(Recipient)
class RecipientAdmin(admin.ModelAdmin):
    list_display = ['email', 'company', 'created_at']
    list_filter = ['created_at']
    search_fields = ['email', 'company']

@admin.register(EmailTemplate)
class EmailTemplateAdmin(admin.ModelAdmin):
    list_display = ['name', 'subject', 'created_at', 'updated_at']
    search_fields = ['name', 'subject']

@admin.register(EmailLog)
class EmailLogAdmin(admin.ModelAdmin):
    list_display = ['recipient', 'subject', 'status', 'sent_at', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['recipient__email', 'subject']