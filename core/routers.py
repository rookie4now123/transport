from rest_framework import routers
from .user.viewsets import UserViewSet, MonitorUserViewSet
from station.viewsets import StationViewSet
from .auth.viewsets import (
    WebLoginViewSet,
    MonitorLoginViewSet,
    WebRegisterViewSet,
)
router = routers.SimpleRouter()
# ############################################################
######### #
# ###################
#USER ###################### #
# ############################################################
######### #
router.register(r'user', UserViewSet, basename='user')
router.register(r'monitors', MonitorUserViewSet, basename='monitor-user')
router.register(r'station', StationViewSet, basename='station')

router.register(r'auth/register', WebRegisterViewSet, basename='web-register')
router.register(r'auth/login', WebLoginViewSet, basename='web-login')
router.register(r'auth/monitor_login', MonitorLoginViewSet, basename='mobile-login')

urlpatterns = [
*router.urls,
]