from django.urls import path
from .views import IndexView, ProductView

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('products/', ProductView.as_view(), name='products'),
]