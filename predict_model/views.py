from django.shortcuts import render

from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.parsers import JSONParser, MultiPartParser

from . import models
from . import serializers


manual_parameters = [
    openapi.Parameter(name="file",
                      in_=openapi.IN_BODY,
                      type=openapi.TYPE_FILE,
                      required=True,
                      description="upload image")
]



class PorcelainView(ModelViewSet):
    queryset = models.Porcelain.objects.all()
    serializer_class = serializers.PorcelainSerializer
    parser_classes = [MultiPartParser]



class EmperorYearView(ModelViewSet):
    queryset = models.EmperorYear.objects.all()
    serializer_class = serializers.EmperorYearSerializer


class DynastyView(ModelViewSet):
    queryset = models.Dynasty.objects.all()
    serializer_class = serializers.DynastySerializer
