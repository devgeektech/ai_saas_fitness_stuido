from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from superadmin.views.views import superuser_required
from django.contrib import messages
from django.db.models import CharField, Value, OuterRef, Subquery, Case, When, F
from django.db.models.functions import Coalesce, Concat
from django_serverside_datatable.views import ServerSideDatatableView
from studio.models import Studio
from authentication.models import User
from utils.constants import (ERROR)
import logging

logger = logging.getLogger(__name__)


# Studio Management for Superadmin
@login_required(login_url="admin-login")
@superuser_required
def studios(request):
    try:
        return render(request, "superadmin/studios/index.html")
    except Exception as ex:
        messages.error(request, ex)
        return render(request, "500.html", {
            ERROR: str(ex),
            "return_url": "/admin/studios"
        })


class StudioUsersListView(ServerSideDatatableView):
    columns = [
        "uuid",
        "first_name",
        "last_name",
        "email",
        "username",
        "role",
        "studio_name",
        "is_active",
    ]

    def get_queryset(self):
        studio_name = Subquery(
            Studio.objects.filter(user=OuterRef("pk")).values("name")[:1]
        )

        return (
            User.objects
                .filter(role="studio_admin")
                .annotate(
                    studio_name=studio_name,
                )
                .order_by("-date_joined")
        )


@login_required(login_url="admin-login")
@superuser_required
@require_POST
def toggle_studio_user_status(request, uuid):
    try:
        studio_user = User.objects.filter(uuid=uuid, role="studio_admin").first()
        if not studio_user:
            return JsonResponse({"success": False, "message": "Studio user not found."}, status=404)

        studio_user.is_active = not studio_user.is_active
        studio_user.save(update_fields=["is_active"])

        return JsonResponse({
            "success": True,
            "status": "Active" if studio_user.is_active else "Inactive",
        })
    except Exception as ex:
        logger.error("Failed to toggle studio user status: %s", ex)
        return JsonResponse({"success": False, "message": str(ex)}, status=500)


@login_required(login_url="admin-login")
@superuser_required
def view_studio(request, uuid):
    try:
        studio_user = User.objects.filter(uuid=uuid, role="studio_admin").first()
        if not studio_user:
            messages.error(request, "Studio user not found.")
            return redirect("studios-index")

        studio = Studio.objects.filter(user=studio_user).first()
        return render(request, "superadmin/studios/view.html", {
            "studio_user": studio_user,
            "studio": studio
        })
    except Exception as ex:
        messages.error(request, ex)
        return render(request, "500.html", {
            ERROR: str(ex),
            "return_url": "/admin/studios"
        })


# Admin Dashboard
@login_required(login_url="admin-login")
@superuser_required
def admin_dashboard(request):
    try:
        if request.user.is_authenticated and request.user.is_superuser:
            return render(request, "superadmin/dashboard.html")
        else:
            return redirect("/admin/login")
    except Exception as ex:
        messages.error(request, ex)        
        context = {ERROR:str(ex),"return_url":"/admin/dashboard"}
        return render(request,"500.html",context)