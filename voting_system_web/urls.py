from django.contrib import admin
from django.urls import path
from api.views import voter_login, voter_reg, sch_reg, sch_update, election_reg, aspirant_reg, team_reg, vote, admin_login, admin_reg, get_elections
from admin_site.views import index, login, elections, create_election, view_election, create_team, add_voter, add_school, schools, view_school, add_aspirant

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/voter/login', voter_login),
    path('api/voter/register', voter_reg, name="voter_reg"),
    path('api/election/register', election_reg, name="election_reg"),
    path('api/aspirant/register', aspirant_reg, name="aspirant_reg"),
    path('api/team/register', team_reg, name="team_reg"),
    path('api/vote', vote),
    path('api/school/register', sch_reg, name="school_reg"),
    path('api/school/update', sch_update),
    path('api/admin/login', admin_login),
    path('api/admin/register', admin_reg),
    path('api/elections', get_elections),
    path('admin_site/', index, name="admin_index"),
    path('admin_site/login', login, name="admin_login"),
    path('admin_site/elections', elections, name="admin_elections"),
    path('admin_site/create_election', create_election, name="admin_create_election"),
    path('admin_site/elections/<int:id>', view_election, name="admin_view_election"),
    path('admin_site/create_team/<int:election_id>', create_team, name="admin_create_team"),
    path('admin_site/add_voter/<int:school_id>', add_voter, name="admin_add_voter"),
    path('admin_site/add_school', add_school, name="admin_add_school"),
    path('admin_site/schools', schools, name="admin_schools"),
    path('admin_site/view_school/<int:id>', view_school, name="view_school"),
    path('admin_site/add_aspirant/', add_aspirant, name="admin_add_aspirant")
]
