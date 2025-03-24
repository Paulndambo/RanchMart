from datetime import datetime
from decimal import Decimal
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from payments.paystack import PaystackIntegration
from orders.models import Cart, CartItem, Order, OrderItem
from shop.models import Animal


# Create your views here.
# Orders Management
@login_required
def orders(request):
    user = request.user
    orders = Order.objects.all()

    if not user.is_superuser:
        orders = Order.objects.filter(user=user)

    print(f"Username: {user.username}, Is Superuser: {user.is_superuser}")

    context = {
        "orders": orders
    }
    return render(request, "orders/orders.html", context)

### Cart Management
@login_required
def add_to_cart(request, animal_id):
    animal = Animal.objects.get(id=animal_id)
    # This already creates a cart if it doesn't exist
    cart, created = Cart.objects.get_or_create(user=request.user)

    # Get existing cart items
    existing_items = CartItem.objects.filter(cart=cart)
    
    # If there's an existing item with the same animal, increment quantity
    existing_item = existing_items.filter(animal=animal).first()
    if existing_item:
        existing_item.quantity += 1
        cart.total_cost += Decimal(animal.price)
        existing_item.save()
    else:
        # If there's a different item, remove it and create new one
        existing_items.delete()
        CartItem.objects.create(cart=cart, animal=animal, quantity=1)
        cart.total_cost = Decimal(animal.price)  # Reset total cost for new item
    
    cart.save()
    messages.success(request, f"{animal.name} added to cart")
    return redirect('cart')

@login_required
def add_to_cart_from_animal_detail(request):
    if request.method == 'POST':
        animal_id = request.POST.get('animal_id')
        quantity = int(request.POST.get('quantity', 1))
        try:
            animal = Animal.objects.get(id=animal_id)
            # This already creates a cart if it doesn't exist
            cart, created = Cart.objects.get_or_create(user=request.user)
            
            # Get all existing items
            existing_items = CartItem.objects.filter(cart=cart)
            
            # Check if the same animal is already in cart
            existing_item = existing_items.filter(animal=animal).first()
            if existing_item:
                # If same animal, increment quantity
                existing_item.quantity += quantity
                cart.total_cost += Decimal(animal.price) * Decimal(quantity)
                existing_item.save()
            else:
                # If different animal, remove existing items and create new one
                existing_items.delete()
                CartItem.objects.create(cart=cart, animal=animal, quantity=quantity)
                cart.total_cost = Decimal(animal.price) * Decimal(quantity)  # Reset total cost
            
            cart.save()
            messages.success(request, f"{animal.name} added to cart")
            return redirect('animal-detail', animal_id=animal_id)
        except Animal.DoesNotExist:
            messages.error(request, "Animal not found")
            return redirect('animal-detail', animal_id=animal_id)
    return redirect('animal-detail', animal_id=animal_id)


@login_required
def increase_quantity(request, item_id):
    item = CartItem.objects.get(id=item_id)
    item.quantity += 1
    cart = item.cart
    cart.total_cost += Decimal(item.animal.price)
    cart.save()
    item.save()
    return redirect('cart')


@login_required
def decrease_quantity(request, item_id):
    item = CartItem.objects.get(id=item_id)
    item.quantity -= 1
    cart = item.cart
    cart.total_cost -= Decimal(item.animal.price)
    cart.save()
    item.save()
    return redirect('cart')

@login_required
def remove_from_cart(request, item_id):
    item = CartItem.objects.get(id=item_id)
    cart = item.cart
    cart.total_cost -= (Decimal(item.animal.price) * Decimal(item.quantity))
    cart.save()
    item.delete()
    messages.success(request, "Item removed from cart")
    return redirect('cart')


@login_required
@transaction.atomic
def checkout(request, cart_id):
    cart= Cart.objects.get(id=cart_id)
    items = CartItem.objects.filter(cart=cart)

    order = Order.objects.create(
        user=request.user,
        total_cost=cart.total_cost,
        status="Pending",
    )

    for item in items:
        order_item = OrderItem.objects.create(
            order=order,
            animal=item.animal,
            quantity=item.quantity
        )
        order_item.order.receiver = item.animal.owner
        order_item.order.save()

    cart.delete()
    total_amount = int(order.total_cost * 100)
    paystack = PaystackIntegration()
    authorization_url, reference = paystack.initiate_payment(total_amount, request.user.email)
    if authorization_url:
        order.payment_url = authorization_url
        order.payment_reference = reference
        order.save()
        return redirect(authorization_url)
    else:
        messages.error(request, "Payment failed")
        return redirect(reverse('order-detail', args=[order.id]))
   

@login_required
def order_detail(request, order_id):
    user = request.user
    order = Order.objects.get(id=order_id)
    items = OrderItem.objects.filter(order=order)


    return render(request, 'orders/order_detail.html', {'order': order, 'items': items})


def print_receipt(request, order_id):
    order = Order.objects.get(id=order_id)
    items = OrderItem.objects.filter(order=order)
    return render(request, 'orders/order_receipt.html', {'order': order, 'items': items})


@login_required
def cart(request):
    cart, _ = Cart.objects.get_or_create(user=request.user)
    items = CartItem.objects.filter(cart=cart)
    print("**************Cart Items**************")
    print(items)
    print("**************Cart Items**************")
    return render(request, 'cart/cart.html', {'items': items, "cart": cart})


@login_required
def confirm_payment(request):
    if request.method == 'POST':
        order_id = request.POST.get('order_id')
        order = Order.objects.get(id=order_id)
        order.status = 'Payment Confirmed'
        order.save()
        return redirect(reverse('order-detail', args=[order_id]))
    return render(request, 'orders/confirm_payment.html')


@login_required
def orders_report(request):
    generated_on = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    orders = Order.objects.all().order_by('-created_at')

    orders_average = sum(order.total_cost for order in orders) / orders.count()
    total_revenue = sum(order.total_cost for order in orders)

    summary = {
        'total_orders': orders.count(),
        'total_revenue': round(total_revenue, 2),
        'average_order_value': round(orders_average, 2)
    }


    return render(request, 'orders/order_report.html', {'orders': orders, 'generated_on': generated_on, 'summary': summary})
