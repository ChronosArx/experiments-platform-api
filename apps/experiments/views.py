from typing import cast

from rest_framework import permissions, viewsets
from drf_spectacular.utils import extend_schema

from apps.accounts.models import User
from apps.experiments.models import Experiment
from apps.experiments.serializers import ExperimentSerializer


@extend_schema(tags=["Experiments"])
class ExperimentViewSet(viewsets.ModelViewSet[Experiment]):
    serializer_class = ExperimentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Experiment.objects.filter(owner=cast(User, self.request.user))

    def perform_create(self, serializer) -> None:
        serializer.save(owner=self.request.user)
