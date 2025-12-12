from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(MedicalInfo)
admin.site.register(AnonQID)
admin.site.register(EncryptedID)
admin.site.register(EMR)