"""backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from main import views
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework import routers
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

# router.register(r'history', views.BookHistoryViewSet)

router = routers.DefaultRouter()
router.register(r'institute', views.InstituteViewSet)
router.register(r'building', views.BuildingViewSet)
router.register(r'audience_status', views.AudienceStatusViewSet)
router.register(r'audience', views.AudienceViewSet)
router.register(r'book', views.BookViewSet)
router.register(r'users_wallet', views.UsersWalletViewSet)
router.register(r'history', views.BookHistoryViewSet)

urlpatterns = [
    path('base-info/', include(router.urls)),
    path('book/', views.book_audience),
    path('stop_booking/', views.index_stop_booking),
    path('timetable/', views.index_timetable),
    path('wallet/', views.index_user_wallet),
    path('admin/', admin.site.urls),
    path('test/', include('test.urls', namespace='test')),
]
urlpatterns += staticfiles_urlpatterns()
