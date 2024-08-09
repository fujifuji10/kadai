from django.db import models
from datetime import datetime, timedelta, timezone

# Create your models here.
class HousingManager(models.Manager):
  
  def fetch_all_housing(self):
    return self.order_by('id').all()

class Housing(models.Model):
  name = models.CharField(max_length=100)
  address = models.CharField(max_length=200)
  size = models.CharField(max_length=15, null=True)
  price = models.IntegerField()
  
  objects = HousingManager()
  
  class Meta:
    db_table = 'housing'
    
  def __str__(self):
    return self.name
  
# class HousingPicturesManager(models.Manager):
#     def fetch_by_housing_id(self, id):
#       return self.filter(id=id).order_by('id').all() 
  
class HousingPictures(models.Model):
  picture = models.FileField(upload_to='picture/')
  house = models.ForeignKey(
    Housing, on_delete=models.CASCADE
  )
  # objects = HousingPicturesManager()
  
  class Meta:
    db_table = 'housing_pictures'
    
  def __str__(self):
    return self.house.name
  
class HouseCommentsManager(models.Manager):
  def fetch_by_pk(self, pk):
    return self.filter(id=pk).order_by('pk').all() 
    
class HouseComments(models.Model):
  
  comment = models.CharField(max_length=1000)
  user = models.ForeignKey(
    'accounts.Users', on_delete=models.CASCADE
  )
  objects = HouseCommentsManager()
  
  class Meta:
    db_table = 'house_comments'
    
  def __str__(self):
    return self.comment
  
class DetailHouse(models.Model):
  name = models.CharField(max_length=100)
  address = models.CharField(max_length=200)
  size = models.CharField(max_length=15, null=True)
  price = models.IntegerField()
  picture = models.ForeignKey(
    HousingPictures, on_delete=models.CASCADE
  )
  
  class Meta:
    db_table = 'detail_house'
    
    def __str__(self):
      return self.name