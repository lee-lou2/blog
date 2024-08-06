from rest_framework.routers import SimpleRouter

from app.content.v1.views import ContentViewSet, ContentCommentViewSet

router = SimpleRouter()
router.register("content/comment", ContentCommentViewSet)
router.register("content", ContentViewSet)

urlpatterns = router.urls
