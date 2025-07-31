from django.urls import path

from .views import YouTubeDownloadView, YouTubeProcessingView

app_name = 'main'

urlpatterns = [
    path('', YouTubeDownloadView.as_view(), name='link_form'),
    path('processing/', YouTubeProcessingView.as_view(), name='youtube_processing')
]

