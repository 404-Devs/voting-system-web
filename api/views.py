from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate, login
from .models import Voter, School, Election, Aspirant, Team, Vote
from django.contrib.admin.views.decorators import staff_member_required
from .lib.blockchain import *
import hashlib
import json
import binascii
import os
import uuid
from time import time
import admin_site.views as admin_views


result = {'status': 'error'}

def voter_login(request):
    # get values passed in the POST object
    reg_no = request.POST.get("reg_no")
    password = request.POST.get("password")
    # make sure that the POST values are not empty
    if all([reg_no, password]):
        try:
            # get voter with the specified registration number
            voter = Voter.objects.get(voter_reg_no=reg_no)
            # check if the number of login attempts have been exhausted
            if voter.login_attempts == 0:
                result['msg'] = "Account temporarily blocked, you have made too many login attempts. Please see the system administrator"
                return HttpResponse(json.dumps(result))
            # hash the passed password
            pwdhash = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'), voter.password_salt.encode('utf-8'),
                                          100000)
            pwdhash = binascii.hexlify(pwdhash)
            # check if the passwords are the same
            if voter.voter_password == pwdhash.decode('ascii'):
                if voter.login_attempts != 10:
                    voter.login_attempts = 10
                    voter.save()
                result['status'] = 'success'
                # no sane person should return the password hash, but "meh!"
                result['data'] = {'id': voter.voter_id, 'reg_no': voter.voter_reg_no, 'email': voter.email,
                                  'school_id': voter.school.school_id, 'dibs': pwdhash.decode('ascii')}
                result['msg'] = 'Authentication successful.'
            else:
                voter.login_attempts -= 1
                voter.save()
                result['msg'] = 'Authentication failed.'
                result['n'] = voter.login_attempts
        except Voter.DoesNotExist:
            result['msg'] = 'Voter does not exist.'
    else:
        result['msg'] = 'Make sure that you provide all the required values.'
    # return a JSON object
    return HttpResponse(json.dumps(result))

@staff_member_required
def voter_reg(request):
    # get values passed in the POST object
    reg_no = request.POST.get("reg_no")
    email = request.POST.get('email')
    password = request.POST.get("password")
    school_id = request.POST.get("school_id")
    # make sure that the POST values are not empty
    if all([reg_no, email, password, school_id]):
        # check if the registration number has been used before
        query = Voter.objects.filter(voter_reg_no=reg_no)
        if query.count() > 0:
            result['msg'] = 'The registration number provided has been registered before.'
            return HttpResponse(json.dumps(result))
        # check if the email has been used before
        query = Voter.objects.filter(email=email)
        if query.count() > 0:
            result['msg'] = 'The email provided has been registered before.'
            return HttpResponse(json.dumps(result))

        # find a random salt
        salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
        # hash the passed password using the hash
        pwdhash = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'), salt, 100000)
        pwdhash = binascii.hexlify(pwdhash)
        try:
            # get the school with the provided school id
            school = School.objects.get(school_id=int(school_id))
            # Save the voter
            Voter.objects.create(voter_reg_no=reg_no, email=email, voter_password=pwdhash.decode('ascii'),
                                 password_salt=salt.decode('ascii'), school=school)
            result['status'] = 'success'
            result['msg'] = 'Voter created successfully.'
        except School.DoesNotExist:
            result['msg'] = 'The school associated with the provided id does not exist.'
    else:
        result['msg'] = 'Make sure that you provide all the required values.'
    # return JSON object
    return admin_views.view_school(request, int(school_id))

@staff_member_required
def delete_voter(request, id):
    voter = get_object_or_404(Voter, pk=id)
    school_id = voter.school.school_id
    voter.delete()
    result['status'] = 'success'
    return admin_views.view_school(request, int(school_id))

def update_password(request):
    reg_no = request.POST.get("reg_no")
    old_pass = request.POST.get("old_password")
    new_pass = request.POST.get("new_password")

    # make sure that the POST values are not empty
    if all([reg_no, old_pass, new_pass]):
        try:
            # get voter with the specified registration number
            voter = Voter.objects.get(voter_reg_no=reg_no)
            # check if the number of login attempts have been exhausted
            if voter.login_attempts == 0:
                result['msg'] = "Account temporarily blocked, you have made too many login attempts. Please see the system administrator"
                return HttpResponse(json.dumps(result))
            # hash the passed password
            pwdhash = hashlib.pbkdf2_hmac('sha512', old_pass.encode('utf-8'), voter.password_salt.encode('utf-8'),
                                          100000)
            pwdhash = binascii.hexlify(pwdhash)
            # check if the passwords are the same
            if voter.voter_password == pwdhash.decode('ascii'):
                if voter.login_attempts != 10:
                    voter.login_attempts = 10
                    voter.save()
                newhash = hashlib.pbkdf2_hmac('sha512', new_pass.encode('utf-8'), salt, 100000)
                newhash = binascii.hexlify(pwdhash)
                voter.newhash = newhash.decode('ascii')
                voter.save()
                result['status'] = 'success'
                result['msg'] = 'Password changed successfully.'
            else:
                voter.login_attempts -= 1
                voter.save()
                result['msg'] = 'Authentication failed.'
                result['n'] = voter.login_attempts
        except Voter.DoesNotExist:
            result['msg'] = 'Voter does not exist.'
    else:
        result['msg'] = 'Make sure that you provide all the required values'
    return HttpResponse(json.dumps(result))

@staff_member_required
def sch_reg(request):
    sch_name = request.POST.get("school_name")
    if sch_name is not None:
        School.objects.create(school_name=sch_name)
        result['status'] = 'success'
        result['msg'] = 'School created successfully.'
    else:
        result['msg'] = 'Make sure that you provide all the required values.'
    return admin_views.schools(request)

@staff_member_required
def sch_update(request):
    sch_id = request.POST.get("school_id")
    sch_name = request.POST.get("school_name")
    if sch_name is not None:
        try:
            school = School.objects.get(school_id=int(sch_id))
            school.school_name = sch_name
            school.save()
            result['status'] = 'success'
            result['msg'] = 'School info updated successfully.'
        except School.DoesNotExist:
            result['msg'] = 'School does not exist.'
    else:
        result['msg'] = 'Make sure that you provide all the required values.'
    return admin_views.view_school(request, int(sch_id))

@staff_member_required
def delete_sch(request, id):
    school = get_object_or_404(School, pk=id)
    school.delete()
    result['status'] = 'success'
    return admin_views.schools(request)

@staff_member_required
def election_reg(request):
    election_name = request.POST.get("election_name")
    start_timestamp = request.POST.get("start_timestamp")
    end_timestamp = request.POST.get("end_timestamp")
    if all([election_name, start_timestamp, end_timestamp]):
        Election.objects.create(election_name=election_name, start_timestamp=start_timestamp, end_timestamp=end_timestamp)
        election = Election.objects.latest('election_id')
        set_election_bc(load_env(), election.election_id, election_name, election.start_unix, election.end_unix)
        result['status'] = 'success'
        result['msg'] = 'Election created successfully.'
    else:
        result['msg'] = 'Make sure that you provide all the required values.'
    return admin_views.elections(request)

def get_elections(request):
    elections = Election.objects.all()
    result['status'] = 'success'
    result['data'] = {}
    result['msg'] = "Query successful"
    
    for data in elections:
        result['data'][data.election_id] = {'id': data.election_id, 'name': data.election_name, 'start': data.start_unix, 'end': data.end_unix, 'last_mod': data.last_mod_unix}
    return HttpResponse(json.dumps(result))

def get_election(request, election_id, voter_id):
    election = get_object_or_404(Election, pk=election_id)
    results_bc = get_results_bc(load_env(), int(election_id))
    voter = Voter.objects.get(voter_id=voter_id)
    query = Vote.objects.filter(voter=voter, election=election)

    vote_count = {}
    for team in results_bc:
        vote_count[team[0]] = team[5]

    teams = Team.objects.filter(election=election)
    result['status'] = 'success'
    result['data'] = {'id': election.election_id, 'name': election.election_name, 'start': election.start_unix, 'end': election.end_unix, 'last_mod': election.last_mod_unix, 'voted': query.count() > 0}
    result['parties'] = {}

    for team in teams:
        result['parties'][team.team_id] = {'id': team.team_id, 'name': team.team_name, 'logo': team.team_logo, 'slogan': team.slogan, 'chairman': team.chairman.name, 'treasurer': team.treasurer.name, 'sec_gen': team.sec_gen.name, 'votes': vote_count[team.team_id]}
    return HttpResponse(json.dumps(result))

@staff_member_required
def delete_election(request, id):
    election = get_object_or_404(Election, pk=id)
    election.delete()
    result['status'] = 'success'
    return admin_views.elections(request)

@staff_member_required
def election_update(request):
    election_id = request.POST.get("election_id")
    election_name = request.POST.get("election_name")
    start_timestamp = request.POST.get("start_timestamp")
    end_timestamp = request.POST.get("end_timestamp")
    if all([election_name, start_timestamp, end_timestamp]):
        try:
            election = Election.objects.get(election_id=election_id)
            election.election_name = election_name
            election.start_timestamp = start_timestamp
            election.end_timestamp = end_timestamp
            election.save()
            result['status'] = 'success'
            result['msg'] = 'Election info updated successfully.'
        except Election.DoesNotExist:
            result['msg'] = 'Election does not exist.'
    else:
        result['msg'] = 'Make sure that you provide all the required values.'
    return admin_views.view_election(request, int(election_id))

@staff_member_required
def aspirant_reg(request):
    voter_reg = request.POST.get("aspirant_reg_no")
    aspirant_photo = request.POST.get("aspirant_photo")
    fname = request.POST.get("fname")
    lname = request.POST.get("lname")
    message = request.POST.get("message")
    if all([voter_reg, aspirant_photo, fname, lname, message]):
        try:
            voter = Voter.objects.get(voter_reg_no=voter_reg)
            Aspirant.objects.create(voter=voter, aspirant_photo=aspirant_photo, fname=fname, lname=lname, message=message)
            aspirant = Aspirant.objects.latest('aspirant_id')
            set_aspirant_bc(load_env(), aspirant.aspirant_id, aspirant.name)
            result['status'] = 'success'
            result['msg'] = 'Aspirant added successfully.'
        except Voter.DoesNotExist:
            result['msg'] = 'Voter does not exist.'
    else:
        result['msg'] = 'Make sure that you provide all the required values.'
    return admin_views.add_aspirant(request)

def get_aspirant(request, id):
    asp = get_object_or_404(Aspirant, pk=id)
    result['status'] = 'success'
    result['data'] = {'id': asp.aspirant_id, 'name': asp.name, 'photo': asp.aspirant_photo}
    return HttpResponse(json.dumps(result))

@staff_member_required
def delete_aspirant(request, id):
    aspirant = get_object_or_404(Aspirant, pk=id)
    aspirant.delete()
    result['status'] = 'success'
    return admin_views.add_aspirant(request)

@staff_member_required
def team_reg(request):
    team_name = request.POST.get("team_name")
    team_logo = request.POST.get("team_logo")
    election_id = request.POST.get("election_id")
    chairman_id = request.POST.get("chairman_reg")
    sec_gen_id = request.POST.get("sec_gen_reg")
    treasurer_id = request.POST.get("treasurer_reg")
    slogan = request.POST.get("slogan")
    if all([team_name, team_logo, election_id, chairman_id, sec_gen_id, treasurer_id, slogan]):
        election = Election.objects.get(election_id=election_id)
        if time() > election.start_unix and time() < election.end_unix:
            result['msg'] = "You cannot register teams at this time. The election has either started or ended."
            return HttpResponse(json.dumps(result))

        chairman = Aspirant.objects.get(voter=Voter.objects.get(voter_reg_no=chairman_id))
        sec_gen = Aspirant.objects.get(voter=Voter.objects.get(voter_reg_no=sec_gen_id))
        treasurer = Aspirant.objects.get(voter=Voter.objects.get(voter_reg_no=treasurer_id))
        Team.objects.create(team_name=team_name, team_logo=team_logo, election=election, chairman=chairman, sec_gen=sec_gen, treasurer=treasurer, slogan=slogan)
        team = Team.objects.latest('team_id')
        set_team_bc(load_env(), election.election_id, team.team_id, team_name, chairman.aspirant_id, sec_gen.aspirant_id, treasurer.aspirant_id)
        result['status'] = 'success'
        result['msg'] = 'Team created successfully.'
    else:
        result['msg'] = 'Make sure that you provide all the required values.'
    return admin_views.view_election(request, int(election_id))

def get_team(request, id):
    team = get_object_or_404(Team, pk=id)
    result['status'] = 'success'
    result['data'] = {'id': team.team_id, 'name': team.team_name, 'logo': team.team_logo, 'slogan': team.slogan, 'chairman': team.chairman.name, 'chairman_id': team.chairman.voter.voter_id, 'chairman_photo': team.chairman.aspirant_photo, 'chairman_msg': team.chairman.message, 'treasurer': team.treasurer.name, 'treasurer_id': team.treasurer.voter.voter_id, 'treasurer_photo': team.treasurer.aspirant_photo, 'treasurer_msg': team.treasurer.message, 'sec_gen': team.sec_gen.name, 'sec_gen_id': team.sec_gen.voter.voter_id, 'sec_gen_photo': team.sec_gen.aspirant_photo, 'sec_gen_msg': team.sec_gen.message, }
    return HttpResponse(json.dumps(result))

@staff_member_required
def delete_team(request, id):
    team = get_object_or_404(Team, pk=id)
    election_id = team.election.election_id
    team.delete()
    result['status'] = 'success'
    return admin_views.view_election(request, election_id)

def vote(request):
    voter_id = request.POST.get("voter_reg")
    election_id = request.POST.get("election_id")
    team_id = request.POST.get("team_id")
    dibs = request.POST.get("dibs")
    if all([voter_id, election_id, team_id, dibs]):
        election = Election.objects.get(election_id=int(election_id))
        if time() < election.start_unix or time() > election.end_unix:
            result['msg'] = "Not the time to cast votes."
            return HttpResponse(json.dumps(result))

        voter = Voter.objects.get(voter_reg_no=voter_id)
        if voter.voter_password != dibs:
            result['msg'] = "Authentication failed!"
            return HttpResponse(json.dumps(result))

        team = Team.objects.get(team_id=int(team_id))
        # check if the voter has voted in this election before
        query = Vote.objects.filter(voter=voter, election=election)
        if query.count() > 0:
            result['msg'] = 'You have already voted. SMH 😒.'
            return HttpResponse(json.dumps(result))

        env = load_env()
        votingToken = uuid.uuid4().hex[:32]
        Vote.objects.create(voter=voter, election=election)
        cast_bc(env, int(election_id), team.team_id, votingToken)
        result['status'] = 'success'
        result['msg'] = 'You have voted successfully.'
    else:
        result['msg'] = 'Make sure that you provide all the required values.'
    return HttpResponse(json.dumps(result))

def results(request, election_id):
    result['status'] = 'success'
    result['data'] = get_results_bc(load_env(), int(election_id))
    return HttpResponse(json.dumps(result))