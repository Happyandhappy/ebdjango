"""ebdjango URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.urls import include, path
from . import views
from account import views as account_views
from payment import views as payment_views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib.auth import views as auth_views
from django.conf.urls import url, include

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/', include('account.urls', namespace='accounts')),
    path('register/', account_views.RegisterFormView.as_view(), name='register'),
    path('login/', auth_views.LoginView.as_view(template_name="account/login.html"), name="login"),
    path('reset-password/', auth_views.PasswordResetView.as_view(template_name="registration/password_reset_form.html"),
         name="reset"),
    path('logout/', views.logout_view, name='logout'),
    path('tasks/', include('dailytask.urls')),
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('payment/', include('payment.urls')),
]
# ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += staticfiles_urlpatterns()
