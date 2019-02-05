from django.contrib import admin
from .models import *

admin.site.register(Candidate)
admin.site.register(Role)
admin.site.register(Qualification)
admin.site.register(City)
admin.site.register(Industry)

