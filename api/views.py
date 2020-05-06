from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from .models import Admin, Voter, School, Election, Aspirant, Team, Vote
import hashlib
import json
import binascii
import os


result = {'status': 'error'}

def admin_login(request):
    # get values passed in the POST object
    username = request.POST.get("username")
    pword = request.POST.get('password')
    # make sure that the POST values are not empty
    if all([username, pword]):
        try:
            admin = Admin.objects.get(user_name=username)
            if admin.login_attempts == 0:
                result['msg'] = "Account temporarily blocked, you have made too many login attempts. Please see the system administrator"
                return HttpResponse(json.dumps(result))
            # hashed password
            pwdhash = hashlib.pbkdf2_hmac('sha512', pword.encode('utf-8'), admin.password_salt.encode('utf-8'),
                                          100000)
            pwdhash = binascii.hexlify(pwdhash)
            # password checking
            if admin.password == pwdhash.decode('ascii'):
                if admin.login_attempts != 10:
                    admin.login_attempts = 10
                    admin.save()
                result['status'] = 'success'
                result['data'] = {'id': admin.admin_id, 'fname': admin.first_name, 'lname': admin.last_name,
                                  'uname': admin.user_name, 'email': admin.email}
                result['msg'] = 'Authentication successful.'
            else:
                admin.login_attempts -= 1
                admin.save()
                result['msg'] = 'Authentication failed.'
                result['n'] = admin.login_attempts
        except Admin.DoesNotExist:
            result['msg'] = 'User does not exist with administration rights.'
    else:
        result['msg'] = 'Make sure that you provide all the required values.'

# TODO: Admins Only
def admin_reg(request):
    f_name = request.POST.get('first_name')
    l_name = request.POST.get('last_name')
    email1 = request.POST.get('email')
    pword = request.POST.get('password')
    u_name = request.POST.get('username')
    # check if the post is not empty
    if all([f_name, l_name, email1, pword, u_name]):
        # find a random salt
        salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
        # hash the password
        pwdhash = hashlib.pbkdf2_hmac('sha512', pword.encode('utf-8'), salt, 100000)
        pwdhash = binascii.hexlify(pwdhash)

        try:
            # save the user
            Admin.objects.create(first_name=f_name, last_name=l_name, email=email1, user_name=u_name,
                                 password=pwdhash.decode('ascii'), password_salt=salt.decode('ascii'))
            result['status'] = 'success'
            result['msg'] = 'User successfully created.'
        except Admin.DoesNotExist:
            result['msg'] = 'Failed to create user'
    else:
        result['msg'] = 'Provide all the required values!'
    return HttpResponse(json.dumps(result))

# TODO: Admins Only
def delete_admin(request, id):
    admin = get_object_or_404(Admin, pk=id)
    admin.delete()
    result['status'] = 'success'
    return HttpResponse(json.dumps(result))

# TODO: Admins Only
def admin_update(request):
    f_name = request.POST.get('first_name')
    l_name = request.POST.get('last_name')
    email = request.POST.get('email')
    u_name = request.POST.get('username')
    if all([f_name, l_name, email, u_name]):
        try:
            admin = Admin.objects.get(username=u_name)
            admin.fname = f_name
            admin.lname = l_name
            admin.email = email
            admin.save()
            result['status'] = 'success'
            result['msg'] = 'Admin info updated successfully.'
        except Admin.DoesNotExist:
            result['msg'] = 'Admin does not exist.'
    else:
        result['msg'] = 'Make sure that you provide all the required values.'
    return HttpResponse(json.dumps(result))

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
                result['data'] = {'id': voter.voter_id, 'reg_no': voter.voter_reg_no, 'email': voter.email,
                                  'school_id': voter.school.school_id}
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

# TODO: Admins Only
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
    return HttpResponse(json.dumps(result))

# TODO: Admins Only
def delete_voter(request, id):
    voter = get_object_or_404(Voter, pk=id)
    voter.delete()
    result['status'] = 'success'
    return HttpResponse(json.dumps(result))

# TODO: Admins Only
def sch_reg(request):
    sch_name = request.POST.get("school_name")
    if sch_name is not None:
        School.objects.create(school_name=sch_name)
        result['status'] = 'success'
        result['msg'] = 'School created successfully.'
    else:
        result['msg'] = 'Make sure that you provide all the required values.'
    return HttpResponse(json.dumps(result))

# TODO: Admins Only
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
    return HttpResponse(json.dumps(result))

# TODO: Admins Only
def delete_sch(request, id):
    school = get_object_or_404(School, pk=id)
    school.delete()
    result['status'] = 'success'
    return HttpResponse(json.dumps(result))

# TODO: Admins Only
def election_reg(request):
    election_name = request.POST.get("election_name")
    start_timestamp = request.POST.get("start_timestamp")
    end_timestamp = request.POST.get("end_timestamp")
    if all([election_name, start_timestamp, end_timestamp]):
        Election.objects.create(election_name=election_name, start_timestamp=start_timestamp, end_timestamp=end_timestamp)
        result['status'] = 'success'
        result['msg'] = 'Election created successfully.'
    else:
        result['msg'] = 'Make sure that you provide all the required values.'
    return HttpResponse(json.dumps(result))

def get_elections(request):
    elections = Election.objects.all()
    result['status'] = 'success'
    result['data'] = {}
    result['msg'] = "Query successful"
    
    for data in elections:
        result['data'][data.election_id] = {'id': data.election_id, 'name': data.election_name, 'start': data.start_unix, 'end': data.end_unix, 'last_mod': data.last_mod_unix}
    return HttpResponse(json.dumps(result))

def get_election(request, election_id):
    election = get_object_or_404(Election, pk=election_id)
    teams = Team.objects.filter(election=election)
    result['status'] = 'success'
    result['data'] = {'id': election.election_id, 'name': election.election_name, 'start': election.start_unix, 'end': election.end_unix, 'last_mod': election.last_mod_unix}
    result['parties'] = {}

    for team in teams:
        result['parties'][team.team_id] = {'id': team.team_id, 'name': team.team_name, 'logo': team.team_logo, 'slogan': team.slogan, 'chairman_id': team.chairman.voter.voter_id, 'treasurer_id': team.treasurer.voter.voter_id, 'sec_gen_id': team.sec_gen.voter.voter_id}
    return HttpResponse(json.dumps(result))

# TODO: Admins Only
def delete_election(request, id):
    election = get_object_or_404(Election, pk=id)
    election.delete()
    result['status'] = 'success'
    return HttpResponse(json.dumps(result))

# TODO: Admins Only
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
    return HttpResponse(json.dumps(result))

# TODO: Admins Only
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
            result['status'] = 'success'
            result['msg'] = 'Aspirant added successfully.'
        except Voter.DoesNotExist:
            result['msg'] = 'Voter does not exist.'
    else:
        result['msg'] = 'Make sure that you provide all the required values.'
    return HttpResponse(json.dumps(result))

def get_aspirant(request, id):
    asp = get_object_or_404(Aspirant, pk=id)
    result['status'] = 'success'
    result['data'] = {'id': asp.aspirant_id, 'name': asp.name, 'photo': asp.aspirant_photo}
    return HttpResponse(json.dumps(result))

# TODO: Admins Only
def delete_aspirant(request, id):
    aspirant = get_object_or_404(Aspirant, pk=id)
    aspirant.delete()
    result['status'] = 'success'
    return HttpResponse(json.dumps(result))

# TODO: Admins Only
def aspirant_update(request):
    # TODO
    pass

# TODO: Admins Only
def team_reg(request):
    team_name = request.POST.get("team_name")
    team_logo = request.POST.get("team_logo")
    election_id = request.POST.get("election_id")
    chairman_id = request.POST.get("chairman_reg")
    sec_gen_id = request.POST.get("sec_gen_reg")
    treasurer_id = request.POST.get("treasurer_reg")
    slogan = request.POST.get("slogan")
    if all([team_name, team_logo, election_id, chairman_id, sec_gen_id, treasurer_id, slogan]):
        # TODO: Check if election_id, chairman_id, sec_gen_id and treasurer_id exist
        election = Election.objects.get(election_id=election_id)
        chairman = Aspirant.objects.get(voter=Voter.objects.get(voter_reg_no=chairman_id))
        sec_gen = Aspirant.objects.get(voter=Voter.objects.get(voter_reg_no=sec_gen_id))
        treasurer = Aspirant.objects.get(voter=Voter.objects.get(voter_reg_no=treasurer_id))
        Team.objects.create(team_name=team_name, team_logo=team_logo, election=election, chairman=chairman, sec_gen=sec_gen, treasurer=treasurer, slogan=slogan)
        result['status'] = 'success'
        result['msg'] = 'Team created successfully.'
    else:
        result['msg'] = 'Make sure that you provide all the required values.'
    return HttpResponse(json.dumps(result))

def get_team(request, id):
    team = get_object_or_404(Team, pk=id)
    result['status'] = 'success'
    result['data'] = {'id': team.team_id, 'name': team.team_name, 'logo': team.team_logo, 'slogan': team.slogan, 'chairman': team.chairman.name, 'chairman_id': team.chairman.voter.voter_id, 'chairman_photo': team.chairman.aspirant_photo, 'treasurer': team.treasurer.name, 'treasurer_id': team.treasurer.voter.voter_id, 'treasurer_photo': team.treasurer.aspirant_photo, 'sec_gen': team.sec_gen.name, 'sec_gen_id': team.sec_gen.voter.voter_id, 'sec_gen_photo': team.sec_gen.aspirant_photo}
    return HttpResponse(json.dumps(result))

# TODO: Admins Only
def delete_team(request, id):
    team = get_object_or_404(Team, pk=id)
    team.delete()
    result['status'] = 'success'
    return HttpResponse(json.dumps(result))

# TODO: Admins Only
def team_update(request):
    # TODO
    pass

# TODO: Admins Only
def vote(request):
    voter_id = request.POST.get("voter_reg")
    election_id = request.POST.get("election_id")
    if all([voter_id, election_id]):
        election = Election.objects.get(election_id=election_id)
        voter = Voter.objects.get(voter_reg_no=voter_id)
        # check if the voter has voted in this election before
        query = Vote.objects.filter(voter=voter, election=election)
        if query.count() > 0:
            result['msg'] = 'You have already voted. SMH.'
            return HttpResponse(json.dumps(result))

        Vote.objects.create(voter=voter, election=election)
        result['status'] = 'success'
        result['msg'] = 'You have voted successfully.'
    else:
        result['msg'] = 'Make sure that you provide all the required values.'
    return HttpResponse(json.dumps(result))