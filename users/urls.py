from django.urls import path
from users.views import login_user, logout_user, users, register

urlpatterns = [
    path("", users, name="users"),
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
    path('register/', register, name='register'),
]
