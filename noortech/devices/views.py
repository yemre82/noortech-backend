from datetime import datetime
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from noortech.responses import response_200, response_400, response_500
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.authtoken.models import Token

from devices.models import Devices

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_device(request):
    devices_obj=Devices.objects.all().order_by('-id')
    if len(devices_obj)==0:
        client_id=1
        pub_id=1
        sub_id=1
    else:
        client_id=devices_obj[0].client_id+1
        pub_id=devices_obj[0].pub_id+1
        sub_id=devices_obj[0].sub_id+1
    device_obj=Devices.objects.create(
        client_id=client_id,
        pub_id=pub_id,
        sub_id=sub_id
    )
    return response_200({
        "client_id":device_obj.client_id,
        "pub_id":device_obj.pub_id,
        "sub_id":device_obj.sub_id,
        "qrcode":"http://167.71.61.186:8081/media/"+str(device_obj.code)
    })


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def get_device(request):
    my_id=request.data.get("id")
    try:
        device_obj=Devices.objects.get(id=my_id)
        return response_200({
            "client_id":device_obj.client_id,
            "pub_id":device_obj.pub_id,
            "sub_id":device_obj.sub_id,
            "qrcode":"http://167.71.61.186:8081/media/"+str(device_obj.code)})
    except ObjectDoesNotExist as e:
        return response_400("Device not found")