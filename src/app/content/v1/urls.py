from rest_framework.routers import SimpleRouter

from app.content.v1.views import ContentViewSet, ContentCommentViewSet

router = SimpleRouter()
router.register("content", ContentViewSet)
router.register("content/(?P<content_id>[^/.]+)/comment", ContentCommentViewSet)

urlpatterns = router.urls
