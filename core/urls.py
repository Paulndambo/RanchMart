from django.urls import path
from core.views import home, about, contact, faq, terms, dashboard, non_admin_dashboard

urlpatterns = [
    path('', home, name='home'),
    path('about/', about, name='about'),
    path('contact/', contact, name='contact'),
    path('faq/', faq, name='faq'),
    path('terms/', terms, name='terms'),
    path('dashboard/', dashboard, name='dashboard'),
    path('user-dashboard/', non_admin_dashboard, name='user-dashboard'),
]
