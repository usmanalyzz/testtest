from django.urls import path
from .views import *

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('userflow/', Userflows.as_view(), name='userflow'),
    path('product/<str:title>/', IndexView.as_view(), name='product_title'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('forget/', CustomPasswordResetView.as_view(), name='forget'),
    path('user-flows/<int:product_id>/', UserFlowDetail.as_view(), name='user_flow_detail'),
    path('api/user-flow/<int:user_flow_id>/', UserFlowDetailAPI.as_view(), name='user_flow_api'),

]