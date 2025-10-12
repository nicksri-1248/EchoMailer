from django import forms
from .models import Recipient, EmailTemplate

class RecipientForm(forms.ModelForm):
    class Meta:
        model = Recipient
        fields = ['email', 'company']
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'company': forms.TextInput(attrs={'class': 'form-control'}),
        }

class BulkRecipientForm(forms.Form):
    csv_file = forms.FileField(
        label='Upload CSV File',
        help_text='CSV format: email, company',
        widget=forms.FileInput(attrs={'class': 'form-control', 'accept': '.csv'})
    )

class EmailTemplateForm(forms.ModelForm):
    class Meta:
        model = EmailTemplate
        fields = ['name', 'subject', 'body']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'subject': forms.TextInput(attrs={'class': 'form-control'}),
            'body': forms.Textarea(attrs={'class': 'form-control', 'rows': 10}),
        }
        help_text = {
            'body': 'Use {{email}}, {{company}} for personalization'
        }

class SendEmailForm(forms.Form):
    template = forms.ModelChoiceField(
        queryset=EmailTemplate.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=False
    )
    subject = forms.CharField(
        max_length=300,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    body = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 10})
    )
    recipients = forms.ModelMultipleChoiceField(
        queryset=Recipient.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True
    )
    send_immediately = forms.BooleanField(
        required=False,
        initial=True,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )