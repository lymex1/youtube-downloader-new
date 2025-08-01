from django.urls import path

from .views import YouTubeDownloadView, DownloadSuccessView

app_name = 'main'

urlpatterns = [
    path('', YouTubeDownloadView.as_view(), name='link_form'),
    path("success/", DownloadSuccessView.as_view(), name="success_page"),
]

