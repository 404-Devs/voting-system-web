from django.db import models

class Admin(models.Model):
    admin_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    user_name = models.CharField(max_length=50)
    email = models.EmailField()
    password = models.CharField(max_length=255)
    password_salt = models.CharField(max_length=255)
