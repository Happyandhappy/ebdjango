from django.contrib import admin
from django.conf.urls import url
from django.urls import include, path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('', views.RegisterFormView.as_view(), name='register'),
    url(r'^profile/$', views.view_profile, name='view_profile' ),
    url(r'^profile/(?P<pk>\d+)/$', views.view_profile, name='view_profile_with_pk'),
    url(r'^profile/edit/$', views.edit_profile, name='edit_profile'),
    url(r'^profile/password/$', views.change_password, name='change_password'),
    url(r'^profile/settimezone/$', views.setTimeZone, name='setTimezone'),
]