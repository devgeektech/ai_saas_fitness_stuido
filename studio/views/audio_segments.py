from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib import messages
from studio.forms.forms import AudioSegmentForm
from studio.models import AudioSegment
from utils.constants import (
    ERROR,
    FALSE,
    FORM,
    INVALID_FORM_DATA,
    INVALID_REQUEST_METHOD,
    MESSAGE,
    RETURN_URL,
    SOMETHING_WENT_WRONG,
    SUCCESS,
    TRUE,

    AUDIO_SEGMENT_CREATED_SUCCESS,
    AUDIO_SEGMENT_UPDATED_SUCCESS,
    AUDIO_SEGMENT_DELETED_SUCCESS,
    AUDIO_SEGMENT_NOT_FOUND,
)
from django_serverside_datatable.views import ServerSideDatatableView


@login_required(login_url='admin-login')
def index(request):

    try:
        context = {}
        return render(request, "studio/audio-segments/index.html", context)
    except Exception as ex:
        messages.error(request, ex)
        context = {
            ERROR: str(ex),
           RETURN_URL: "/studio/audio-segments"
        }
        return render(request, "500.html", context)



class AudioSegmentsListView(ServerSideDatatableView):

    columns = [
        "uuid",
        "segment",
        "voice_id",
        "duration",
        "status",
        "created_at",
    ]

    def get_queryset(self):
        queryset = AudioSegment.objects.all()
        return queryset



@login_required(login_url="admin-login")
def create(request):

    try:
        if request.method == "POST":
            form = AudioSegmentForm(request.POST)
            if form.is_valid():
                obj = form.save(commit=FALSE)
                obj.studio = request.user.studio
                obj.user = request.user
                obj.save()

                messages.success(request, "Audio segment created successfully")
                return redirect("audio-segments-index")
            else:
                messages.error(request, "Invalid form data")
                return render(request,"studio/audio-segments/create.html",{FORM: form})

        form = AudioSegmentForm()
        return render(request, "studio/audio-segments/create.html", {FORM: form})

    except Exception as ex:
        messages.error(request, f"Error: {str(ex)}")
        return render(request, "500.html", {ERROR: str(ex), RETURN_URL: "/studio/audio-segments/create"})



@login_required(login_url="admin-login")
def edit(request, uuid):

    try:

        audio_obj = AudioSegment.objects.filter(uuid=uuid).first()

        if not audio_obj:
            messages.error(request, AUDIO_SEGMENT_NOT_FOUND)
            return redirect("audio-segments-index")


        if request.method == "POST":
            form = AudioSegmentForm(
                request.POST,
                instance=audio_obj
            )
            if form.is_valid():
                obj = form.save(commit=FALSE)
                obj.studio = request.user.studio
                obj.user = request.user
                obj.save()

                messages.success(request, AUDIO_SEGMENT_UPDATED_SUCCESS)
                return redirect("audio-segments-index")
            
            messages.error(request, INVALID_FORM_DATA)
            return render(request, "studio/audio-segments/edit.html", {FORM: form, "audio_obj": audio_obj})

        form = AudioSegmentForm(instance=audio_obj)
        return render(request, "studio/audio-segments/edit.html",{FORM: form, "audio_obj": audio_obj})

    except Exception as ex:
        messages.error(request, SOMETHING_WENT_WRONG)
        return render(request, "500.html", {ERROR: str(ex), RETURN_URL: "/studio/audio-segments/list"})



@login_required(login_url="admin-login")
def view(request, uuid):

    try:
        audio_obj = AudioSegment.objects.filter(uuid=uuid).first()
        if not audio_obj:
            messages.error(request, AUDIO_SEGMENT_NOT_FOUND)
            return redirect("audio-segments-index")

        return render(request, "studio/audio-segments/view.html", {"audio_obj": audio_obj})

    except Exception as ex:
        messages.error(request, SOMETHING_WENT_WRONG)
        return render(request, "500.html", {ERROR: str(ex), RETURN_URL: "/studio/audio-segments/list"})



@login_required(login_url="admin-login")
def delete(request, uuid):

    try:

        if request.method == "POST":

            audio_obj = AudioSegment.objects.filter(uuid=uuid).first()
            if not audio_obj:
                return JsonResponse({SUCCESS: FALSE, ERROR: AUDIO_SEGMENT_NOT_FOUND})
            
            audio_obj.delete()
            return JsonResponse({SUCCESS: TRUE, MESSAGE: AUDIO_SEGMENT_DELETED_SUCCESS})

        return JsonResponse({ SUCCESS: FALSE, ERROR: INVALID_REQUEST_METHOD})

    except Exception as ex:
        return JsonResponse({SUCCESS: FALSE, ERROR: str(ex)})