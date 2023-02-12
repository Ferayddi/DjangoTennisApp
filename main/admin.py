from django.contrib import admin
from .models import Sessions
from .models import PriorityRecord

# Register your models here.
class SessionsAdmin(admin.ModelAdmin):
  list_display = ("date", "member_email", "session_choice", "session_flexible", "session_assigned", "attended")

admin.site.register(Sessions, SessionsAdmin)
admin.site.register(PriorityRecord)