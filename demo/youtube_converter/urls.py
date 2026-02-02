from django.urls import path
from . import views

app_name='youtube_converter'
urlpatterns = [

    path('', views.homepage, name='homepage'),
    path('download_video/', views.download_video, name='download_video'),
]