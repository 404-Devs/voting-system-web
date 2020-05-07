from django.shortcuts import render, get_object_or_404
from api.models import Election, Team, Aspirant

def r_index(request):
    elections = Election.objects.all()
    elections_list = []
    
    for data in elections:
        elections_list.append({'id': data.election_id, 'name': data.election_name, 'start': data.start_timestamp, 'end': data.end_timestamp })
    return render(request, "r_index.html", {'elections_list': elections_list})

def r_get_election(request, id):
    election = get_object_or_404(Election, pk=id)
    teams = Team.objects.filter(election=election)

    teams_list = []
    for team in teams:
        teams_list.append({'id': team.team_id, 'name': team.team_name, 'logo': team.team_logo, 'chairman': team.chairman.name, 'chairman_id': team.chairman.aspirant_id, 'treasurer': team.treasurer.name, 'treasurer_id': team.treasurer.aspirant_id, 'sec_gen': team.sec_gen.name, 'sec_gen_id': team.sec_gen.aspirant_id})
    return render(request, "r_view_election.html", {'id': election.election_id, 'name': election.election_name, 'start': election.start_timestamp, 'end': election.end_timestamp, 'teams_list': teams_list})

def r_view_aspirant(request, id):
    aspirant = get_object_or_404(Aspirant, pk=id)
    return render(request, "r_view_aspirant.html", {'name': aspirant.name, 'photo': aspirant.aspirant_photo, 'msg': aspirant.message, 'school': aspirant.voter.school.school_name})