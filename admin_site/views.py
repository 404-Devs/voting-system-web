from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from api.models import Election, Team, School, Voter

def index(request):
    return render(request, "index.html")

def login(request):
    return render(request, "login.html")

def elections(request):
    elections = Election.objects.all()
    elections_list = []
    
    for data in elections:
        elections_list.append({'id': data.election_id, 'name': data.election_name, 'start': data.start_timestamp, 'end': data.end_timestamp })
    return render(request, "elections.html", {'elections_list': elections_list})

def create_election(request):
    return render(request, "create_elections.html")

def view_election(request, id):
    election = get_object_or_404(Election, pk=id)
    teams = Team.objects.filter(election=election)

    teams_list = []
    for team in teams:
        teams_list.append({'id': team.team_id, 'name': team.team_name, 'logo': team.team_logo, 'chairman': team.chairman.name, 'chairman_id': team.chairman.voter.voter_id, 'treasurer': team.treasurer.name, 'treasurer_id': team.treasurer.voter.voter_id, 'sec_gen': team.sec_gen.name, 'sec_gen_id': team.sec_gen.voter.voter_id})
    return render(request, "view_election.html", {'id': election.election_id, 'name': election.election_name, 'start': election.start_timestamp, 'end': election.end_timestamp, 'teams_list': teams_list})

def create_team(request, election_id):
    return render(request, "add_team.html", {'election_id': election_id})

def add_voter(request, school_id):
    return render(request, "add_voter.html", {"school_id": school_id})

def add_school(request):
    return render(request, "add_school.html")

def schools(request):
    schools = School.objects.all()
    schools_list = []
    
    for data in schools:
        schools_list.append({'id': data.school_id, 'name': data.school_name })
    return render(request, "schools.html", {'schools_list': schools_list})

def view_school(request, id):
    school = get_object_or_404(School, pk=id)
    students = Voter.objects.filter(school=school)

    students_list = []
    for student in students:
        students_list.append({'id': student.voter_id, 'reg_no': student.voter_reg_no, 'email': student.email})
    return render(request, "view_school.html", {'id': id, 'name': school.school_name, 'students_list': students_list})

def add_aspirant(request):
    return render(request, "add_aspirant.html")