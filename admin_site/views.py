from django.shortcuts import render

from django.http import HttpResponse
from .models import Admin
import hashlib
import json
import binascii
import os



def admin_login(request):
    username = request.POST.get("username")
    pword = request.POST.get('password')
    result = {}
    if username is not None and pword is not None:
        try:
            admin = Admin.objects.get(user_name=username)
            # hashed password
            pwdhash = hashlib.pbkdf2_hmac('sha512', pword.encode('utf-8'), admin.password_salt.encode('utf-8'),
                                          100000)
            pwdhash = binascii.hexlify(pwdhash)
            # password checking
            if admin.password == pwdhash.decode('ascii'):
                result['status'] = 'success'
                result['data'] = {'id': admin.admin_id, 'fname': admin.first_name, 'lname': admin.last_name,
                                  'uname': admin.user_name, 'email': admin.email}
                result['msg'] = 'Authentication successful.'
            else:
                result['status'] = 'error'
                result['msg'] = 'Authentication failed.'
        except Admin.DoesNotExist:
            result['status'] = 'error'
            result['msg'] = 'User does not exist with administration rights.'

    else:
        result['status'] = 'error'
        result['msg'] = 'User does not exit'
    # return a response of json object
    return HttpResponse(json.dumps(result))


def admin_registration(request):
    f_name = request.POST.get('first_name')
    l_name = request.POST.get('last_name')
    email1 = request.POST.get('email')
    pword = request.POST.get('password')
    u_name = request.POST.get('username')
    result = {}
    # check if the post is not empty
    if f_name is not None and l_name is not None and email1 is not None and pword is not None and u_name is not None:
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
            result['status'] = 'error'
            result['msg'] = 'Failed to create user'
    else:
        result['status'] = 'error'
        result['msg'] = 'Provide all the required values!'
    return HttpResponse(json.dumps(result))
