from django.urls import path
from . import tryyy

urlpatterns = [
    path('',tryyy.index, name ="index"),
    path('video_feed', tryyy.video_feed, name='video_feed'),
               ]