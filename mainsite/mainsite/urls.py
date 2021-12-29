"""mainsite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.urls import path,include
from dashboard import views
from django.conf import Settings, settings
from django.conf.urls.static import static

urlpatterns = [
    #path('', views.license_detail,name='license_detail'),
    path('', views.home,name='home'),
    path('home/', views.home,name='home'),
    path('login/', views.api_login,name='api_login'),
    path('account_info/', views.account_info,name='account_info'),
    path('api_token_info/',views.api_token_info,name='api_token_info'),
    path('license_detail/', views.license_detail, name='license_detail'),
    path('admin_user/', views.admin_user, name='admin_user'),
    path('standard_user/', views.standard_user, name='standard_user'),
    path('data_export_csv/',views.data_export_csv,name='data_export_csv'),
    path('admin/', admin.site.urls),
    path('__debug__/', include('debug_toolbar.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


    