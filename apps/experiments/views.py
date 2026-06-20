from typing import cast

from django.http import FileResponse
from rest_framework import generics, mixins, permissions, viewsets
from rest_framework.decorators import action
from drf_spectacular.utils import extend_schema

from apps.accounts.models import User
from apps.experiments.models import Dataset, Experiment
from apps.experiments.serializers import DatasetSerializer, ExperimentSerializer


@extend_schema(tags=["Experiments"])
class ExperimentViewSet(viewsets.ModelViewSet[Experiment]):
    serializer_class = ExperimentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Experiment.objects.filter(owner=cast(User, self.request.user))

    def perform_create(self, serializer) -> None:
        serializer.save(owner=self.request.user)


@extend_schema(tags=["Datasets"])
class DatasetUploadView(generics.CreateAPIView[Dataset]):
    serializer_class = DatasetSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer) -> None:
        serializer.save(owner=self.request.user)


@extend_schema(tags=["Datasets"])
class DatasetViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet[Dataset],
):
    serializer_class = DatasetSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Dataset.objects.filter(owner=cast(User, self.request.user))

    @action(detail=True, methods=["get"])
    def download(self, request, pk=None) -> FileResponse:
        dataset = self.get_object()
        filename = dataset.name
        response = FileResponse(dataset.file.open("rb"), as_attachment=True)
        response["Content-Disposition"] = f'attachment; filename="{filename}"'
        return response
