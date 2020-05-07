from django.db import models
import time

def to_unix(t_time):
    return int(time.mktime(t_time.timetuple()))

class Admin(models.Model):
    admin_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    user_name = models.CharField(max_length=50, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    password_salt = models.CharField(max_length=255)
    login_attempts = models.IntegerField(default=10)

class School(models.Model):
    school_id = models.AutoField(primary_key=True)
    school_name = models.CharField(max_length=255, unique=True)
    last_modified = models.DateTimeField(auto_now_add=True)

class Voter(models.Model):
    voter_id = models.AutoField(primary_key=True)
    voter_reg_no = models.CharField(max_length=50, unique=True)
    email = models.EmailField(unique=True)
    voter_password = models.CharField(max_length=255)
    password_salt = models.CharField(max_length=255)
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    login_attempts = models.IntegerField(default=10)

class Election(models.Model):
    election_id = models.AutoField(primary_key=True)
    election_name = models.CharField(max_length=100)
    start_timestamp = models.DateTimeField(auto_now_add=False)
    end_timestamp = models.DateTimeField(auto_now_add=False)
    last_modified = models.DateTimeField(auto_now_add=True)

    @property
    def start_unix(self):
        return to_unix(self.start_timestamp)

    @property
    def end_unix(self):
        return to_unix(self.end_timestamp)

    @property
    def last_mod_unix(self):
        return to_unix(self.last_modified)

class Aspirant(models.Model):
    aspirant_id = models.AutoField(primary_key=True)
    voter = models.OneToOneField(Voter, on_delete=models.CASCADE)
    fname = models.CharField(max_length=50)
    lname = models.CharField(max_length=50)
    aspirant_photo = models.TextField()
    message = models.TextField()
    last_modified = models.DateTimeField(auto_now_add=True)

    @property
    def name(self):
        return self.fname + " " + self.lname

class Team(models.Model):
    team_id = models.AutoField(primary_key=True)
    team_name = models.CharField(max_length=255)
    team_logo = models.TextField()
    slogan = models.TextField()
    election = models.ForeignKey(Election, on_delete=models.CASCADE)
    chairman = models.ForeignKey(Aspirant, related_name='chairman_id', on_delete=models.CASCADE)
    sec_gen = models.ForeignKey(Aspirant, related_name='sec_gen_id', on_delete=models.CASCADE)
    treasurer = models.ForeignKey(Aspirant, related_name='treasurer_id', on_delete=models.CASCADE)
    last_modified = models.DateTimeField(auto_now_add=True)

class Vote(models.Model):
    vote_id = models.AutoField(primary_key=True)
    voter = models.ForeignKey(Voter, on_delete=models.CASCADE)
    election = models.ForeignKey(Election, on_delete=models.CASCADE)
    last_modified = models.DateTimeField(auto_now_add=True)
