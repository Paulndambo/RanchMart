from django.urls import path
from orders.views import checkout, order_detail, add_to_cart, cart, add_to_cart_from_animal_detail, remove_from_cart, increase_quantity, decrease_quantity, orders

urlpatterns = [
    path("", orders, name="orders"),
    path('<int:order_id>/', order_detail, name='order-detail'),
    path('cart/', cart, name='cart'),
    path('add-to-cart/<int:animal_id>/', add_to_cart, name='add-to-cart'),
    path('add-to-cart-from-animal-detail/', add_to_cart_from_animal_detail, name='add-to-cart-from-animal-detail'),
    path('remove-from-cart/<int:item_id>/', remove_from_cart, name='remove-from-cart'),
    path('increment-quantity/<int:item_id>/', increase_quantity, name='increment-quantity'),
    path('decrement-quantity/<int:item_id>/', decrease_quantity, name='decrement-quantity'),
    path('checkout/<int:cart_id>/', checkout, name='checkout'),
]
