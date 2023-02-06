from django.contrib import admin
from .models import Sessions
from .models import PriorityRecord

# Register your models here.
admin.site.register(Sessions)
admin.site.register(PriorityRecord)