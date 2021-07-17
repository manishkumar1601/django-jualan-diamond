from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('panel/', admin.site.urls),
    path('', include('main.urls'))
]
