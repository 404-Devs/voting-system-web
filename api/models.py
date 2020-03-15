from django.db import models

class School(models.Model):
    school_id = models.AutoField(primary_key=True)
    school_name = models.CharField(max_length=255)

class Voter(models.Model):
    voter_id = models.AutoField(primary_key=True)
    voter_reg_no = models.CharField(max_length=50)
    email = models.EmailField()
    voter_password = models.CharField(max_length=255)
    password_salt = models.CharField(max_length=255)
    school_id = models.ForeignKey(School, on_delete=models.CASCADE)
    login_attempts = models.IntegerField(default=10)

class Election(models.Model):
    election_id = models.AutoField(primary_key=True)
    election_name = models.CharField(max_length=100)
    start_timestamp = models.DateTimeField(auto_now_add=True)
    end_timestamp = models.DateTimeField(auto_now_add=True)

class Aspirant(models.Model):
    aspirant_id = models.AutoField(primary_key=True)
    voter_id = models.ForeignKey(Voter, on_delete=models.CASCADE)
    aspirant_photo = models.ImageField(upload_to='aspirant_photos')

class Team(models.Model):
    team_id = models.AutoField(primary_key=True)
    team_name = models.CharField(max_length=255)
    team_logo = models.ImageField(upload_to='team_logos')
    election_id = models.ForeignKey(Election, on_delete=models.CASCADE)
    chairman_id = models.ForeignKey(Aspirant, related_name='chairman_id', on_delete=models.CASCADE)
    sec_gen_id = models.ForeignKey(Aspirant, related_name='sec_gen_id', on_delete=models.CASCADE)
    treasurer_id = models.ForeignKey(Aspirant, related_name='treasurer_id', on_delete=models.CASCADE)
    blockchain_address = models.CharField(max_length=255)

class Vote(models.Model):
    vote_id = models.AutoField(primary_key=True)
    voter_id = models.ForeignKey(Voter, on_delete=models.CASCADE)
    election_id = models.ForeignKey(Election, on_delete=models.CASCADE)
