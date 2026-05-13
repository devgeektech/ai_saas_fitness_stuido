from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from authentication.models import User
from django.contrib import messages
from studio.forms.forms import ClassForm
from studio.models import Class, Studio
from utils.constants import (CLASS_CREATED_SUCCESSFULLY, CLASS_DELETED_SUCCESSFULLY, CLASS_NOT_FOUND, CLASS_UPDATED_SUCCESSFULLY, ERROR, FALSE, FORM, INVALID_FORM_DATA, INVALID_REQUEST_METHOD, MESSAGE, RETURN_URL, SOMETHING_WENT_WRONG, STUDIO_NOT_FOUND_FOR_USER, SUCCESS, TRUE)
from django_serverside_datatable.views import ServerSideDatatableView
import logging
from superadmin.views.views import superuser_required
from django.db.models import F, Value, Q
from django.db.models.functions import Concat

logger = logging.getLogger(__name__)

# show Register user agent
@login_required(login_url='admin-login')
def index(request):
    try:
        context = {}
        return render(request, "studio/classes/index.html", context)
    except Exception as ex:
        messages.error(request, ex)        
        context = {ERROR:str(ex),RETURN_URL:"/studio/classes"}
        return render(request,"500.html",context)
    

# Get all class list
class ClassesListView(ServerSideDatatableView):
    columns = [
        "uuid",
        "title",
        "category",
        "difficulty",
        "duration",
        "status",
        "created_at"
    ]

    def get_queryset(self):
        user= self.request.user
        queryset = Class.objects.filter(created_by=user)
        return queryset



#create product
@login_required(login_url="admin-login")
def create(request):
    try:
        if request.method == "POST":
            form = ClassForm(request.POST)

            if form.is_valid():
                obj = form.save(commit=False)

                obj.created_by = request.user
                obj.studio = request.user.studio

                obj.save()

                messages.success(request, CLASS_CREATED_SUCCESSFULLY)
                return redirect("classes-index")

            else:
                messages.error(request, INVALID_FORM_DATA)
                return render(request, "studio/classes/create.html", {
                    FORM: form
                })
                
        form = ClassForm()
        return render(request, "studio/classes/create.html", {
            FORM: form
        })

    except Exception as ex:
        messages.error(request, f"Error: {str(ex)}")
        return render(request, "500.html", {
            ERROR: str(ex),
            RETURN_URL: "/studio/classes/create"
        })
        
# Edit class
@login_required(login_url="admin-login")
def edit(request, uuid):
    try:

        class_obj = Class.objects.filter(uuid=uuid, created_by=request.user).first()

        if not class_obj:
            messages.error(request, "Class not found.")
            return redirect("classes-index")

        if request.method == "POST":
            form = ClassForm(request.POST, instance=class_obj)

            if form.is_valid():
                obj = form.save(commit=False)
                obj.created_by = request.user
                obj.save()

                messages.success(request, CLASS_UPDATED_SUCCESSFULLY)
                return redirect("classes-index")

            messages.error(request, INVALID_FORM_DATA)
            return render(request, "studio/classes/edit.html", {
                FORM: form,
                "class_obj": class_obj
            })

        form = ClassForm(instance=class_obj)
        return render(request, "studio/classes/edit.html", {
            FORM: form,
            "class_obj": class_obj
        })

    except Exception as ex:
        messages.error(request, SOMETHING_WENT_WRONG)
        return render(request, "500.html", {
            ERROR: str(ex),
            RETURN_URL: "/studio/classes/list"
        })
    
    
@login_required(login_url="admin-login")
def view(request, uuid):
    try:

        class_obj = Class.objects.filter(
            uuid=uuid,
            created_by=request.user
        ).first()

        if not class_obj:
            messages.error(request, CLASS_NOT_FOUND)
            return redirect("classes-index")

        return render(request, "studio/classes/view.html", {
            "class_obj": class_obj
        })

    except Exception as ex:
        messages.error(request, SOMETHING_WENT_WRONG)
        return render(request, "500.html", {
            ERROR: str(ex),
            RETURN_URL: "/studio/classes/list"
        })

    
# Delete
@login_required(login_url="admin-login")
def delete(request, uuid):
    try:

        if request.method == "POST":
            class_obj = Class.objects.filter(
                uuid=uuid,
                created_by=request.user
            ).first()
            if not class_obj:
                return JsonResponse({
                    SUCCESS: FALSE,
                    ERROR: CLASS_NOT_FOUND
                })
            class_obj.delete()
            return JsonResponse({
                SUCCESS: TRUE,
                MESSAGE: CLASS_DELETED_SUCCESSFULLY
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