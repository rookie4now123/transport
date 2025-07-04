from rest_framework import routers
from .user.viewsets import UserViewSet, MonitorUserViewSet
from station.viewsets import StationViewSet
from route.viewsets import RouteViewSet
from django.urls import path, include
from .auth.viewsets import (
    WebLoginViewSet,
    MonitorLoginViewSet,
    WebRegisterViewSet,
    RefreshViewSet
)
from tracking.viewsets import(
    MobileRouteRunViewSet,
    MobileLocationPointViewSet,
    WebRouteRunViewSet,
    WebLocationPointViewSet
)
from tracking.views import location_stream
from student.viewsets import StudentViewSet

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
router.register(r'student', StudentViewSet, basename='student')

router.register(r'routeruns', WebRouteRunViewSet, basename='web-routerun')
router.register(r'locationpoints', WebLocationPointViewSet, basename='web-locationpoint')

router.register(r'auth/register', WebRegisterViewSet, basename='web-register')
router.register(r'auth/login', WebLoginViewSet, basename='web-login')
router.register(r'auth/refresh', RefreshViewSet, basename='auth-refresh')

monitor_router = routers.SimpleRouter()

monitor_router.register(r'routeruns', MobileRouteRunViewSet, basename='mobile-routerun')
monitor_router.register(r'locationpoints', MobileLocationPointViewSet, basename='mobile-locationpoint')
monitor_router.register(r'auth/login', MonitorLoginViewSet, basename='mobile-login')


urlpatterns = [
path('', include(router.urls)),
path('monitor/', include(monitor_router.urls)),
#*router.urls,
path('location-stream/', location_stream, name='location-stream')
]