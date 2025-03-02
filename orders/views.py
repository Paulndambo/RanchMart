from decimal import Decimal
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction

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
    cart, _ = Cart.objects.get_or_create(user=request.user)

    item = CartItem.objects.filter(cart=cart, animal=animal).first()
    if item:
        item.quantity += 1
        item.save()
    else:
        CartItem.objects.create(cart=cart, animal=animal, quantity=1)
    cart.total_cost += Decimal(animal.price)
    cart.save()
    messages.success(request, f"{animal.name} added to cart")
    return redirect('cart')

@login_required
def add_to_cart_from_animal_detail(request):
    if request.method == 'POST':
        animal_id = request.POST.get('animal_id')
        quantity = request.POST.get('quantity')
        try:
            animal = Animal.objects.get(id=animal_id)
            cart, _ = Cart.objects.get_or_create(user=request.user)

            item = CartItem.objects.filter(cart=cart, animal=animal).first()
            if item:
                item.quantity += int(quantity)
                item.save()
            else:   
                CartItem.objects.create(cart=cart, animal=animal, quantity=quantity)
            cart.total_cost += Decimal(quantity) * Decimal(animal.price)
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
        status="Pending"
    )

    for item in items:
        OrderItem.objects.create(
            order=order,
            animal=item.animal,
            quantity=item.quantity
        )

    cart.delete()
    messages.success(request, "Order placed successfully")
    return redirect("dashboard")
   

def order_detail(request, order_id):
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
