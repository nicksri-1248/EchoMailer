from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('recipients/', views.recipient_list, name='recipient_list'),
    path('recipients/add/', views.add_recipient, name='add_recipient'),
    path('recipients/<int:pk>/edit/', views.edit_recipient, name='edit_recipient'),
    path('recipients/<int:pk>/delete/', views.delete_recipient, name='delete_recipient'),
    path('recipients/import/', views.import_recipients, name='import_recipients'),
    path('templates/', views.template_list, name='template_list'),
    path('templates/add/', views.add_template, name='add_template'),
    path('compose/', views.compose_email, name='compose_email'),
    path('logs/', views.email_logs, name='email_logs'),
]