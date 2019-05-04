from django.urls import path

from . import views

app_name = 'user'
url_patterns = [
    path('login', LoginView.as_view(), name='login'),
    path('logout', LogoutView.as_view(), name='logout'),
]
