from django.shortcuts import render, redirect
from django.views import View
from django.conf import settings
import os
import uuid
import threading
from django.http import FileResponse
from Scripts.youtube_downloader import download_youtube_video
from YouTubeDownload.settings import BASE_DIR


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

        temp_dir = os.path.join(settings.MEDIA_ROOT, "tmp")
        os.makedirs(temp_dir, exist_ok=True)

        # Уникальное имя
        filename = f"{uuid.uuid4().hex}.mp4"
        output_path = os.path.join(temp_dir, filename)

        try:
            # Скачиваем
            download_youtube_video(url, output_path, "cookies.txt")

            # Готовим ответ
            response = FileResponse(open(output_path, 'rb'), content_type='video/mp4')
            response['Content-Disposition'] = f'attachment; filename="video.mp4"'

            # Удаление через 60 сек.
            def delete_file(path):
                try:
                    os.remove(path)
                    print(f"Удалён файл: {path}")
                except Exception as e:
                    print(f"Ошибка при удалении: {e}")

            threading.Timer(60, delete_file, args=[output_path]).start()

            return response

        except Exception as e:
            return redirect("main:link_form")  # или показать ошибку

