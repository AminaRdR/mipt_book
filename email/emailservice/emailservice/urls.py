"""
URL configuration for emailservice project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path

from mainemail.views import \
    index_kafka_send, \
    index_kafka_get, \
    send_test, \
    index_kafka_registration, \
    send_email, \
    make_pdf_for_user_booking, \
    send_email_booking

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('send_test/', send_test),
    path('send_email/', send_email),
    path('send_email_booking/', send_email_booking),
    # path('send_weekly/', send_weekly),
    path('make_pdf/', make_pdf_for_user_booking),
    path('kafka_start/', index_kafka_send),
    path('kafka_get/', index_kafka_get),
    path('kafka_registration/', index_kafka_registration),
]
