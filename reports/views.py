import csv
from django.shortcuts import render
from django.http import HttpResponse
from orders.models import Order
from django.utils import timezone
from datetime import datetime

from shop.models import Animal
from payments.models import Payment
# Create your views here.
def sales_report(request):
    orders = Order.objects.all()
    
    # Handle date filtering
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    status = request.GET.get('status')
    
    if start_date:
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
        orders = orders.filter(created_at__gte=start_date)
    
    if end_date:
        end_date = datetime.strptime(end_date, '%Y-%m-%d')
        orders = orders.filter(created_at__lte=end_date)
    
    if status:
        orders = orders.filter(status=status)
    
    # Handle CSV export
    if request.GET.get('export') == 'csv':
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="sales_report.csv"'
        
        writer = csv.writer(response)
        writer.writerow(['Order ID', 'Customer', 'Total', 'Date', 'Status'])
        
        for order in orders:
            writer.writerow([
                order.id,
                f"{order.user.first_name} {order.user.last_name}",
                order.total_cost,
                order.created_at.strftime('%Y-%m-%d'),
                order.status
            ])
        
        return response
    
    context = {
        'orders': orders,
        'start_date': start_date,
        'end_date': end_date,
        'order_statuses': ["Pending", "Paid", "Delivered", "Cancelled"],
    }
    return render(request, 'reports/orders.html', context)


def inventory_report(request):
    animals = Animal.objects.all()
    
    # Handle filtering
    species = request.GET.get('species')
    status = request.GET.get('status')
    age_range = request.GET.get('age_range')
    
    if species:
        animals = animals.filter(species=species)
    
    if status:
        animals = animals.filter(status=status)
        
    if age_range:
        if age_range == 'young':
            animals = animals.filter(age__lt=2)
        elif age_range == 'adult':
            animals = animals.filter(age__gte=2, age__lt=10)
        elif age_range == 'senior':
            animals = animals.filter(age__gte=10)
    
    # Handle CSV export
    if request.GET.get('export') == 'csv':
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="inventory_report.csv"'
        
        writer = csv.writer(response)
        writer.writerow(['ID', 'Name', 'Species', 'Age', 'Status', 'Price', 'Added Date'])
        
        for animal in animals:
            writer.writerow([
                animal.id,
                animal.name,
                animal.species,
                animal.age,
                animal.status,
                animal.price,
                animal.created_at.strftime('%Y-%m-%d')
            ])
        
        return response
    
    # Get unique species for filter dropdown
    all_species = Animal.objects.values_list('species', flat=True).distinct()
    animal_statuses = ["Available", "Sold", "Reserved", "Not Available"]
    age_ranges = [
        ('all', 'All Ages'),
        ('young', 'Young (< 2 years)'),
        ('adult', 'Adult (2-10 years)'),
        ('senior', 'Senior (10+ years)')
    ]
    
    context = {
        'animals': animals,
        'species_list': all_species,
        'animal_statuses': animal_statuses,
        'age_ranges': age_ranges,
        'selected_species': species,
        'selected_status': status,
        'selected_age_range': age_range,
    }
    return render(request, 'reports/animals.html', context)


def financial_report(request):
    payments = Payment.objects.all()
    
    # Handle date filtering
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    payment_method = request.GET.get('payment_method')
    status = request.GET.get('status')
    
    if start_date:
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
        payments = payments.filter(created_at__date__gte=start_date)
    
    if end_date:
        end_date = datetime.strptime(end_date, '%Y-%m-%d')
        payments = payments.filter(created_at__date__lte=end_date)
    
    if payment_method:
        payments = payments.filter(payment_method=payment_method)
        
    if status:
        payments = payments.filter(status=status)
    
    # Handle CSV export
    if request.GET.get('export') == 'csv':
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="financial_report.csv"'
        
        writer = csv.writer(response)
        writer.writerow(['Payment ID', 'Order ID', 'Customer', 'Amount', 'Payment Type', 'Status', 'Date'])
        
        for payment in payments:
            writer.writerow([
                payment.id,
                payment.order.id if payment.order else 'N/A',
                f"{payment.order.user.first_name} {payment.order.user.last_name}",
                payment.amount,
                payment.payment_method,
                payment.created_at.strftime('%Y-%m-%d')
            ])
        
        return response
    
    # Get unique payment types and statuses for filter dropdowns
    payment_types = Payment.objects.values_list('payment_method', flat=True).distinct()
    payment_statuses = ["Completed", "Pending", "Failed", "Refunded"]
    
    context = {
        'payments': payments,
        'payment_types': payment_types,
        'payment_statuses': payment_statuses,
        'start_date': start_date,
        'end_date': end_date,
        'selected_payment_method': payment_method,
        'selected_status': status,
    }
    return render(request, 'reports/payments.html', context)

