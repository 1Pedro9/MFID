"""
URL configuration for MFID project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from display.views import index, dependents, search, sos, settings, apps, signup, login, insert_member, check_login, logout, add_items, sos_request, chatbot, askbot, problems

urlpatterns = [
    path('', index, name="index"),
    path('dependents/', dependents, name="dependents"),
    path('search/', search, name="search"),
    path('sos/', sos, name="sos"),
    path('settings/', settings, name="settings"),
    path('apps/', apps, name="apps"),
    path('login/', login, name="login"),
    path('signup/', signup, name="signup"),
    path('insert_member/', insert_member, name="insert_member"),
    path('check_login/', check_login, name="check_login"),
    path('logout/', logout, name="logout"),
    path('sos_request/', sos_request, name="sos_request"),
    path('add_items/', add_items, name="add_items"),
    path('chatbot/', chatbot, name="chatbot"),
    path('askbot/', askbot, name="askbot"),
    path('problems/', problems, name="problems"),
    path('admin/', admin.site.urls),
]
