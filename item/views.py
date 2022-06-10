from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from . import models
from . import serializers
from .models import ProductEvaluationImage
from .serializers import ProdcutEvaluationImageSerializers


class ItemView(ReadOnlyModelViewSet):
    queryset = models.Item.objects.all()
    serializer_class = serializers.ItemSerializer


from rest_framework.parsers import JSONParser, MultiPartParser


class ProductEvaluationImageView(GenericViewSet):
    queryset = ProductEvaluationImage.objects.all()
    serializer_class = ProdcutEvaluationImageSerializers
    parser_classes = [JSONParser, MultiPartParser]

    def create(self, request):
        data = request.data
        files = request.FILES.getlist('images')
        product_id = request.data['product']
        for file in files:
            serializer = self.get_serializer(
                data={"images": file, "evaluation": data["evaluation"]})
            serializer.is_valid(raise_exception=True)
            serializer.save()
        return Response("获取成功", status=200)
