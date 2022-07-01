from django.urls import path
from .views import *


app_name = 'taskapp'


urlpatterns = [
    path('create/', CreateUserAPI.as_view(), name='create'),
    path('status/', CreateStatusAPI.as_view(), name='status'),
    path('login/', ObtainAuthToken.as_view(), name='api_token_auth'),
]
