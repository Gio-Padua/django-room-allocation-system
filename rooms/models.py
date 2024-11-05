from django.db import models
from django.utils import timezone

ZONE_CHOICES = [
    ('p1', 'Zone 1'),
    ('p2', 'Zone 2'),
    ('p3', 'Zone 3'),
    ('p4', 'Zone 4'),
    ('p5', 'Zone 5'),
    ('p6', 'Zone 6'),
    ('p7', 'Zone 7'),
    ('p8', 'Zone 8'),

]
PRIORITY_CATEGORY =[
     ('SC', 'Senior Citizen'),
     ('PWD', 'Person with Disability'),
     ('P', 'Pregnant'), 
     ('SC & PWD', 'Senior Citizen and PWD'),
     ('SC & P', 'Senior Citizen and Pregnant'),
     ('PWD & P', 'PWD and Pregnant'),
     ('ALL', 'Senior Citizen, PWD, and Pregnant'),
     ('NONE', 'None'),
]
class Resident(models.Model):
    fname = models.CharField(max_length=75, default="Add First Name")
    lname = models.CharField(max_length=75, default="Add Last Name")
    address = models.CharField(max_length=55,
        choices=ZONE_CHOICES,
        default='Zone 1',)
    street = models.CharField(max_length=75, default='Gil Malungkot Street',)
    family_size = models.PositiveIntegerField(default=1)

    
    priority_members = models.PositiveIntegerField(default=0)
    priority_category = models.CharField(max_length=55,
        choices=PRIORITY_CATEGORY,
        default='NONE',)
    priority = models.BooleanField(default=False)
    assigned = models.BooleanField(default=False)
    date = models.DateTimeField(default=timezone.now, editable=True)

    class Meta:
        verbose_name_plural = "Residents"
    def __str__(self):

        return self.lname +', '+self.fname 

class Room(models.Model):
    name = models.CharField(max_length=75, default="Room 101")
    building = models.CharField(max_length=80, default="Tower of God")
    capacity = models.PositiveIntegerField(default=15)
    priority = models.BooleanField(default=False)
    class Meta:
        constraints = [
            models.CheckConstraint(
                check=models.Q(capacity__lte=20),
                name='capacity_not_exceed_20'
            )
        ]
        verbose_name_plural = "Rooms"
    def __str__(self):

            return self.name


class Allocation(models.Model):
    resident = models.ForeignKey(Resident, on_delete=models.CASCADE, default='1')
    room = models.ForeignKey(Room, on_delete=models.CASCADE, default='1')
    date = models.DateTimeField(default=timezone.now)
    class Meta:
        verbose_name_plural = "Allocations"
    
    def __str__(self):

        return self.room.name +"  "+ self.resident.lname+ " " + self.resident.fname
    

