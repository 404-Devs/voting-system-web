from django.contrib import admin
from django.urls import path
from api.views import *
from admin_site.views import *
from django.contrib.auth.views import LogoutView
from django.conf.urls import url
from django.conf import settings

urlpatterns = [
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
    path('api/election/<int:election_id>/<int:voter_id>', get_election),
    path('api/election/delete/<int:id>', delete_election),
    path('api/results/<int:election_id>', results),
    path('', index, name="admin_index"),
    path('elections', elections, name="admin_elections"),
    path('create_election', create_election, name="admin_create_election"),
    path('elections/<int:id>', view_election, name="admin_view_election"),
    path('aspirants/<int:id>', view_aspirant, name="admin_view_aspirant"),
    path('create_team/<int:election_id>', create_team, name="admin_create_team"),
    path('add_voter/<int:school_id>', add_voter, name="admin_add_voter"),
    path('add_school', add_school, name="admin_add_school"),
    path('schools', schools, name="admin_schools"),
    path('view_school/<int:id>', view_school, name="view_school"),
    path('add_aspirant/', add_aspirant, name="admin_add_aspirant"),
    url(r'^logout/$', LogoutView.as_view(), name='logout')
]