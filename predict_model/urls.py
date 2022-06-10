from django.urls import path
from rest_framework.routers import DefaultRouter

from . import views

urlpatterns = [

]

router = DefaultRouter()
router.register("porcelain", viewset=views.PorcelainView, basename="porcelain")
router.register("dynasty", viewset=views.DynastyView, basename="dynasty")
router.register("EmperorYear", viewset=views.EmperorYearView, basename="EmperorYear")

urlpatterns += router.urls