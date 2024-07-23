from django import forms
from .models import Housing, HouseComments
from django.contrib.auth.password_validation import validate_password
from accounts.models import Users

class RegistHouseForm(forms.ModelForm):
  name = forms.CharField(label='物件名')
  address = forms.CharField(label='住所')
  price = forms.IntegerField(label='家賃', min_value=0)
  picture = forms.FileField(label='写真', required=False)
  
  class Meta():
    model = Housing
    fields = ('name', 'address', 'price', 'picture')
    
class EditHouseForm(forms.ModelForm):
  name = forms.CharField(label='物件名')
  address = forms.CharField(label='住所')
  price = forms.IntegerField(label='家賃', min_value=0)
  picture = forms.FileField(label='写真', required=False)
  
  class Meta:
    model = Housing
    fields = ('name','address', 'price', 'picture')
    
class DeleteHouseForm(forms.ModelForm):
  
  class Meta:
    model = Housing
    fields = []
    
class PostHouseCommentForm(forms.ModelForm):
  comment = forms.CharField(label='', widget=forms.Textarea(attrs={'rows': 5, 'cols': 60})) #rows=行数 cols=列幅（120/OO)
  
  class Meta:
    model = HouseComments
    fields = ('comment',)