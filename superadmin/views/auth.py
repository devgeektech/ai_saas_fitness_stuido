from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from superadmin.views.views import superuser_required
from authentication.models import User
from django.contrib import messages
from utils.constants import (ERROR)
import logging

logger = logging.getLogger(__name__)


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