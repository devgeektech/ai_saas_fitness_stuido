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
from utils.utils import generate_random_string
from utils.constants import (    
    ACCESS_RESTRICTON,
    ERROR,
    FALSE,
    INVALID_LOGIN_DETAILS,
    INVALID_OLD_PASSWORD,
    INVALID_PASSWORD,
    LOGIN_ACCOUNT,
    LOGIN_SUCCESS,
    LOGOUT_SUCCESS,
    PASSWORD_NOT_MATCHED,
    PROFILE_UPDATED_SUCCESS,
    REGISTER_SUCCESS,
    SUCCESS,
    TRUE,
    MESSAGE,
    USER_ALREADY_EXISTS,
    USER_NOT_ACTIVE,
    USER_NOT_FOUND, 
)
import os

# login for superadmin , studio admin
def auth_login(request):
    try:        
        if request.method == "POST":
            email = request.POST.get("email")
            password = request.POST.get("password")
            
            try:
                user = User.objects.get(Q(email=email))
            except User.DoesNotExist:
                return JsonResponse({SUCCESS: FALSE, ERROR: USER_NOT_FOUND})
            
            if user.is_superuser and user.is_active:
                user = authenticate(email=email, password=password)
                if user is not None:
                    login(request, user)
                    messages.success(request, LOGIN_SUCCESS)
                    return JsonResponse({SUCCESS: TRUE, MESSAGE: LOGIN_SUCCESS})
                else:
                    return JsonResponse(
                        {SUCCESS: FALSE, ERROR: INVALID_LOGIN_DETAILS}
                    )
            if user.is_active and user.role=="studio_admin":
                user = authenticate(email=email, password=password)
                if user is not None:
                    login(request, user)
                    messages.success(request, LOGIN_SUCCESS)
                    return JsonResponse({SUCCESS: TRUE, "user_role":user.role, MESSAGE: LOGIN_SUCCESS})
                else:
                    return JsonResponse(
                        {SUCCESS: FALSE, ERROR: INVALID_LOGIN_DETAILS}
                    )
            return JsonResponse({SUCCESS: FALSE, ERROR: USER_NOT_ACTIVE})
        else:
            return render(request, "login.html")
    except Exception as ex:
        return JsonResponse({SUCCESS: FALSE, ERROR: f"Error: {str(ex)}"})
    
# register studio user
def auth_register(request):
    try:

        if request.method == "POST":

            email = request.POST.get("email").strip()
            password = request.POST.get("password").strip()
            confirm_password = request.POST.get("confirm_password").strip()

            # Check Password Match
            if password != confirm_password:
                messages.error(request, PASSWORD_NOT_MATCHED)
                return redirect('admin-register')

            # Check Existing User
            if User.objects.filter(Q(email=email)).exists():
                messages.error(request, USER_ALREADY_EXISTS)
                return redirect('admin-register')

            # Create User
            user = User.objects.create_user(
                email=email,
                username=email.split("@")[0],
                password=password,
            )

            user.role = "studio_admin"
            user.is_active = True
            user.email_verified = True
            user.save()
            messages.success(request, REGISTER_SUCCESS)
            return redirect('admin-login')
        else:
            return render(request, "register.html")

    except Exception as ex:
        return render(request, '500.html', {
            ERROR: str(ex)
        })
        
        
        
# Logout User
@login_required(login_url="login")
def auth_logout(request):
    try:
        logout(request)
        messages.success(request, LOGOUT_SUCCESS)
        return redirect("admin-login")
    except Exception as ex:
        messages.error(request, str(ex))        
        context = {ERROR:str(ex),"return_url":"/profile"}
        return render(request,"500.html",context)
    
# profile
@login_required(login_url="login")
def profile(request):
    try:
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
                    fs = FileSystemStorage(location="static/images/uploads/user/")
                    new_image = fs.save(new_image_name, image)
                    user.image = f"uploads/user/{new_image_name}"

                    try:
                        # Delete the old image
                        os.remove(old_image.path)
                    except Exception as ex:
                        pass
                
                user.phone = phone
                user.save()
                messages.success(request, PROFILE_UPDATED_SUCCESS)
                return redirect("profile")

            except Exception as ex:
                messages.error(request, str(ex))        
                context = {ERROR:str(ex),"return_url":"/profile"}
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
                context = {ERROR:str(ex),"return_url":"/profile"}
                return render(request,"500.html",context)

        if request.user.is_authenticated:
            return render(request,"profile.html")
        else:
            messages.error(request, LOGIN_ACCOUNT)  
            return redirect("admin-login")
    except Exception as ex:
        messages.error(request, str(ex))        
        context = {ERROR:str(ex),"return_url":"/profile"}
        return render(request,"500.html",context)
    
    
    
# Clear Logs
def clear_logs(request):
    try:
        with open("logs/debug.log", "w"):
            pass
        return HttpResponse("Logs are cleared.")
    except Exception as ex:
        return HttpResponse(ex)
    