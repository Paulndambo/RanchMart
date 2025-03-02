from django.urls import path
from payments.views import payments, payment_detail, new_payment

urlpatterns = [
    path('', payments, name='payments'),
    path('<int:payment_id>/', payment_detail, name='payment-detail'),
    path('new-payment/', new_payment, name='new-payment'),
]
