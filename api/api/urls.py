"""api URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from v1.registration import urls as registration_urls
from v1.campaign import urls as campaign_urls
from v1.survey import urls as survey_urls
from v1.utility import urls as utility_urls
from v1.consumer import urls as consumer_urls
from v1.commonapp import urls as common_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include(common_urls)),
    path('api/v1/registration/', include(registration_urls)),
    path('api/v1/campaign/', include(campaign_urls)),
    path('api/v1/survey/', include(survey_urls)),
    path('api/v1/utilities/', include(utility_urls)),
    path('api/v1/tenant/', include(tenant_urls)),
    path('api/v1/consumer/', include(consumer_urls)),
]
