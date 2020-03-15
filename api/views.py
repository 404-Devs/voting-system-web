from django.shortcuts import render
from django.http import HttpResponse
from .models import Voter, School
import hashlib
import json
import binascii
import os


def voter_login(request):
    # get values passed in the POST object
    reg_no = request.POST.get("reg_no")
    password = request.POST.get("password")
    result = {'status': 'error'}
    # make sure that the POST values are not empty
    if reg_no is not None and password is not None:
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
                                  'school_id': voter.school_id.school_id}
                result['msg'] = 'Authentication successful.'
            else:
                voter.login_attempts -= 1
                voter.save()
                result['msg'] = 'Authentication failed.'
                result['n'] = voter.login_attempts
        except Voter.DoesNotExist:
            result['msg'] = 'Voter does not exist.'
    else:
        result['msg'] = 'The school associated with the provided id does not exist.'
    # return a JSON object
    return HttpResponse(json.dumps(result))


def voter_registration(request):
    # TODO: Make sure that only registered admins can do voter registration
    # get values passed in the POST object
    reg_no = request.POST.get("reg_no")
    email = request.POST.get('email')
    password = request.POST.get("password")
    school_id = request.POST.get("school_id")
    result = {'status': 'error'}
    # make sure that the POST values are not empty
    if reg_no is not None and email is not None and password is not None and school_id is not None:
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
                                 password_salt=salt.decode('ascii'), school_id=school)
            result['status'] = 'success'
            result['msg'] = 'Voter created successfully.'
        except School.DoesNotExist:
            result['msg'] = 'The school associated with the provided id does not exist.'
    else:
        result['msg'] = 'Make sure that you provide all the required values.'
    # return JSON object
    return HttpResponse(json.dumps(result))
