from django.urls import path

from devices.views import add_device, get_device

urlpatterns = [
    path('add-device', add_device),
    path("get-device", get_device)
]