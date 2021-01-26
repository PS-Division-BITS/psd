from django.contrib import admin
from .models import *

admin.site.register(PS2TSTransfer)
admin.site.register(TS2PSTransfer)
admin.site.register(ActiveUserProfile)
admin.site.register(DeadlineModel)

# Register your models here.
