from django.urls import path
from .views import *

app_name = 'investment'

urlpatterns = [
    path('investments/', CreateInvestmentAPIView.as_view(), name="list"), #POST
    path('investment_lists', InvestmentListAPIView.as_view(), name="list_out"), #GET
    path('investments/<pk>/', UpdateInvestmentAPIView.as_view(), name="update"), #PUT
    path('delete_investments/<pk>/', DestroyInvestmentAPIView.as_view(), name="delete"), #DELETE 
]