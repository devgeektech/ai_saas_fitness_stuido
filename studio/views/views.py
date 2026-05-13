from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.db.models import Q
from django.contrib import messages
from authentication.models import User
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.hashers import check_password
from studio.models import Studio
from utils.utils import generate_random_string
from django.utils.text import slugify
from utils.constants import (    
    ERROR,
    INVALID_OLD_PASSWORD,
    INVALID_PASSWORD,
    LOGIN_ACCOUNT,
    PROFILE_UPDATED_SUCCESS,
)
import os

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
        context = {ERROR:str(ex), "return_url":"/studio/admin/dashboard"}
        return render(request,"500.html",context)
    
    
@login_required(login_url="login")
def studio_admin_profile(request):
    try:
        
        if request.method == "GET":
            studio = Studio.objects.filter(user=request.user).first()

            return render(request, "studio/profile.html", {
                "studio": studio
            })
        if request.method == "POST" and request.POST.get('type') == "update_info":
            try:
                image = request.FILES.get("image")
                phone = request.POST.get("phone")  
                user = request.user

                # Change Profile Picture
                if image is not None:                   
                    old_image = user.image
                    original_file_name = image.name
                    file_extension = original_file_name.split(".")[-1]
                    unique_name = generate_random_string(6) 
                    new_image_name = f"{unique_name}.{file_extension}"
                    # Save the avatar with the new name
                    fs = FileSystemStorage(location="media/studios/user/")
                    new_image = fs.save(new_image_name, image)
                    user.image = f"studios/user/{new_image_name}"

                    try:
                        # Delete the old image
                        os.remove(old_image.path)
                    except Exception as ex:
                        pass
                
                user.save()
                messages.success(request, PROFILE_UPDATED_SUCCESS)
                return redirect("profile")

            except Exception as ex:
                messages.error(request, str(ex))        
                context = {ERROR:str(ex),"return_url":"/studio/admin/profile"}
                return render(request,"500.html",context)

        elif request.method == "POST" and request.POST.get('type') == "update_password":
            try:
                current_password = request.POST.get("current_password")
                if check_password(current_password, request.user.password):
                    password = request.POST.get("password")
                    if password:
                        user = request.user
                        user.set_password(password)
                        user.save()
                        login(request, user)
                        messages.success(request, PROFILE_UPDATED_SUCCESS)
                        return redirect("profile")
                    messages.error(request, INVALID_PASSWORD)
                    return redirect("profile")
                messages.error(request, INVALID_OLD_PASSWORD)
                return redirect("profile")
            except Exception as ex:
                messages.error(request, str(ex))        
                context = {ERROR:str(ex),"return_url":"/studio/admin/profile"}
                return render(request,"500.html",context)
            
        elif request.method == "POST" and request.POST.get('type') == "update_profile":
            try:
                name = request.POST.get("name")
                slug = request.POST.get("slug")
                # slug 
                if not slug:
                    slug = slugify(name)
                else:
                    slug = slugify(slug)
                brand_color = request.POST.get("brand_color")
                logo = request.FILES.get("logo")

                # If user already has studio -> update
                if request.user.studio:

                    studio = request.user.studio

                    studio.name = name
                    studio.slug = slug
                    studio.brand_color = brand_color
                    studio.save()

                # Else create new studio
                else:

                    studio = Studio.objects.create(
                        name=name,
                        slug=slug,
                        brand_color=brand_color,
                    )

                    # Save studio id in auth user table
                    request.user.studio = studio
                    request.user.save()
                    

                if logo:
                    old_logo = studio.logo

                    file_extension = logo.name.split(".")[-1]
                    unique_name = generate_random_string(6)
                    new_logo_name = f"{unique_name}.{file_extension}"

                    fs = FileSystemStorage(location="media/studios/")
                    fs.save(new_logo_name, logo)

                    studio.logo = f"studios/{new_logo_name}"
                    studio.save()

                    try:
                        if old_logo:
                            os.remove(old_logo.path)
                    except Exception:
                        pass

                messages.success(request, PROFILE_UPDATED_SUCCESS)
                return redirect("studio-admin-profile")

            except Exception as ex:
                return render(request, "500.html", {
                    ERROR: str(ex),
                    "return_url": "/studio/admin/profile"
                })
    except Exception as ex:
        messages.error(request, str(ex))        
        context = {ERROR:str(ex),"return_url":"/studio/admin/profile"}
        return render(request,"500.html",context)
    