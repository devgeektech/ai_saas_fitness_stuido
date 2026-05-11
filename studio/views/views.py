from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from utils.constants import ERROR

# Create your views here.
@login_required(login_url="admin-login")
def studio_admin_dashboard(request):
    try:
        if request.user.is_authenticated and request.user.is_active and request.user.role == "studio_admin":
            return render(request, "studio/dashboard.html")
        else:
            return redirect("/admin/login")
    except Exception as ex:
        messages.error(request, ex)        
        context = {ERROR:str(ex)}
        return render(request,"500.html",context)