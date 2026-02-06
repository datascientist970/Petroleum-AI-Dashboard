# urls.py (in your app directory)
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('api/dashboard-data/', views.api_dashboard_data, name='api_dashboard_data'),
    path('api/ai-insights/', views.api_ai_insights, name='api_ai_insights'),
    path('generate-pdf-report/', views.generate_pdf_report, name='generate_pdf_report'),
]