from django.contrib import admin
from django.urls import path
from api.views import voter_login, voter_registration
from admin_site.views import admin_login, admin_registration

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/login/voter', voter_login),
    path('api/register/voter', voter_registration),
    path('admin_site/login/admin', admin_login),
    path('admin_site/register/admin', admin_registration)
]
