from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib import messages
from studio.forms.forms import AvatarVideoForm
from studio.models import AvatarVideo
from utils.constants import ERROR, FALSE, FORM, INVALID_FORM_DATA, INVALID_REQUEST_METHOD, MESSAGE, RETURN_URL, SUCCESS, TRUE
from django_serverside_datatable.views import ServerSideDatatableView


@login_required(login_url='admin-login')
def index(request):

    try:
        context = {}
        return render(
            request,
            "studio/avatar-videos/index.html",
            context
        )

    except Exception as ex:
        messages.error(request, ex)
        context = {
            ERROR: str(ex),
            "return_url": "/studio/avatar-videos"
        }
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
                obj = form.save(commit=False)
                obj.studio = request.user.studio
                obj.user = request.user
                obj.save()

                messages.success(
                    request,
                    "Avatar video created successfully"
                )
                return redirect("avatar-videos-index")

            else:

                messages.error(request, "Invalid form data")
                return render(
                    request,
                    "studio/avatar-videos/create.html",
                    {
                        "form": form
                    }
                )

        form = AvatarVideoForm()
        return render(
            request,
            "studio/avatar-videos/create.html",
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
                "return_url": "/studio/avatar-videos/create"
            }
        )



@login_required(login_url="admin-login")
def edit(request, uuid):

    try:

        avatar_obj = AvatarVideo.objects.filter(
            uuid=uuid
        ).first()

        if not avatar_obj:
            messages.error(request, "Avatar video not found.")
            return redirect("avatar-videos-index")


        if request.method == "POST":
            form = AvatarVideoForm(
                request.POST,
                instance=avatar_obj
            )

            if form.is_valid():
                obj = form.save(commit=False)
                obj.studio = request.user.studio
                obj.user = request.user
                obj.save()

                messages.success(
                    request,
                    "Avatar video updated successfully"
                )
                return redirect("avatar-videos-index")

            messages.error(request, "Invalid form data")
            return render(
                request,
                "studio/avatar-videos/edit.html",
                {
                    "form": form,
                    "avatar_obj": avatar_obj
                }
            )

        form = AvatarVideoForm(instance=avatar_obj)
        return render(
            request,
            "studio/avatar-videos/edit.html",
            {
                "form": form,
                "avatar_obj": avatar_obj
            }
        )

    except Exception as ex:
        messages.error(request, "Something went wrong")
        return render(
            request,
            "500.html",
            {
                "error": str(ex),
                "return_url": "/studio/avatar-videos/list"
            }
        )



@login_required(login_url="admin-login")
def view(request, uuid):

    try:
        avatar_obj = AvatarVideo.objects.filter(
            uuid=uuid
        ).first()

        if not avatar_obj:
            messages.error(request, "Avatar video not found.")
            return redirect("avatar-videos-index")

        return render(
            request,
            "studio/avatar-videos/view.html",
            {
                "avatar_obj": avatar_obj
            }
        )

    except Exception as ex:
        messages.error(request, "Something went wrong")
        return render(
            request,
            "500.html",
            {
                "error": str(ex),
                "return_url": "/studio/avatar-videos/list"
            }
        )



@login_required(login_url="admin-login")
def delete(request, uuid):

    try:

        if request.method == "POST":
            avatar_obj = AvatarVideo.objects.filter(
                uuid=uuid
            ).first()

            if not avatar_obj:
                return JsonResponse({
                    "success": False,
                    "error": "Avatar video not found"
                })

            avatar_obj.delete()
            return JsonResponse({
                "success": True,
                "message": "Avatar video deleted successfully"
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