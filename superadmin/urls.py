from django.urls import path
from superadmin.views import auth

urlpatterns = [
    path("dashboard", auth.admin_dashboard, name="admin-dashboard"),
    
]
