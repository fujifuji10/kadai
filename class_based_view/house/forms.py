from django import forms #絶対必要
from .models import Housings, HousingPictures #booksにデータをそうにゅうするため
from datetime import datetime #現在時刻を表記するため
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.forms import AuthenticationForm

class HouseAddForm(forms.ModelForm):
  name = forms.CharField(label='物件名')
  zip_code = forms.IntegerField(label='郵便番号')
  address = forms.CharField(label='住所')
  distance = forms.CharField(label='最寄駅からの距離')
  price = forms.IntegerField(label='家賃')
  floor = forms.CharField(label='間取り')
  house_kind = forms.CharField(label='物件の種類')
  constraction = forms.CharField(label='築年数')
  floor_number = forms.CharField(label='階数')
  picture = forms.FileField(label='写真', required=False)
    
  class Meta:
    model = Housings
    fields = ['name', 'zip_code', 'address', 'distance', 'price', 'floor', 'house_kind', 'constraction', 'floor_number', 'picture']
    
  def save(self, *args, **kwargs):
    obj = super(HouseAddForm, self).save(commit=False) #classのobjがobjに入る。
    obj.create_at = datetime.now() #このdatetime(現在時刻)は標準ライブラリを使用（datetimeをインポート要)
    obj.update_at = datetime.now()
    obj.save()
    return obj
  
class HouseUpdateForm(forms.ModelForm):
  name = forms.CharField(label='物件名')
  zip_code = forms.IntegerField(label='郵便番号')
  address = forms.CharField(label='住所')
  distance = forms.CharField(label='最寄駅からの距離')
  price = forms.IntegerField(label='家賃')
  floor = forms.CharField(label='間取り')
  house_kind = forms.CharField(label='物件の種類')
  constraction = forms.CharField(label='築年数')
  floor_number = forms.CharField(label='階数')
  picture = forms.FileField(label='写真', required=False)
  
  class Meta:
    model = Housings
    fields = ['name', 'zip_code', 'address', 'distance', 'price', 'floor', 'house_kind', 'constraction', 'floor_number', 'picture']
    
  def save(self, *args, **kwargs):
    obj = super(HouseUpdateForm, self).save(commit=False) #classのobjがobjに入る。
    obj.update_at = datetime.now()
  #create_atは今回更新のみなので削除
    obj.save()
    return obj
  
class PictureUploadForm(forms.ModelForm):
  picture = forms.FileField(required=False)
  
  class Meta:
    model = HousingPictures
    fields = ['picture',]
  
  def save(self, *args, **kwargs):
    obj = super(PictureUploadForm, self).save(commit=False)
    obj.create_at = datetime.now()
    obj.update_at = datetime.now()
    obj.book = kwargs['book']
    obj.save()
    return obj
  
# class RegistForm(forms.ModelForm):
#     username = forms.CharField(label='名前')
#     age = forms.IntegerField(label='年齢', min_value=0)
#     email = forms.EmailField(label='メールアドレス')
#     password = forms.CharField(label='パスワード', widget=forms.PasswordInput())
    
#     class Meta:
#       model = Users
#       fields = ['username', 'age', 'email', 'password']
      
#     def save(self, commit=False):
#       user = super().save(commit=False)
#       validate_password(self.cleaned_data['password'], user)
#       user.set_password(self.cleaned_data['password'])
#       user.save()
#       return user
    
class UserLoginForm(forms.ModelForm):
  email = forms.EmailField(label='メールアドレス')
  password = forms.CharField(label='パスワード', widget=forms.PasswordInput())
  
# class HouseAddForm(forms.ModelForm):
#     name = forms.CharField(label='物件名')
#     zip_code = forms.IntegerField(label='郵便番号')
#     address = forms.CharField(label='住所')
#     distance = forms.CharField(label='最寄駅からの距離')
#     price = forms.IntegerField(label='家賃')
#     floor = forms.CharField(label='間取り')
#     house_kind = forms.CharField(label='物件の種類')
#     constraction = forms.CharField(label='築年数')
#     floor_number = forms.CharField(label='階数')
    
#     class Meta:
#       model = Housings
#       fields = ['name', 'zip_code', 'address', 'distance', 'price', 'floor', 'house_kind', 'constraction', 'floor_number']