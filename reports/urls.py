from django.urls import path
from reports.views import sales_report, inventory_report, financial_report

urlpatterns = [
    path('sales-report/', sales_report, name='sales-report'),
    path('inventory-report/', inventory_report, name='inventory-report'),
    path('financial-report/', financial_report, name='financial-report'),
]
