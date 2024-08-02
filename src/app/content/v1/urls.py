from rest_framework.routers import SimpleRouter

from app.content.v1.views import ContentViewSet

router = SimpleRouter()
router.register("content", ContentViewSet)

urlpatterns = router.urls
