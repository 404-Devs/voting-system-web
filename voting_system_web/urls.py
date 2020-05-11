from django.contrib import admin
from django.urls import path
from api.views import *
from admin_site.views import *
from results.views import *

urlpatterns = [
    path('', r_index),
    path('election/<int:id>', r_get_election, name="r_get_election"),
    path('aspirant/<int:id>', r_view_aspirant, name="r_view_aspirant"),
    path('admin/', admin.site.urls),
    path('api/voter/login', voter_login),
    path('api/voter/register', voter_reg, name="voter_reg"),
    path('api/voter/delete/<int:id>', delete_voter),
    path('api/election/register', election_reg, name="election_reg"),
    path('api/aspirant/register', aspirant_reg, name="aspirant_reg"),
    path('api/aspirant/<int:id>', get_aspirant),
    path('api/aspirant/delete/<int:id>', delete_aspirant),
    path('api/team/register', team_reg, name="team_reg"),
    path('api/team/<int:id>', get_team),
    path('api/team/delete/<int:id>', delete_team),
    path('api/vote', vote),
    path('api/school/register', sch_reg, name="school_reg"),
    path('api/school/delete/<int:id>', delete_sch),
    path('api/school/update', sch_update),
    path('api/elections', get_elections),
    path('api/election/<int:election_id>', get_election),
    path('api/election/delete/<int:id>', delete_election),
    path('api/results/<int:election_id>', results),
    path('admin_site/', index, name="admin_index"),
    path('admin_site/elections', elections, name="admin_elections"),
    path('admin_site/create_election', create_election, name="admin_create_election"),
    path('admin_site/elections/<int:id>', view_election, name="admin_view_election"),
    path('admin_site/aspirants/<int:id>', view_aspirant, name="admin_view_aspirant"),
    path('admin_site/create_team/<int:election_id>', create_team, name="admin_create_team"),
    path('admin_site/add_voter/<int:school_id>', add_voter, name="admin_add_voter"),
    path('admin_site/add_school', add_school, name="admin_add_school"),
    path('admin_site/schools', schools, name="admin_schools"),
    path('admin_site/view_school/<int:id>', view_school, name="view_school"),
    path('admin_site/add_aspirant/', add_aspirant, name="admin_add_aspirant")
]
