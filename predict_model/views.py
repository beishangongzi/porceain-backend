from django.shortcuts import render

from rest_framework.viewsets import ModelViewSet
from rest_framework import viewsets
from rest_framework import mixins
from rest_framework.response import Response
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.parsers import JSONParser, MultiPartParser
from rest_framework import status
from django.utils.timezone import now

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


class PredictView(viewsets.GenericViewSet, mixins.CreateModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.ListModelMixin):
    queryset = models.PrdictModel.objects.all()
    serializer_class = serializers.PredictSerializer
    parser_classes = [MultiPartParser]

    def create(self, request, *args, **kwargs):
        """
        predict the image

        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        predict_age = self.predict(serializer.validated_data)
        serializer.validated_data.update({"uploader": request.user, "datetime": now(),
                                          "predict_age": predict_age})
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def predict(self, request):
        return models.EmperorYear.objects.get(pk=1)

    # def list(self, request, *args, **kwargs):
    #     res_super = super(PredictView, self).list(request, *args, **kwargs)
    #     return res_super

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset().filter(uploader=request.user))

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)