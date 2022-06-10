from django.urls import path
from rest_framework.routers import DefaultRouter

from . import views

urlpatterns = [

]

router = DefaultRouter()
router.register("items", viewset=views.ItemView, basename="item")
router.register("image", viewset=views.ProductEvaluationImageView, basename="image_test")

urlpatterns += router.urls