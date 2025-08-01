import uuid
import os
import threading
from django.views import View
from django.shortcuts import render, redirect
from django.conf import settings
from Scripts.youtube_downloader import download_youtube_video


class YouTubeDownloadView(View):
    def get(self, request):
        return render(request, "main/download_form.html")

    def post(self, request):
        url = request.POST.get("url")
        if not url:
            return redirect("main:link_form")

        filename = f"{uuid.uuid4().hex}.mp4"
        temp_dir = os.path.join(settings.MEDIA_ROOT, "tmp")
        os.makedirs(temp_dir, exist_ok=True)
        output_path = os.path.join(temp_dir, filename)

        try:
            request.session["downloaded_filename"] = filename
            download_youtube_video(url, output_path, f"{settings.BASE_DIR}/cookies/cookies.txt")

            return redirect("main:success_page")

        except Exception as e:
            print("[Ошибка загрузки]", e)
            return redirect("main:link_form")


class DownloadSuccessView(View):
    def get(self, request):
        filename = request.session.get("downloaded_filename")
        if not filename:
            return redirect("main:link_form")

        file_url = f"{settings.MEDIA_URL}tmp/{filename}"

        path = os.path.join(settings.MEDIA_ROOT, "tmp", filename)
        threading.Timer(10, lambda: os.remove(path)).start()

        return render(request, "main/success.html", {"file_url": file_url})
