from rest_framework.routers import SimpleRouter

from apps.experiments.views import ExperimentViewSet

router = SimpleRouter()
router.register("experiments", ExperimentViewSet, basename="experiment")

urlpatterns = router.urls
