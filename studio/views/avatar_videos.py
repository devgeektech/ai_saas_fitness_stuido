from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib import messages
from studio.forms.forms import AvatarVideoForm
from studio.models import AvatarVideo
from utils.constants import AVATAR_VIDEO_CREATED_SUCCESS, AVATAR_VIDEO_DELETED_SUCCESS, AVATAR_VIDEO_NOT_FOUND, AVATAR_VIDEO_UPDATED_SUCCESS, ERROR, FALSE, FORM, INVALID_FORM_DATA, INVALID_REQUEST_METHOD, MESSAGE, RETURN_URL, SOMETHING_WENT_WRONG, SUCCESS, TRUE
from django_serverside_datatable.views import ServerSideDatatableView


@login_required(login_url='admin-login')
def index(request):

    try:
        context = {}
        return render(request, "studio/avatar-videos/index.html", context)

    except Exception as ex:
        messages.error(request, ex)
        context = {ERROR: str(ex),RETURN_URL: "/studio/avatar-videos"}
        return render(request, "500.html", context)



class AvatarVideosListView(ServerSideDatatableView):

    columns = [
        "uuid",
        "segment",
        "avatar_id",
        "status",
        "created_at",
    ]

    def get_queryset(self):
        queryset = AvatarVideo.objects.all()
        return queryset



@login_required(login_url="admin-login")
def create(request):

    try:
        if request.method == "POST":
            form = AvatarVideoForm(request.POST)
            if form.is_valid():
                obj = form.save(commit=FALSE)
                obj.studio = request.user.studio
                obj.user = request.user
                obj.save()

                messages.success(request, AVATAR_VIDEO_CREATED_SUCCESS)
                return redirect("avatar-videos-index")

            else:
                messages.error(request, INVALID_FORM_DATA)
                return render(request, "studio/avatar-videos/create.html", {"form": form})

        form = AvatarVideoForm()
        return render(request, "studio/avatar-videos/create.html", {"form": form})

    except Exception as ex:
        messages.error(request, f"Error: {str(ex)}")
        return render(request, "500.html", {ERROR: str(ex), RETURN_URL: "/studio/avatar-videos/create"})



@login_required(login_url="admin-login")
def edit(request, uuid):

    try:

        avatar_obj = AvatarVideo.objects.filter(uuid=uuid).first()

        if not avatar_obj:
            messages.error(request, AVATAR_VIDEO_NOT_FOUND)
            return redirect("avatar-videos-index")


        if request.method == "POST":
            form = AvatarVideoForm(
                request.POST,
                instance=avatar_obj
            )

            if form.is_valid():
                obj = form.save(commit=FALSE)
                obj.studio = request.user.studio
                obj.user = request.user
                obj.save()

                messages.success(request, AVATAR_VIDEO_UPDATED_SUCCESS)
                return redirect("avatar-videos-index")

            messages.error(request, INVALID_FORM_DATA)
            return render(request, "studio/avatar-videos/edit.html", {FORM: form,"avatar_obj": avatar_obj})

        form = AvatarVideoForm(instance=avatar_obj)
        return render(request, "studio/avatar-videos/edit.html", {FORM: form, "avatar_obj": avatar_obj})

    except Exception as ex:
        messages.error(request, SOMETHING_WENT_WRONG)
        return render(request, "500.html", {ERROR: str(ex), RETURN_URL: "/studio/avatar-videos/list"})



@login_required(login_url="admin-login")
def view(request, uuid):

    try:
        avatar_obj = AvatarVideo.objects.filter(
            uuid=uuid
        ).first()

        if not avatar_obj:
            messages.error(request, AVATAR_VIDEO_NOT_FOUND)
            return redirect("avatar-videos-index")

        return render(
            request, "studio/avatar-videos/view.html", {"avatar_obj": avatar_obj})

    except Exception as ex:
        messages.error(request, "Something went wrong")
        return render(request, "500.html", {ERROR: str(ex), RETURN_URL: "/studio/avatar-videos/list"})



@login_required(login_url="admin-login")
def delete(request, uuid):

    try:

        if request.method == "POST":
            avatar_obj = AvatarVideo.objects.filter(
                uuid=uuid
            ).first()

            if not avatar_obj:
                return JsonResponse({SUCCESS: FALSE, ERROR: AVATAR_VIDEO_NOT_FOUND})

            avatar_obj.delete()
            return JsonResponse({SUCCESS: TRUE, MESSAGE: AVATAR_VIDEO_DELETED_SUCCESS})

        return JsonResponse({SUCCESS: FALSE, ERROR: INVALID_REQUEST_METHOD})

    except Exception as ex:

        return JsonResponse({SUCCESS: FALSE, ERROR: str(ex)})