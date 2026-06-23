from django.urls import path
from rest_framework.routers import SimpleRouter

from apps.experiments.views import DatasetUploadView, DatasetViewSet, ExperimentViewSet

router = SimpleRouter()
router.register("experiments", ExperimentViewSet, basename="experiment")
router.register("datasets", DatasetViewSet, basename="dataset")

urlpatterns = [
    path("datasets/upload_csv/", DatasetUploadView.as_view(), name="dataset-upload"),
] + router.urls
