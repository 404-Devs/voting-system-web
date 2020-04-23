from django.contrib import admin
from .models import Admin, School, Voter, Election, Aspirant, Team, Vote

admin.site.register(Admin)
admin.site.register(School)
admin.site.register(Voter)
admin.site.register(Election)
admin.site.register(Aspirant)
admin.site.register(Team)
admin.site.register(Vote)
