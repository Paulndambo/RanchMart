from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from decimal import Decimal
from django.views.generic import ListView
from django.db.models import Q
from payments.paystack import PaystackIntegration

from payments.models import Payment
from orders.models import Order
# Create your views here.

@login_required
def payments(request):
    payments = Payment.objects.all()
    
    # Filter by user permissions
    if not request.user.is_superuser:
        payments = payments.filter(
            Q(order__receiver=request.user) | 
            Q(order__user=request.user)
        )
    
    # Get filter parameters from request
    search_query = request.GET.get('search')
    payment_method = request.GET.get('payment_method')
    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')
    status = request.GET.get('status')
    
    # Apply search filters
    if search_query:
        try:
            amount_query = float(search_query)
            payments = payments.filter(
                Q(amount=amount_query) |
                Q(order__id__icontains=search_query) |
                Q(order__user__username__icontains=search_query) |
                Q(order__receiver__username__icontains=search_query)
            )
        except ValueError:
            payments = payments.filter(
                Q(order__id__icontains=search_query) |
                Q(order__user__username__icontains=search_query) |
                Q(order__receiver__username__icontains=search_query)
            )
    
    # Filter by payment method
    if payment_method:
        payments = payments.filter(payment_method=payment_method)
        
    # Filter by date range
    if date_from:
        payments = payments.filter(created_at__gte=date_from)
    if date_to:
        payments = payments.filter(created_at__lte=date_to)
        
    # Filter by order status
    if status:
        payments = payments.filter(order__status=status)
    
    # Order by most recent first
    payments = payments.order_by('-created_at')
    
    # Prepare context with filter choices for the template
    context = {
        'payments': payments,
        'search_query': search_query or '',
        'payment_method': payment_method or '',
        'date_from': date_from or '',
        'date_to': date_to or '',
        'status': status or '',
        'payment_method_choices': Payment.objects.values_list('payment_method', flat=True).distinct(),
        'status_choices': Order.objects.values_list('status', flat=True).distinct(),
    }
    
    return render(request, 'payments/payments.html', context)


@login_required
def payment_detail(request, payment_id):
    payment = Payment.objects.get(id=payment_id)
    return render(request, 'payments/payment_detail.html', {'payment': payment})

@login_required
def new_payment(request):
    if request.method == 'POST':
        order_id = request.POST.get('order_id')
        amount = request.POST.get('amount')
        payment_method = request.POST.get('payment_method')
        order = Order.objects.get(id=order_id)
        Payment.objects.create(order=order, amount=amount, payment_method=payment_method)

        order.amount_paid += Decimal(amount)
        order.save()

        if order.amount_paid == order.total_cost:
            order.status = 'Paid'
            order.save()
        else:
            order.status = 'Partially Paid'
            order.save()
        return redirect(reverse('order-detail', args=[order_id]))
    return render(request, 'payments/new_payment.html')


def make_payment(request, order_id):
    order = Order.objects.get(id=order_id)
    if request.method == 'POST':
        amount = request.POST.get('amount')
        payment_method = request.POST.get('payment_method')
        Payment.objects.create(order=order, amount=amount, payment_method=payment_method)
        return redirect(reverse('order-detail', args=[order_id]))
    return render(request, 'payments/make_payment.html', {'order': order})

class PaymentsListView(ListView):
    model = Payment
    template_name = 'payments/payments.html'
    context_object_name = 'payments'
    paginate_by = 10
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filter by user permissions
        if not self.request.user.is_superuser:
            queryset = queryset.filter(
                Q(order__receiver=self.request.user) | 
                Q(order__user=self.request.user)
            )
        
        # Get filter parameters from request
        search_query = self.request.GET.get('search')
        payment_method = self.request.GET.get('payment_method')
        date_from = self.request.GET.get('date_from')
        date_to = self.request.GET.get('date_to')
        status = self.request.GET.get('status')
        
        if search_query:
            # Convert search query to float if it's a number for amount search
            try:
                amount_query = float(search_query)
                queryset = queryset.filter(
                    Q(amount=amount_query) |
                    Q(order__id__icontains=search_query) |
                    Q(order__user__username__icontains=search_query) |
                    Q(order__receiver__username__icontains=search_query)
                )
            except ValueError:
                queryset = queryset.filter(
                    Q(order__id__icontains=search_query) |
                    Q(order__user__username__icontains=search_query) |
                    Q(order__receiver__username__icontains=search_query)
                )
        
        # Filter by payment method
        if payment_method:
            queryset = queryset.filter(payment_method=payment_method)
            
        # Filter by date range
        if date_from:
            queryset = queryset.filter(created_at__gte=date_from)
        if date_to:
            queryset = queryset.filter(created_at__lte=date_to)
            
        # Filter by order status
        if status:
            queryset = queryset.filter(order__status=status)
            
        return queryset.order_by('-created_at')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add filter parameters to context for form persistence
        context['search_query'] = self.request.GET.get('search', '')
        context['payment_method'] = self.request.GET.get('payment_method', '')
        context['date_from'] = self.request.GET.get('date_from', '')
        context['date_to'] = self.request.GET.get('date_to', '')
        context['status'] = self.request.GET.get('status', '')
        
        # Add payment method choices for the filter dropdown
        context['payment_method_choices'] = Payment.objects.values_list(
            'payment_method', flat=True).distinct()
        
        # Add order status choices for the filter dropdown
        context['status_choices'] = Order.objects.values_list(
            'status', flat=True).distinct()
        
        return context


def paystack_callback(request):
    reference = request.GET.get('reference')
    paystack = PaystackIntegration()
    order = paystack.verify_payment(reference)
    if order:
        return redirect(reverse('order-detail', args=[order.id]))
    else:
        return redirect(reverse('order-detail', args=[order.id]))

def paystack_webhook(request):
    pass
