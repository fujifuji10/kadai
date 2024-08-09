from django.db import models
from django.urls import reverse_lazy
from django.dispatch import receiver
import os
import logging

application_logger = logging.getLogger('application-logger')

class BaseModel(models.Model):
  create_at = models.DateTimeField()
  update_at = models.DateTimeField()
  
  class Meta:
    abstract = True #abstractクラスとして抽象的なモデルを作成※実際のモデルは下に定義
    
class Housings(BaseModel): 
#Basemodelを継承することで、create_atとupdate_atを使うことができる。
  name = models.CharField(max_length=255)
  price = models.IntegerField()
  zip_code = models.IntegerField(null=True)
  address = models.CharField(max_length=100, null=True)
  distance = models.CharField(max_length=30, null=True)
  floor = models.CharField(max_length=10, null=True)
  house_kind = models.CharField(max_length=20, null=True)
  constraction = models.IntegerField(null=True)
  floor_number = models.IntegerField(null=True)
  picture = models.ForeignKey(
    'HousingPictures', on_delete=models.CASCADE, blank=True, null=True
  )
  
  class Meta:
    db_table = 'housing'
  
class HousingPicturesManager(models.Manager):
  def filter_by_book(self, book):
    return self.filter(book=book).all()
  
class HousingPictures(BaseModel):
  
  picture = models.FileField(upload_to='housing_pictures/')
  housing = models.ForeignKey(
    'Housings', on_delete=models.CASCADE
  )
  order = models.IntegerField(blank=True, null=True)
  objects = HousingPicturesManager()
  
  class Meta:
    db_table = 'housing_pictures'
    ordering = ['order']
    
  def __str__(self):
    return self.housing.name + ': ' + str(self.order)
  
@receiver(models.signals.post_delete, sender=HousingPictures)
def delete_picture(sender, instance, **kwargs):
  if instance.picture:
    if os.path.isfile(instance.picture.path):
      os.remove(instance.picture.path)
      application_logger.info(f'{instance.picture.path}を削除しました')