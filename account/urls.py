from django.urls import path, include
from . import views
from rest_framework.routers import SimpleRouter

from .views import Deposit, Withdrawal

router = SimpleRouter()
router.register('accounts', views.AccountViewSet)

urlpatterns = [
    # path('accounts', views.ListAccount.as_view()),
    # path('accounts/<int:pk>', views.AccountViewSet.as_view()),
    path('', include(router.urls)),
    path('deposit', Deposit.as_view()),
    path('withdraw', Withdrawal.as_view()),


    # path('create', views.CreateAccount.as_view()),



]
