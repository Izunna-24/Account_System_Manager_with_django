from django.urls import path
from . import views

urlpatterns = [
    path('accounts', views.list_account),
    path('accounts/<int:pk>', views.account_detail)

]
