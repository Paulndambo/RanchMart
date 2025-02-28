from django.urls import path
from shop.views import animals, animal_detail, cow_list, cow_detail, new_cow, edit_cow

urlpatterns = [
    path('', animals, name='animals'),
    path('animal/<int:animal_id>/', animal_detail, name='animal-detail'),
    path('cows/', cow_list, name='cows'),
    path('cows/<int:animal_id>/', cow_detail, name='cow-detail'),
    path('new-cow/', new_cow, name='new-cow'),
    path('edit-cow/', edit_cow, name='edit-cow'),
]

