from django.urls import path
from . import views
from tripay.views import thank_you, received_callback
from config import TRIPAY_PRIVATE_KEY 

urlpatterns = [
    path('', views.index),
    path('check-purchase/', views.checkPurchase, name = "check-purchase"),
    path('thank-you/', thank_you),
    path(f'{TRIPAY_PRIVATE_KEY}/webhook', received_callback),
    path('api/check-id', views.checkId),
    path('api/generate-payment', views.generatePayment, name = "generate-payment")
]