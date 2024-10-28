from django.urls import path
from .views import IndexView, ProductView, CustomLoginView, CustomPasswordResetView, RegisterView, CustomLogoutView

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('product/<int:product_id>/', ProductView.as_view(), name='product_detail'),
    path('product/<str:title>/', IndexView.as_view(), name='product_title'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('forget/', CustomPasswordResetView.as_view(), name='forget'),
]