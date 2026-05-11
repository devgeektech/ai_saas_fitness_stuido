from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from authentication.models import User
from django.contrib import messages
from studio.forms.forms import ClassForm
from studio.models import Class, Studio
from utils.constants import (ERROR, FALSE)
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
        context = {ERROR:str(ex),"return_url":"/studio/classes"}
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

        studio = Studio.objects.filter(user=request.user).first()

        if not studio:
            messages.error(request, "Studio not found for this user.")
            return redirect("studio-admin-profile")

        # ---------------- POST ----------------
        if request.method == "POST":
            form = ClassForm(request.POST)

            if form.is_valid():
                obj = form.save(commit=False)

                obj.created_by = request.user
                obj.studio = studio

                obj.save()

                messages.success(request, "Class created successfully")
                return redirect("classes-list")

            else:
                messages.error(request, "Invalid form data")
                return render(request, "studio/classes/create.html", {
                    "form": form
                })

        # ---------------- GET ----------------
        form = ClassForm()
        return render(request, "studio/classes/create.html", {
            "form": form
        })

    except Exception as ex:
        messages.error(request, f"Error: {str(ex)}")
        return render(request, "500.html", {
            "error": str(ex),
            "return_url": "/studio/classes/create"
        })
        
# Edit class
@login_required(login_url="admin-login")
def edit(request, uuid):
    try:

        class_obj = Class.objects.filter(
            uuid=uuid,
            created_by=request.user
        ).first()

        if not class_obj:
            messages.error(request, "Class not found.")
            return redirect("classes-list")

        # ---------------- POST ----------------
        if request.method == "POST":
            form = ClassForm(request.POST, instance=class_obj)

            if form.is_valid():
                obj = form.save(commit=False)
                obj.created_by = request.user
                obj.save()

                messages.success(request, "Class updated successfully")
                return redirect("classes-list")

            messages.error(request, "Invalid form data")
            return render(request, "studio/classes/edit.html", {
                "form": form,
                "class_obj": class_obj
            })

        # ---------------- GET ----------------
        form = ClassForm(instance=class_obj)

        return render(request, "studio/classes/edit.html", {
            "form": form,
            "class_obj": class_obj
        })

    except Exception as ex:
        messages.error(request, "Something went wrong")
        return render(request, "500.html", {
            "error": str(ex),
            "return_url": "/studio/classes/list"
        })
    
    
@login_required(login_url="admin-login")
def view(request, uuid):
    try:

        class_obj = Class.objects.filter(
            uuid=uuid,
            created_by=request.user
        ).first()

        if not class_obj:
            messages.error(request, "Class not found.")
            return redirect("classes-list")

        return render(request, "studio/classes/view.html", {
            "class_obj": class_obj
        })

    except Exception as ex:
        messages.error(request, "Something went wrong")
        return render(request, "500.html", {
            "error": str(ex),
            "return_url": "/studio/classes/list"
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
                    "success": False,
                    "error": "Class not found"
                })
            class_obj.delete()
            return JsonResponse({
                "success": True,
                "message": "Class deleted successfully"
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