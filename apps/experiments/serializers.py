from rest_framework import serializers

from apps.experiments.models import Experiment


class ExperimentSerializer(serializers.ModelSerializer[Experiment]):
    class Meta:
        model = Experiment
        fields = ["id", "title", "description", "owner", "created_at"]
        read_only_fields = ["id", "owner", "created_at"]
