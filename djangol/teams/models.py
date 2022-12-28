from django.db import models
from PIL import Image

# Create your models here.
class Team(models.Model):
    """Un tema sobre lo que ha aprendido el usuario."""
    name = models.CharField(max_length=200)
    profile = models.CharField(max_length=1000)
    date_added = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='uploads/%name', height_field=None, width_field=None, null=True, blank=True)

    def __str__(self):
        """Devuelve una representación del modelo como cadena."""
        return self.name


class Country(models.Model):
    """Un tema sobre lo que ha aprendido el usuario."""
    name = models.CharField(max_length=200)
    image = models.ImageField(upload_to='uploads/countries', height_field=None, width_field=None, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """Devuelve una representación del modelo como cadena."""
        return self.name

class Player(models.Model):
    """Un tema sobre lo que ha aprendido el usuario."""
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    name = models.CharField(max_length=300)
    date_added = models.DateTimeField(auto_now_add=True)
    position = models.CharField(max_length=300)
    birth = models.CharField(max_length=300)
    age = models.CharField(max_length=300)
    birth = models.CharField(max_length=300)
    height = models.CharField(max_length=300)
    foot = models.CharField(max_length=300)
    sing_date = models.CharField(max_length=300)
    end_contract = models.CharField(max_length=300)
    market_value = models.CharField(max_length=300)
    image = models.ImageField(upload_to='uploads/%team', height_field=None, width_field=None, null=True, blank=True)
    class Meta:
        verbose_name_plural = 'players'
    def __str__(self):
        """Devuelve una representación del modelo como cadena."""
        return self.name
