from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib import messages
from studio.forms.forms import AudioSegmentForm
from studio.models import AudioSegment
from utils.constants import ERROR, FALSE, FORM, INVALID_FORM_DATA, INVALID_REQUEST_METHOD, MESSAGE, RETURN_URL, SUCCESS, TRUE
from django_serverside_datatable.views import ServerSideDatatableView


@login_required(login_url='admin-login')
def index(request):

    try:

        context = {}

        return render(
            request,
            "studio/audio-segments/index.html",
            context
        )

    except Exception as ex:

        messages.error(request, ex)

        context = {
            ERROR: str(ex),
            "return_url": "/studio/audio-segments"
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

                obj = form.save(commit=False)
                obj.studio = request.user.studio
                obj.user = request.user
                obj.save()

                messages.success(
                    request,
                    "Audio segment created successfully"
                )

                return redirect("audio-segments-index")

            else:

                messages.error(request, "Invalid form data")

                return render(
                    request,
                    "studio/audio-segments/create.html",
                    {
                        "form": form
                    }
                )

        form = AudioSegmentForm()

        return render(
            request,
            "studio/audio-segments/create.html",
            {
                "form": form
            }
        )

    except Exception as ex:

        messages.error(request, f"Error: {str(ex)}")

        return render(
            request,
            "500.html",
            {
                "error": str(ex),
                "return_url": "/studio/audio-segments/create"
            }
        )



@login_required(login_url="admin-login")
def edit(request, uuid):

    try:

        audio_obj = AudioSegment.objects.filter(
            uuid=uuid
        ).first()

        if not audio_obj:

            messages.error(request, "Audio segment not found.")

            return redirect("audio-segments-index")


        if request.method == "POST":

            form = AudioSegmentForm(
                request.POST,
                instance=audio_obj
            )

            if form.is_valid():

                obj = form.save(commit=False)
                obj.studio = request.user.studio
                obj.user = request.user
                obj.save()

                messages.success(
                    request,
                    "Audio segment updated successfully"
                )

                return redirect("audio-segments-index")

            messages.error(request, "Invalid form data")

            return render(
                request,
                "studio/audio-segments/edit.html",
                {
                    "form": form,
                    "audio_obj": audio_obj
                }
            )

        form = AudioSegmentForm(instance=audio_obj)

        return render(
            request,
            "studio/audio-segments/edit.html",
            {
                "form": form,
                "audio_obj": audio_obj
            }
        )

    except Exception as ex:

        messages.error(request, "Something went wrong")

        return render(
            request,
            "500.html",
            {
                "error": str(ex),
                "return_url": "/studio/audio-segments/list"
            }
        )



@login_required(login_url="admin-login")
def view(request, uuid):

    try:

        audio_obj = AudioSegment.objects.filter(
            uuid=uuid
        ).first()

        if not audio_obj:

            messages.error(request, "Audio segment not found.")

            return redirect("audio-segments-index")

        return render(
            request,
            "studio/audio-segments/view.html",
            {
                "audio_obj": audio_obj
            }
        )

    except Exception as ex:

        messages.error(request, "Something went wrong")

        return render(
            request,
            "500.html",
            {
                "error": str(ex),
                "return_url": "/studio/audio-segments/list"
            }
        )



@login_required(login_url="admin-login")
def delete(request, uuid):

    try:

        if request.method == "POST":

            audio_obj = AudioSegment.objects.filter(
                uuid=uuid
            ).first()

            if not audio_obj:

                return JsonResponse({
                    "success": False,
                    "error": "Audio segment not found"
                })

            audio_obj.delete()

            return JsonResponse({
                "success": True,
                "message": "Audio segment deleted successfully"
            })

        return JsonResponse({
            "success": False,
            "error": "Invalid request method"
        })

    except Exception as ex:

        return JsonResponse({
            "success": False,
            "error": str(ex)
        })