from django.urls import path, re_path

from . import views


urlpatterns = [
    path('<int:task_pk>/<int:step_pk>/', views.step_detail, name='step'),
    path('<int:pk>/', views.task_detail, name='detail'),
    path('traffic/', views.traffic_task, name='traffic'),
    path('conversion-rate/', views.conversion_rate_task, name='conversionrate'),
    path('marketing/', views.marketing_task, name='marketing'),
    path('done/<int:pk>/', views.task_done, name='finish_task')
]