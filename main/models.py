from django.db import models

# Create your models here.

class PriorityRecord(models.Model):
    member_email = models.CharField(max_length=200)
    week = models.CharField(max_length=250, default="", null=True)


class Sessions(models.Model):
    date = models.CharField(max_length=250)
    member_email = models.CharField(max_length=250)
    session_choice = models.IntegerField()    #Which session the student chooses
    session_flexible =  models.BooleanField(default=0)   #Whether or not the student allowed being switched to another session if full
    session_assigned = models.IntegerField(default=0)    #Which student has been successfully assigned, if not assigned, it will be 0
    attended = models.BooleanField(default=0)