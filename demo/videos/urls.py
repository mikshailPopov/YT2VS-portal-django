from django.urls import path
from . import views

urlpatterns = [
    path('', views.convert_history, name='convert_history'),
    path("videos/<int:video_id>/", views.detail, name='detail'),
]