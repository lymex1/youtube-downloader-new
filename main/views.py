from django.shortcuts import render, redirect
from django.views import View
from django.conf import settings
import os

from Scripts.youtube_downloader import download_youtube_video


class YouTubeDownloadView(View):
    template_name = "main/download_form.html"

    def get(self, request):
        return render(request, "main/download_form.html")

    def post(self, request):
        url = request.POST.get("url")
        request.session["url"] = url
        return redirect("main:youtube_processing")

class YouTubeProcessingView(View):
    def get(self, request):
        url = request.session.get("url")
        if not url:
            return redirect("main:link_form")

        output_path = os.path.join(settings.MEDIA_ROOT, "video.mp4")

        try:
            download_youtube_video(url, output_path, "/Users/egorkarinkin/Desktop/VSProjects/Django/YouTubeDownload/YouTubeDownload/cookies/www.youtube.com_cookies.txt")
            return render(request, "main/processing.html", {"ready": True, "filename": "video.mp4"})
        except Exception as e:
            return render(request, "main/processing.html", {"error": str(e)})