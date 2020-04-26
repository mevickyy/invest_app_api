from django.urls import path
from .views import *


urlpatterns = [
    path('admin/company/', CreateCompanyAPIView.as_view(), name="list"), #POST
    path('admin/company_lists', CompanyListAPIView.as_view(), name="list_out"), #GET
    path('admin/company/<pk>/', UpdateCompanyAPIView.as_view(), name="update"), #PUT
    path('admin/delete_company/<pk>/', DestroyCompanyAPIView.as_view(), name="delete"), #DELETE
]