from django.db.models.query import QuerySet
from django.shortcuts import render, redirect, get_object_or_404
from . import forms
from django.core.exceptions import ValidationError
from django.contrib import messages
from .models import Housing, HouseComments
from django.http import Http404
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
import os
from accounts.models import Users

# Create your views here.
class HousingListView(LoginRequiredMixin, ListView):
  model = Housing
  template_name = os.path.join('house', 'list_house.html')

# def list_house(request):
#   house = Housing.objects.fetch_all_housing()
#   return render(
#   request, 'house/list_house.html', context={
#     'house':house
#   }
#   )

# def edit_house(request, id):
#   house = get_object_or_404(Housing, id=id) #Housingをidからget_object_or_404から取得します
#   if house.user.id != request.user.id: #ログイン者のuser.idと編集希望者のリクエストのuser.idが違っていればエラーを発生させる
#     raise Http404
#   edit_house_form = forms.EditHouseForm(request.POST or None, instance=house)
#   if edit_house_form.is_valid():
#     edit_house_form.save()
#     messages.success(request, '物件情報を更新しました')
#     return redirect('house:list_house')
#   return render( #上のリダイレクトする場合以外は以下を渡してね（返す）
#     request, 'house/edit_house.html', context={
#       'edit_house_form':edit_house_form,
#       'id':id, #引数のIDをそのまま渡す
#     }
#   )
  
# def delete_house(request, id):
#   house = get_object_or_404(Housing, id=id)
#   if house.user.id != request.user.id:
#     raise Http404
#   delete_house_form = forms.DeleteHouseForm(request.POST or None)
#   if delete_house_form.is_valid(): #csrf_tokenのチェック！
#     house.delete()
#     messages.success(request, '物件を削除しました')
#     return redirect('house:list_house')
#   return render(
#     request, 'house/delete_house.html', context={
#       'delete_house_form':
#         delete_house_form
#     }
#   )

def post_house_comments(request, pk):
  post_house_comment_form = forms.PostHouseCommentForm(request.POST or None) #requestを送信した結果をコメントモデルに挿入するためのform
  house = get_object_or_404(Housing, pk=pk)
  comments = HouseComments.objects.fetch_by_pk(pk) #テーマに対してのコメントを全て取得
  if post_house_comment_form.is_valid():
    post_house_comment_form.instance.house = house #作成されたテーマが対象
    post_house_comment_form.instance.user = request.user #ログインしているログインユーザーが対象
    post_house_comment_form.save() #ここまでだとどのテーマに対するコメント？誰がコメント？かわからないので要素を入れる
    return redirect('house:post_house_comments', pk=pk)
  return render(
    request, 'house/post_house_comments.html', context={
      'post_house_comment_form':post_house_comment_form,
      'comments':comments,
    }
  )
  

  
class HouseDetailView(LoginRequiredMixin, DetailView):
  model = Housing
  template_name = os.path.join('house', 'detail_house.html')