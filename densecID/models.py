from django.db import models

# Create your models here.
# The class describes the schema for the database
class dendrites(models.Model):
    dendID = models.CharField(max_length=20)
    dendPic = models.BinaryField()
    prod_name = models.CharField(max_length=50)
    prod_disc = models.CharField(max_length=100)
    prod_category = models.CharField(max_length=50)
    mfg_date = models.CharField(max_length=20)
    exp_date = models.CharField(max_length=20) 
    def __str__(self):
        return self.prod_name
    
