from django.urls import path
from .views import IndexView, ProductView

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('product/<int:product_id>/', ProductView.as_view(), name='product_detail'),
]