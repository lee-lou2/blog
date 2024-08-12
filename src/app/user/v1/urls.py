from rest_framework.routers import SimpleRouter

from app.user.v1.views import UserProfileViewSet

router = SimpleRouter()
router.register("user/profile", UserProfileViewSet)

urlpatterns = router.urls
