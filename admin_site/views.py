from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.contrib.admin.views.decorators import staff_member_required
from api.models import Election, Team, School, Voter, Aspirant
from time import time
from datetime import datetime
from django.utils.timezone import make_aware


@staff_member_required
def index(request):
    ongoing = Election.objects.filter(start_timestamp__lt = make_aware(datetime.fromtimestamp(time())))
    return render(request, "index.html", {'elections': Election.objects.count(), 'schools': School.objects.count(), 'teams': Team.objects.count(), 'voters': Voter.objects.count(), 'ongoing': ongoing.count()})

@staff_member_required
def elections(request):
    elections = Election.objects.all()
    elections_list = []
    
    for data in elections:
        elections_list.append({'id': data.election_id, 'name': data.election_name, 'start': data.start_timestamp, 'end': data.end_timestamp })
    return render(request, "elections.html", {'elections_list': elections_list})

@staff_member_required
def create_election(request):
    return render(request, "create_elections.html")

@staff_member_required
def view_election(request, id):
    election = get_object_or_404(Election, pk=id)
    teams = Team.objects.filter(election=election)

    teams_list = []
    for team in teams:
        teams_list.append({'id': team.team_id, 'name': team.team_name, 'logo': team.team_logo, 'chairman': team.chairman.name, 'chairman_id': team.chairman.aspirant_id, 'treasurer': team.treasurer.name, 'treasurer_id': team.treasurer.aspirant_id, 'sec_gen': team.sec_gen.name, 'sec_gen_id': team.sec_gen.aspirant_id})
    return render(request, "view_election.html", {'id': election.election_id, 'name': election.election_name, 'start': election.start_timestamp, 'end': election.end_timestamp, 'teams_list': teams_list})

@staff_member_required
def create_team(request, election_id):
    return render(request, "add_team.html", {'election_id': election_id})

@staff_member_required
def add_voter(request, school_id):
    return render(request, "add_voter.html", {"school_id": school_id})

@staff_member_required
def schools(request):
    schools = School.objects.all()
    schools_list = []
    
    for data in schools:
        schools_list.append({'id': data.school_id, 'name': data.school_name })
    return render(request, "schools.html", {'schools_list': schools_list})

@staff_member_required
def add_school(request):
    return render(request, "add_school.html")

@staff_member_required
def view_school(request, id):
    school = get_object_or_404(School, pk=id)
    students = Voter.objects.filter(school=school)

    students_list = []
    for student in students:
        students_list.append({'id': student.voter_id, 'reg_no': student.voter_reg_no, 'email': student.email})
    return render(request, "view_school.html", {'id': id, 'name': school.school_name, 'students_list': students_list})

@staff_member_required
def add_aspirant(request):
    return render(request, "add_aspirant.html")

@staff_member_required
def view_aspirant(request, id):
    aspirant = get_object_or_404(Aspirant, pk=id)
    return render(request, "view_aspirant.html", {'id': aspirant.aspirant_id, 'fname': aspirant.fname, 'lname': aspirant.lname, 'photo': aspirant.aspirant_photo, 'msg': aspirant.message, 'email': aspirant.voter.email, 'school': aspirant.voter.school.school_name})