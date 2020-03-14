from django.shortcuts import render
from django.http import HttpResponse
from .models import Voter, School
import hashlib
import json
import binascii
import os


def voter_login(request):
    # TODO: Fix the number of times one can try a password before the account id blocked temporarily
    # get values passed in the POST object
    reg_no = request.POST.get("reg_no")
    password = request.POST.get("password")
    result = {}
    # make sure that the POST values are not empty
    if reg_no is not None and password is not None:
        try:
            # get voter with the specified registration number
            voter = Voter.objects.get(voter_reg_no=reg_no)
            # hash the passed password
            pwdhash = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'), voter.password_salt.encode('utf-8'),
                                          100000)
            pwdhash = binascii.hexlify(pwdhash)
            # check if the passwords are the same
            if voter.voter_password == pwdhash.decode('ascii'):
                result['status'] = 'success'
                result['data'] = {'id': voter.voter_id, 'reg_no': voter.voter_reg_no, 'email': voter.email,
                                  'school_id': voter.school_id.school_id}
                result['msg'] = 'Authentication successful.'
            else:
                result['status'] = 'error'
                result['msg'] = 'Authentication failed.'
        except Voter.DoesNotExist:
            result['status'] = 'error'
            result['msg'] = 'Voter does not exist.'
    else:
        result['status'] = 'error'
        result['msg'] = 'The school associated with the provided id does not exist.'
    # return a JSON object
    return HttpResponse(json.dumps(result))


def voter_registration(request):
    # TODO: Check if the registration numbers & emails have been registered before
    # TODO: Return specific error message if school doesn't exist in db
    # TODO: Make sure that only registered admins can do voter registration
    # get values passed in the POST object
    reg_no = request.POST.get("reg_no")
    email = request.POST.get('email')
    password = request.POST.get("password")
    school_id = request.POST.get("school_id")
    result = {}
    # make sure that the POST values are not empty
    if reg_no is not None and email is not None and password is not None and school_id is not None:
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
            result['status'] = 'error'
            result['msg'] = 'The school associated with the provided id does not exist.'
    else:
        result['status'] = 'error'
        result['msg'] = 'Make sure that you provide all the required values.'
    # return JSON object
    return HttpResponse(json.dumps(result))
