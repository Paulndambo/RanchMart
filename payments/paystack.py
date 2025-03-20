import requests
from orders.models import Order
from payments.models import Payment
class PaystackIntegration:
    BASE_URL = "https://api.paystack.co"

    def __init__(self):
        self.secret_key = "sk_test_aac883149953639077db21cf2d96590e04829777"

    def initiate_payment(self, amount, email):
        url = f"{self.BASE_URL}/transaction/initialize"
        headers = {
            "Authorization": f"Bearer {self.secret_key}",
            "Content-Type": "application/json"
        }
        data = {
            "amount": amount,
            "email": email,
            "callback_url": "http://localhost:8000/payments/paystack-callback/"
        }
        response = requests.post(url, headers=headers, json=data)

        if response.status_code == 200:
            data = response.json()
            print(data["data"]["authorization_url"], data["data"]["reference"])
            return data["data"]["authorization_url"], data["data"]["reference"]
        else:   
            print(response.json())
            return None

    def verify_payment(self, reference):
        url = f"{self.BASE_URL}/transaction/verify/{reference}"
        headers = {
            "Authorization": f"Bearer {self.secret_key}",
            "Content-Type": "application/json"
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            
            if data["data"]["status"] == "success": 
                payment_method = data["data"]["authorization"]["bank"]
                order = Order.objects.get(payment_reference=reference)
                order.payment_method = payment_method
                order.status = "Paid"
                order.save()
                Payment.objects.create(order=order, amount=order.total_cost, payment_method=payment_method)
                return order
            else:
                return None
        else:
            print(response.json())
            return None

    def create_checkout_url(self, amount, email, callback_url):
        pass


