from django.db import models

class State(models.Model):
    state_code = models.IntegerField(unique=True) 
    state_name = models.CharField(max_length=30)

    class Meta:
        app_label = 'stp'

    def __str__(self):
        return self.state_name


class District(models.Model):
    district_code = models.IntegerField(unique=True)
    district_name = models.CharField(max_length=30)
    state = models.ForeignKey(State, on_delete=models.CASCADE, to_field='state_code', related_name='districts')

    class Meta:
        app_label = 'stp'

    def __str__(self):
        return f"{self.district_name}, {self.state.state_name}"


class SubDistrict(models.Model):
    subdistrict_code = models.IntegerField(unique=True)
    subdistrict_name = models.CharField(max_length=100)
    district = models.ForeignKey(District, on_delete=models.CASCADE, to_field='district_code', related_name='subdistricts')

    class Meta:
        app_label = 'stp'

    def __str__(self):
        return f"{self.subdistrict_name}, {self.district.district_name}"


class Village(models.Model):  # Changed from Villages to Village
    village_code = models.IntegerField(unique=True)  # Added unique=True
    village_name = models.CharField(max_length=100)
    subdistrict = models.ForeignKey(SubDistrict, on_delete=models.CASCADE, to_field='subdistrict_code', related_name='villages')
    sewage_gap = models.DecimalField(max_digits=20, decimal_places=10)
    mean_temperature = models.DecimalField(max_digits=20, decimal_places=10)
    mean_rainfall = models.DecimalField(max_digits=20, decimal_places=10)
    number_of_tourists = models.IntegerField()
    water_quality_index = models.DecimalField(max_digits=20, decimal_places=10)
    number_of_asi_sites = models.IntegerField()
    gdp_at_current_prices = models.DecimalField(max_digits=20, decimal_places=10)
    
    class Meta:
        app_label = 'stp'

    def __str__(self):  # Added __str__ method for better readability
        return f"{self.village_name}, {self.subdistrict.subdistrict_name}"


class Weight(models.Model):
    sewage_gap = models.FloatField()
    mean_temperature = models.FloatField()
    mean_rainfall = models.FloatField()
    number_of_tourists = models.FloatField()
    water_quality_index = models.FloatField()
    number_of_asi_sites = models.FloatField()
    gdp_at_current_prices = models.FloatField()

    class Meta:
        app_label = 'stp'
        
    def __str__(self):  # Added __str__ method for better readability
        return f"Weight configuration #{self.id}"