from django.contrib import admin
from .models import AddProject,AddNewHazard,AddSignup,AddDesignElement,AddActivity
# Register your models here.

admin.site.register(AddProject)
admin.site.register(AddNewHazard)
admin.site.register(AddSignup)
admin.site.register(AddDesignElement)
admin.site.register(AddActivity)
