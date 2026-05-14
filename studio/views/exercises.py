from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib import messages
from django_serverside_datatable.views import ServerSideDatatableView
from studio.forms.forms import ExerciseForm
from studio.models import Exercise
from utils.constants import ERROR, EXERCISE_CREATED_SUCCESSFULLY, EXERCISE_DELETED_SUCCESSFULLY, EXERCISE_NOT_FOUND, EXERCISE_UPDATED_SUCCESSFULLY, FALSE, FORM, INVALID_FORM_DATA, INVALID_REQUEST_METHOD, MESSAGE, RETURN_URL, SUCCESS, TRUE
import logging

logger = logging.getLogger(__name__)


# index page
@login_required(login_url='admin-login')
def index(request):
    try:
        return render(request, "studio/exercises/index.html")

    except Exception as ex:
        messages.error(request, str(ex))
        return render(request, "500.html", {
            ERROR: str(ex),
            RETURN_URL: "/studio/exercises"
        })


# listing
class ExercisesListView(ServerSideDatatableView):

    columns = [
        "uuid",
        "name",
        "category",
        "difficulty",
        "muscle_group",
        "status",
        "created_at"
    ]

    def get_queryset(self):

        queryset = Exercise.objects.all().order_by("-created_at")
        return queryset


# create
@login_required(login_url="admin-login")
def create(request):

    try:
        if request.method == "POST":
            form = ExerciseForm(
                request.POST,
                request.FILES
            )
            if form.is_valid():
                obj = form.save(commit=False)
                obj.studio = request.user.studio
                obj.user = request.user
                obj.save()
                
                
                messages.success(request, EXERCISE_CREATED_SUCCESSFULLY)
                return redirect("exercises-index")
            messages.error(request, INVALID_FORM_DATA)
            return render(request, "studio/exercises/create.html", {
                FORM: form
            })
        form = ExerciseForm()
        return render(request, "studio/exercises/create.html", {
            FORM: form
        })
    except Exception as ex:
        messages.error(request, str(ex))
        return render(request, "500.html", {
            ERROR: str(ex),
            RETURN_URL: "/studio/exercises/create"
        })


# edit excercise
@login_required(login_url="admin-login")
def edit(request, uuid):

    try:
        exercise_obj = Exercise.objects.filter(
            uuid=uuid
        ).first()
        if not exercise_obj:
            messages.error(request, EXERCISE_NOT_FOUND)
            return redirect("exercises-index")

        if request.method == "POST":
            form = ExerciseForm(
                request.POST,
                request.FILES,
                instance=exercise_obj
            )
            if form.is_valid():
                obj = form.save(commit=False)
                obj.studio = request.user.studio
                obj.user = request.user
                obj.save()
                
                messages.success(request, EXERCISE_UPDATED_SUCCESSFULLY)
                return redirect("exercises-index")
            messages.error(request, INVALID_FORM_DATA)
            return render(request, "studio/exercises/edit.html", {
                FORM: form,
                "exercise_obj": exercise_obj
            })

        form = ExerciseForm(instance=exercise_obj)
        return render(request, "studio/exercises/edit.html", {
            FORM: form,
            "exercise_obj": exercise_obj
        })
    except Exception as ex:
        messages.error(request, str(ex))
        return render(request, "500.html", {
            ERROR: str(ex),
            RETURN_URL: "/studio/exercises"
        })


# view
@login_required(login_url="admin-login")
def view(request, uuid):

    try:
        exercise_obj = Exercise.objects.filter(
            uuid=uuid
        ).first()
        if not exercise_obj:
            messages.error(request, EXERCISE_NOT_FOUND)
            return redirect("exercises-index")
        return render(request, "studio/exercises/view.html", {
            "exercise_obj": exercise_obj
        })
    except Exception as ex:
        messages.error(request, str(ex))
        return render(request, "500.html", {
            ERROR: str(ex),
            RETURN_URL: "/studio/exercises"
        })


# delete
@login_required(login_url="admin-login")
def delete(request, uuid):

    try:

        if request.method == "POST":
            exercise_obj = Exercise.objects.filter(
                uuid=uuid
            ).first()
            
            if not exercise_obj:
                return JsonResponse({
                    SUCCESS: FALSE,
                    ERROR: EXERCISE_NOT_FOUND
                })

            exercise_obj.delete()
            return JsonResponse({
                SUCCESS: TRUE,
                MESSAGE: EXERCISE_DELETED_SUCCESSFULLY
            })

        return JsonResponse({
            SUCCESS: FALSE,
            ERROR: INVALID_REQUEST_METHOD
        })

    except Exception as ex:
        return JsonResponse({
            SUCCESS: FALSE,
            ERROR: str(ex)
        })