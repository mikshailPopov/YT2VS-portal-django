from re import template
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.template import loader

from .models import Video


def convert_history(request):
    youtube_vid_list = Video.objects.all()
    # template = loader.get_template('videos/index.html')
    context = {
        "youtube_vid_list": youtube_vid_list,
    }
    # return HttpResponse(template.render(context, request))
    # context = {"latest_question_list": latest_question_list}
    return render(request, "videos/index.html", context)

def detail(request, video_id):
    # template = loader.get_template('videos/video_details.html')
    video = get_object_or_404(Video, pk=video_id)

    context = {
        "video_id": video.id,
        "video_url": video.url,
        "video_date": video.date,
    }
    # return HttpResponse(template.render(context, request))
    return render(request, "videos/video_details.html", context)
    # return HttpResponse("You're looking at question %s." % video_id)
