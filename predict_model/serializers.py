from rest_framework.serializers import ModelSerializer, Serializer
from rest_framework import serializers
import django
from django.utils.timezone import now

from . import models


class PorcelainSerializer(ModelSerializer):
    class Meta:
        model = models.Porcelain
        fields = "__all__"


class EmperorYearSerializer(ModelSerializer):
    class Meta:
        model = models.EmperorYear
        fields = "__all__"


class DynastySerializer(ModelSerializer):
    class Meta:
        model = models.Dynasty
        fields = "__all__"


class PredictSerializer(ModelSerializer):
    # image = serializers.ImageField()
    # name = serializers.CharField(max_length=10)
    # description = serializers.CharField()
    # value = serializers.FloatField()
    # datetime = serializers.DateTimeField(read_only=True)
    # uploader = serializers.IntegerField(read_only=True, source="User.id")
    # truth_age = serializers.IntegerField(source="EmperorYear.id")
    # predict_age = serializers.IntegerField(source="EmperorYear.id")
    class Meta:
        fields = "__all__"
        model = models.PrdictModel
        read_only_fields = ["id", "uploader", "datetime", "predict_age"]
        depth = 3

        extra_kwargs = {
            # "uploader"
        }

    def create(self, validated_data):
        return models.PrdictModel.objects.create(**validated_data)



