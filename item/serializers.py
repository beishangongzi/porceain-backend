from rest_framework.serializers import ModelSerializer
from rest_framework import serializers

from . import models


class ItemSerializer(ModelSerializer):
    class Meta:
        model = models.Item
        fields = "__all__"


class ProdcutEvaluationImageSerializers(serializers.ModelSerializer):
    ''' 用户评论关联图片序列化器 '''
    images = serializers.ImageField(
        max_length=None, use_url=True, allow_null=True, required=False)
    class Meta:
        model = models.ProductEvaluationImage
        fields = "__all__"