"""
URL configuration for main_app project.

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
from django.urls import path, include

admin.site.site_header = "SRB Admin"
admin.site.site_title = "SRB Admin Portal"
admin.site.index_title = "Welcome to SRB Admin Portal"

urlpatterns = [
    path("admin/", admin.site.urls),
    path('dj-rest-auth/', include('dj_rest_auth.urls')),
    # path('dj-rest-auth/registration/verify-email/',
        #  VerifyEmailView.as_view(), name='account_email_verification_sent'),
    # path('accounts/', include('allauth.urls')),
    # path('dj-rest-auth/password/reset/confirm/<uidb64>/<token>/',
        #  PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    # path('dj-rest-auth/facebook/', views.FacebookLogin.as_view(), name='fb_login'),
    path('dj-rest-auth/registration/', include('dj_rest_auth.registration.urls')),
    path("", include("myapp.urls"))
]
