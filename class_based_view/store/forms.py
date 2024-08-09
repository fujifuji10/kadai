from django import forms #絶対必要
from .models import Books, Pictures #booksにデータをそうにゅうするため
from datetime import datetime #現在時刻を表記するため

class BookForm(forms.ModelForm):
  
  class Meta:
    model = Books
    fields = ['name', 'description', 'price'] #bookformを実施するとsaveメソッドが呼び出されて、データがsaveされるようにしたい。saveメソッドを下でカスタマイズする
    
  def save(self, *args, **kwargs):
    obj = super(BookForm, self).save(commit=False) #classのobjがobjに入る。
    obj.create_at = datetime.now() #このdatetime(現在時刻)は標準ライブラリを使用（datetimeをインポート要)
    obj.update_at = datetime.now()
    obj.save()
    return obj
  
class BookUpdateForm(forms.ModelForm):
  
  class Meta:
    model = Books
    fields = ['name', 'description', 'price'] 
    
  def save(self, *args, **kwargs):
    obj = super(BookUpdateForm, self).save(commit=False) #classのobjがobjに入る。
    obj.update_at = datetime.now()
  #create_atは今回更新のみなので削除
    obj.save()
    return obj
  
class PictureUploadForm(forms.ModelForm):
  picture = forms.FileField(required=False)
  
  class Meta:
    model = Pictures
    fields = ['picture',]
  
  def save(self, *args, **kwargs):
    obj = super(PictureUploadForm, self).save(commit=False)
    obj.create_at = datetime.now()
    obj.update_at = datetime.now()
    obj.book = kwargs['book']
    obj.save()
    return obj