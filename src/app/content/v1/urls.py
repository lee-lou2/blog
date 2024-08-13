from rest_framework.routers import SimpleRouter

from app.content.v1.views import ContentViewSet, ContentCommentViewSet

router = SimpleRouter()
router.register("", ContentViewSet)
router.register("(?P<content_id>[^/.]+)/comment", ContentCommentViewSet)

urlpatterns = router.urls
