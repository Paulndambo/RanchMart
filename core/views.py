from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from shop.models import Animal
from orders.models import Order, OrderItem
from users.models import User

# Create your views here.
def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')

def faq(request):
    return render(request, 'faq.html')

def terms(request):
    return render(request, 'terms.html')

@login_required
def dashboard(request):
    if not request.user.is_superuser:
        return redirect('user-dashboard')

    orders_count = Order.objects.all().count()
    animals_count = Animal.objects.all().count()
    users_count = User.objects.all().count()
    orders = Order.objects.all()[:5]

    context = {
        "orders_count": orders_count,
        "animals_count": animals_count,
        "users_count": users_count,
        "orders": orders
    }
    return render(request, 'dashboard.html', context)


@login_required
def non_admin_dashboard(request):
    orders = Order.objects.filter(user=request.user)
    animals = Animal.objects.filter(owner=request.user)
    my_animal_sales = OrderItem.objects.filter(animal__owner=request.user)
    total_sales = sum(item.quantity * item.animal.price for item in my_animal_sales)
    sales_count = my_animal_sales.count()

    context = {
        "orders": orders,
        "animals_count": animals.count(),
        "orders_count": orders.count(),
        "my_animal_sales": my_animal_sales,
        "total_sales": total_sales,
        "sales_count": sales_count
    }
    print(context)
    return render(request, 'user_dashboard.html', context)
