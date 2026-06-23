from pathlib import Path

from rest_framework import serializers

from apps.experiments.models import Dataset, Experiment


class ExperimentSerializer(serializers.ModelSerializer[Experiment]):
    class Meta:
        model = Experiment
        fields = ["id", "title", "description", "owner", "created_at"]
        read_only_fields = ["id", "owner", "created_at"]


class DatasetSerializer(serializers.ModelSerializer[Dataset]):
    class Meta:
        model = Dataset
        fields = ["id", "name", "version", "file", "owner", "uploaded_at"]
        read_only_fields = ["id", "owner", "uploaded_at"]

    def validate_file(self, value) -> object:
        ext = Path(value.name).suffix.lower()
        if ext != ".csv":
            raise serializers.ValidationError("Solo se permiten archivos CSV.")
        return value
