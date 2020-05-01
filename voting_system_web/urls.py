from django.contrib import admin
from django.urls import path
from api.views import voter_login, voter_reg, sch_reg, sch_update, election_reg, aspirant_reg, team_reg, vote, admin_login, admin_reg, get_elections

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/voter/login', voter_login),
    path('api/voter/register', voter_reg),
    path('api/election/register', election_reg),
    path('api/aspirant/register', aspirant_reg),
    path('api/team/register', team_reg),
    path('api/vote', vote),
    path('api/school/register', sch_reg),
    path('api/school/update', sch_update),
    path('api/admin/login', admin_login),
    path('api/admin/register', admin_reg),
    path('api/elections', get_elections)
]
