from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib import messages
from django_serverside_datatable.views import ServerSideDatatableView
from studio.forms.forms import ClassSegmentForm
from studio.models import ClassSegment
from utils.constants import CLASS_SEGMENT_CREATED_SUCCESSFULLY, CLASS_SEGMENT_UPDATED_SUCCESSFULLY, ERROR, FALSE, FORM, INVALID_FORM_DATA, INVALID_REQUEST_METHOD, MESSAGE, RETURN_URL, SEGMENT_NOT_FOUND, SUCCESS, TRUE


# INDEX
@login_required(login_url='admin-login')
def index(request):

    try:
        context = {}
        return render(request, "studio/class-segments/index.html", context)
    except Exception as ex:
        messages.error(request, ex)
        context = {
            ERROR: str(ex),
            RETURN_URL: "/studio/class-segments"
        }
        return render(request, "500.html", context)


# LIST VIEW
class ClassSegmentsListView(ServerSideDatatableView):

    columns = [
        "uuid",
        "title",
        "segment_type",
        "duration",
        "order",
        "created_at"
    ]

    def get_queryset(self):
        queryset = ClassSegment.objects.all()
        return queryset


# CREATE
@login_required(login_url="admin-login")
def create(request):

    try:
        if request.method == "POST":
            form = ClassSegmentForm(request.POST)
            if form.is_valid():
                obj = form.save(commit=False)
                obj.studio = request.user.studio
                obj.user = request.user
                obj.save()
                
                messages.success(request, CLASS_SEGMENT_CREATED_SUCCESSFULLY)
                return redirect("class-segments-index")

            else:
                messages.error(request, INVALID_FORM_DATA)
                return render(request, "studio/class-segments/create.html",
                    {
                        FORM: form
                    }
                )

        form = ClassSegmentForm()
        return render(request, "studio/class-segments/create.html",
            {
                FORM: form
            }
        )

    except Exception as ex:
        messages.error(request, f"Error: {str(ex)}")
        return render( request, "500.html",
            {
                ERROR: str(ex),
                RETURN_URL: "/studio/class-segments/create"
            }
        )


# EDIT
@login_required(login_url="admin-login")
def edit(request, uuid):

    try:

        segment_obj = ClassSegment.objects.filter(uuid=uuid).first()

        if not segment_obj:
            messages.error(request, SEGMENT_NOT_FOUND)
            return redirect("class-segments-index")

        if request.method == "POST":

            form = ClassSegmentForm(request.POST, instance=segment_obj)

            if form.is_valid():
                obj = form.save(commit=False)
                obj.studio = request.user.studio
                obj.user = request.user
                obj.save()
                
                messages.success(request, CLASS_SEGMENT_UPDATED_SUCCESSFULLY)
                return redirect("class-segments-index")

            messages.error(request, INVALID_FORM_DATA)
            return render(request, "studio/class-segments/edit.html",
                {
                    FORM: form,
                    "segment_obj": segment_obj
                }
            )

        form = ClassSegmentForm(instance=segment_obj)
        return render(request, "studio/class-segments/edit.html",
            {
                FORM: form,
                "segment_obj": segment_obj
            }
        )

    except Exception as ex:
        messages.error(request, "Something went wrong")
        return render(request, "500.html",
            {
                "error": str(ex),
                "return_url": "/studio/class-segments"
            }
        )


# VIEW
@login_required(login_url="admin-login")
def view(request, uuid):

    try:

        segment_obj = ClassSegment.objects.filter(
            uuid=uuid
        ).first()

        if not segment_obj:
            messages.error(request, "Segment not found.")
            return redirect("class-segments-index")

        return render(
            request,
            "studio/class-segments/view.html",
            {
                "segment_obj": segment_obj
            }
        )

    except Exception as ex:
        messages.error(request, "Something went wrong")
        return render(
            request,
            "500.html",
            {
                "error": str(ex),
                "return_url": "/studio/class-segments"
            }
        )


# DELETE
@login_required(login_url="admin-login")
def delete(request, uuid):

    try:

        if request.method == "POST":
            segment_obj = ClassSegment.objects.filter(
                uuid=uuid
            ).first()

            if not segment_obj:
                return JsonResponse({
                    "success": False,
                    "error": "Segment not found"
                })

            segment_obj.delete()
            return JsonResponse({
                "success": True,
                "message": "Class segment deleted successfully"
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