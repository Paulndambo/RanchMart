from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from decimal import Decimal

from payments.models import Payment
from orders.models import Order
# Create your views here.

@login_required
def payments(request):
    payments = Payment.objects.all()
    if not request.user.is_superuser:
        payments = payments.filter(order__receiver=request.user)
    return render(request, 'payments/payments.html', {'payments': payments})


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