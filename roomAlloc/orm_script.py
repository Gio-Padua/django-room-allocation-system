from .models import *
from django.db import connection
from django_seed import seeder

def run():
    obj, created = Resident.objects.get_or_create(name = "juan", address = "purok 2", family_size = "5")
    obj.save()
    print(Resident.objects.all())