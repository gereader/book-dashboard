from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('reading-stats/', views.reading_stats, name='reading-stats'),
]