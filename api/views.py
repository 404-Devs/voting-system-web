from django.shortcuts import render
from django.http import HttpResponse
from .models import Voter
import hashlib
import json
import binascii

def voter_login(request):
    reg_no = request.POST.get("reg_no")
    password = request.POST.get("password")
    result = {}
    try:
        voter = Voter.objects.get(voter_reg_no=reg_no)
        pwdhash = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), voter.password_salt.encode('utf-8'), 100000)
        pwdhash = binascii.hexlify(pwdhash)
        print(voter.voter_password, pwdhash.decode('ascii'))
        if voter.voter_password == pwdhash.decode('ascii'):
            result['status'] = 'success'
            result['data'] = {'id': voter.voter_id, 'reg_no': voter.voter_reg_no, 'email': voter.email, 'school_id': voter.school_id.school_id}
        else:
            result['status'] = 'error'
    except Voter.DoesNotExist:
        result['status'] = 'error'
    return HttpResponse(json.dumps(result))
