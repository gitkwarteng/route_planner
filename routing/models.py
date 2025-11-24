from django.contrib.gis.db import models

class FuelStation(models.Model):
    opis_id = models.CharField(max_length=50)
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=2, db_index=True)
    rack_id = models.IntegerField()
    price = models.DecimalField(max_digits=12, decimal_places=9, db_index=True)
    location = models.PointField(geography=True, spatial_index=True)
    
    class Meta:
        verbose_name = "Fuel Station"
        verbose_name_plural = "Fuel Stations"
