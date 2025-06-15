from rest_framework import routers
from .user.viewsets import UserViewSet, MonitorUserViewSet
from station.viewsets import StationViewSet
from route.viewsets import RouteViewSet
from .auth.viewsets import (
    WebLoginViewSet,
    MonitorLoginViewSet,
    WebRegisterViewSet,
)
from tracking.viewsets import(
    MobileRouteRunViewSet,
    MobileLocationPointViewSet,
    WebRouteRunViewSet,
    WebLocationPointViewSet
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
router.register(r'route', RouteViewSet, basename='route')

router.register(r'routeruns', MobileRouteRunViewSet, basename='mobile-routerun')
router.register(r'locationpoints', MobileLocationPointViewSet, basename='mobile-locationpoint')
router.register(r'routeruns', WebRouteRunViewSet, basename='web-routerun')
router.register(r'locationpoints', WebLocationPointViewSet, basename='web-locationpoint')


router.register(r'auth/register', WebRegisterViewSet, basename='web-register')
router.register(r'auth/login', WebLoginViewSet, basename='web-login')
router.register(r'auth/monitor_login', MonitorLoginViewSet, basename='mobile-login')

urlpatterns = [
*router.urls,
]