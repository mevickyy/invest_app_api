from django.urls import include, path


api_urls = [
    path('', include('accounts.urls')),
    path('', include('company.urls')),
    path('', include('investment.urls')),
]

urlpatterns = [
    path('api/', include(api_urls)),
]