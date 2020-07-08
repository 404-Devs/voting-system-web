from django.contrib import admin
from .models import School, Voter, Election, Aspirant, Team, Vote, SendGrid

admin.site.register(School)
admin.site.register(Voter)
admin.site.register(Election)
admin.site.register(Aspirant)
admin.site.register(Team)
admin.site.register(Vote)
admin.site.register(SendGrid)
