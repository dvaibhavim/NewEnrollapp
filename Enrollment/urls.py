"""Enrollment URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from Enrollapp.views import register, create_account_NDS,success, handle404,old_user_update, create_account_CHSS
from django.conf.urls import url,include
from django.views.generic import TemplateView
from django.conf.urls import handler404
handler404 = handle404

import os
urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', create_account_NDS, name = "autocomplete"),
    path('register/Enroll',create_account_NDS),
    path('CHSS/',create_account_CHSS, name="autocomplete"),
    path('CHSS/Enroll',create_account_CHSS),
    path('success',success),
    path('register/Enroll_user', old_user_update, name="autocomplete"),
    path('register/Enroll_user/Update',TemplateView.as_view(template_name=os.path.join("enrollapp","update_school_verify.html"))),
]


