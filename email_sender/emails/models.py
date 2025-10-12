from django.db import models
from django.contrib.auth.models import User

class Recipient(models.Model):
    email = models.EmailField(unique=True)
    company = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['email']
    
    def __str__(self):
        return f"{self.email} ({self.company})" if self.company else self.email

class EmailTemplate(models.Model):
    name = models.CharField(max_length=200)
    subject = models.CharField(max_length=300)
    body = models.TextField(help_text="Use {{email}}, {{company}} for personalization")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name

class EmailLog(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('sent', 'Sent'),
        ('failed', 'Failed'),
    ]
    
    recipient = models.ForeignKey(Recipient, on_delete=models.CASCADE)
    template = models.ForeignKey(EmailTemplate, on_delete=models.SET_NULL, null=True)
    subject = models.CharField(max_length=300)
    body = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    error_message = models.TextField(blank=True)
    sent_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.recipient.email} - {self.status}"