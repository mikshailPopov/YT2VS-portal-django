from django.shortcuts import render
from django.http import FileResponse
from zipfile import ZipFile
from .forms import UrlForm
from urllib.parse import urlparse, parse_qs
from os import listdir
from os.path import isfile, join
import os
import yt_dlp


audio_formats = ['mp3']
video_formats = ['mp4']

format_options = audio_formats + video_formats


def homepage(request):
    context = {
        "format_options": format_options,
    }
    return render(request, "homepage/home_page.html", context)


def download_video(request):

    context = {
        "format_options": format_options,
        "form": UrlForm(),
    }
    if request.method == "POST":
        form = UrlForm(request.POST)
        if form.is_valid():
            BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            filepath = BASE_DIR+"/youtube_converter/files/"

            files_del = [f for f in listdir(filepath) if isfile(join(filepath, f))]
            # print(files_del)
            for i in range(len(files_del)):
                os.remove(filepath+files_del[i])

            # yt-dlp convert
            # info = ""
            link = request.POST.get("youtube_url", "")
            youtube_format = request.POST.get("formats", "")
            ydl_opts = {}

            parsed_url = urlparse(link)
            query_params = parse_qs(parsed_url.query)
            is_playlist = "list" in query_params

            if youtube_format in audio_formats:
                ydl_opts = {
                    'format': 'bestaudio/best',
                    'outtmpl': f'{BASE_DIR}/youtube_converter/files/%(title)s',
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': f'{youtube_format}',  # Convert audio to MP3
                        'preferredquality': '192',  # Audio quality (bitrate)
                    }],
                }
            elif youtube_format in video_formats:
                ydl_opts = {
                    'format': f'bestvideo[ext={youtube_format}]+bestaudio[ext={youtube_format}]/best[ext={youtube_format}]',
                    'outtmpl': f'{BASE_DIR}/youtube_converter/files/%(title)s.{youtube_format}',
                    'merge_output_format': youtube_format,  # Ensures output is MP4
                }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([link])
                info = ydl.extract_info(link, download=False)

            # handling zip file (for playlists)
            if is_playlist:
                filenames = []
                for root, directories, files in os.walk(filepath):
                    for filename in files:
                        filenames.append(filename)

                with ZipFile(f'{filepath}{info["title"]}.zip', 'a') as zip:
                    for filename in filenames:
                        absname = os.path.abspath(os.path.join(filepath, filename))
                        arcname = absname[len(filepath):]
                        zip.write(absname,arcname)

                filename = f"{info['title']}.zip"
                response = FileResponse(open(os.path.join(filepath, filename), "rb"), as_attachment=True)
                return response

            else:
                onlyfiles = [f for f in listdir(filepath) if isfile(join(filepath, f))]
                response = FileResponse(open(os.path.join(filepath, onlyfiles[0]), "rb"), as_attachment=True)
                return response
    return render(request, "homepage/home_page.html", context)
