from django.db import models


class StoreMaster(models.Model):
    store_id = models.CharField(max_length=12)
    store_name = models.CharField(max_length=70, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    state_code = models.CharField(max_length=2, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    city_code = models.CharField(max_length=2, blank=True, null=True)
    status = models.CharField(max_length=1, blank=True, null=True)
    outlet_type = models.CharField(max_length=9)
    store_type = models.CharField(max_length=26)
    store_created_date = models.DateTimeField(blank=True, null=True)
    pincode = models.IntegerField(blank=True, null=True)
    latitude = models.DecimalField(max_digits=18, decimal_places=9, blank=True, null=True)
    longitude = models.DecimalField(max_digits=18, decimal_places=9, blank=True, null=True)
    address = models.CharField(max_length=255, null=True)

    class Meta:
        managed = True



# With 5 -6 instruction able get this model properly

class StoreCompetition(models.Model):
    store = models.ForeignKey(StoreMaster, on_delete=models.CASCADE)
    year = models.IntegerField(blank=True, null=True)
    week = models.IntegerField(blank=True, null=True)
    competition_store_name = models.CharField(max_length=70, blank=True, null=True)
    competition_store_uid = models.CharField(max_length=50, blank=True, null=True)
    competition_store_type = models.CharField(max_length=26, blank=True, null=True)
    competition_store_latitude = models.DecimalField(max_digits=18, decimal_places=10, null=False)
    competition_store_longitude = models.DecimalField(max_digits=18, decimal_places=10, null=False)
    competition_store_address = models.CharField(max_length=255, null=True)
    competition_store_distance = models.DecimalField(max_digits=18, decimal_places=2, null=False)
    competition_store_status = models.CharField(max_length=30, blank=True, null=True)
    updated_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = True
        unique_together = (('store', 'year', 'week', 'competition_store_uid'),)
        indexes = [
            models.Index(fields=['store', 'year', 'week', 'competition_store_uid'],
                         name='store_competition_idx'),
        ]
