from rest_framework.serializers import ModelSerializer

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
