from django.db import models

# Create your models here.

class Member(models.Model):
    english_name = models.CharField(max_length=255)
    chinese_name = models.CharField(max_length=255, null=True)
    email = models.EmailField()
    password = models.CharField(max_length=255)
    student_id = models.IntegerField()
    membership_years_duration = models.PositiveSmallIntegerField(null=True)
    membership_start_date = models.DateField(null=True)
    paid = models.BooleanField(null=True)
    is_admin = models.BooleanField(default=0)
    is_active = models.BooleanField()

