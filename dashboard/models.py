# from django.db import models
# from django.utils import timezone

# ZONE_CHOICES = [
#     (1, 'Zone 1'),
#     (2, 'Zone 2'),
#     (3, 'Zone 3'),
#     (4, 'Zone 4'),
#     (5, 'Zone 5'),
#     (6, 'Zone 6'),
#     (7, 'Zone 7'),
#     (8, 'Zone 8'),

# ]
# class Resident(models.Model):
#     name = models.CharField(max_length=75, default="Juan Luna")
#     address = models.CharField(max_length=55,
#         choices=ZONE_CHOICES,
#         default=1,)
#     family_size = models.PositiveIntegerField(default=1)
#     priority = models.BooleanField(default=False)
#     assigned = models.BooleanField(default=False)
#     class Meta:
#         verbose_name_plural = "Residents"

# class Room(models.Model):
#     name = models.CharField(max_length=75, default="Room 101")
#     building = models.CharField(max_length=80, default="Tower of God")
#     capacity = models.PositiveIntegerField(default=15)
#     priority = models.BooleanField(default=False)
#     class Meta:
#         constraints = [
#             models.CheckConstraint(
#                 check=models.Q(capacity__lte=20),
#                 name='capacity_not_exceed_20'
#             )
#         ]
#         verbose_name_plural = "Residents"


# class Allocation(models.Model):
#     resident = models.ForeignKey(Resident, on_delete=models.CASCADE, default='1')
#     Room = models.ForeignKey(Room, on_delete=models.CASCADE, default='1')
#     date = models.DateTimeField(default=timezone.now)
#     class Meta:
#         verbose_name_plural = "Allocations"
    

