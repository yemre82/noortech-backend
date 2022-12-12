from django.urls import path

from devices.views import add_device

urlpatterns = [
    path('add-device', add_device),
]