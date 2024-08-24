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
class Resident(models.Model):
    name = models.CharField(max_length=75, default="Juan Luna")
    address = models.CharField(max_length=55,
        choices=ZONE_CHOICES,
        default='Zone 1',)
    family_size = models.PositiveIntegerField(default=1)
    priority = models.BooleanField(default=False)
    assigned = models.BooleanField(default=False)
    class Meta:
        verbose_name_plural = "Residents"
    def __str__(self):

        return self.name 

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

            return self.room.name +"  "+ self.resident.name
    

