from django.contrib import admin
from .models import Member



# Register your models here.

class MemberAdmin(admin.ModelAdmin):
  list_display = ("english_name", "email", "student_id", "membership_years_duration", "paid", "is_active", "is_admin")
  
admin.site.register(Member, MemberAdmin)