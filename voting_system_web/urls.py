from django.contrib import admin
from django.urls import path
from api.views import voter_login, voter_registration

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/login/voter', voter_login),
    path('api/register', voter_registration)
]
