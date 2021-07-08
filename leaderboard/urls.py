from django.urls import path
from .views import *

urlpatterns = [
    path('', board, name='board'),
    path('join/', join, name='join'),
    path('board/', board, name='board'),
    path('verify/', verify, name='verify'),
]
