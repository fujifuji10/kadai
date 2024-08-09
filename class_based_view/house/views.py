from typing import Any
from django.db.models.query import QuerySet
from django.forms import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.base import (
  View,TemplateView,RedirectView
)
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import (
  CreateView, UpdateView, DeleteView, FormView,
)
from . import forms
from datetime import datetime
from django.contrib import messages
from .models import Housings, HousingPictures
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from .forms import PictureUploadForm, UserLoginForm, HouseAddForm, HouseUpdateForm
import logging
from django.http import Http404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin
import os

application_logger = logging.getLogger('application-logger') #settings.pyのloggersに記載しているので呼び出すと記載の設定で作成してくれる。
error_logger= logging.getLogger('error-logger')
    
class HomeView(TemplateView):
  template_name = 'account/home.html'
  
class UserLoginView(FormView):
  template_name = 'account/user_login.html'
  form_class = UserLoginForm
  
  def post(self, request, *args, **kwargs):
    email = request.POST['email']
    password = request.POST['password']
    user = authenticate(email=email, password=password)
    if user is not None and user.is_active:
      login(request, user)
    return redirect('account:home')
  
class UserLogoutView(View):
  
  def get(self, request, *args, **kwargs):
    logout(request)
    return redirect('account:user_login')

  # def get_context_data(self, **kwargs):
  #   context = super().get_context_data(**kwargs)
  #   application_logger.debug('Home画面を表示します')
  #   if kwargs.get('name') == 'ああああ':
  #      #エラーログの出力 今まではアプリケーションを記載していいたが、settings.pyに設定したエラーログを使用
  #     # error_logger.error('この名前は利用できません')
  #     raise Http404('この名前は使用できません')
  #   context['name'] = kwargs.get('name')
  #   context['time'] = datetime.now()
  #   return context
# datetime.nowを実施した結果をコンテキストのtimeの中に入れてreturn contextでcontextを返す
class HouseDetailView(LoginRequiredMixin,DetailView):
  model = Housings
  template_name = os.path.join('house', 'house_detail.html')
  
  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    print(context)
    # context['form'] = forms.BookForm()
    return context
  
class HousingListView(ListView):
  model = Housings #一覧表示するモデル
  template_name = 'house/list_house.html' #表示するテンプレートの名前
  
  def get_queryset(self):
    query = super().get_queryset()
    name = self.request.GET.get('housing.name', None)
    if name:
      query = query.filter(
        name__icontains = name
      )
    distance = self.request.GET.get('housing.distance', None)
    if distance:
      query = query.filter(
        distance__icontains = distance
      )
    order_by_price = self.request.GET.get('order_by_price', 0)
    if order_by_price == '1':
      query = query.order_by('price')
    elif order_by_price == '2':
      query = query.order_by('-price')
    return query
    
  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['housing.name'] = self.request.GET.get('housing.name', '')
    context['housing.distance'] = self.request.GET.get('housing.distance', '')
    order_by_price = self.request.GET.get('order_by_price')
    if order_by_price == '1':
      context['ascending'] = True
    elif order_by_price == '2':
      context['descending'] = True
    return context
  
class HouseCreateView(CreateView):
  model = Housings
  template_name = 'house/house_add.html'
  form_class = HouseAddForm
  success_url = reverse_lazy('house:list_house')
  
  def form_valid(self, form):
    form.instance.create_at = datetime.now()
    form.instance.update_at = datetime.now()
    return super(HouseCreateView, self).form_valid(form)
  
  # def get_initial(self, **kwargs):
  #   initial = super(BookCreateView, self).get_initial(**kwargs)
  #   initial['name'] = 'sample'
  #   return initial
  
class HouseUpdateView(SuccessMessageMixin, UpdateView):
  template_name = 'house/house_update.html'
  model = Housings
  form_class = forms.HouseUpdateForm
  success_message = '更新に成功しました'
  
  def get_success_url(self):
    print(self.object)
    return reverse_lazy('house/house:list_house', kwargs={'id': self.object.id})
  
  def get_success_message(self, cleaned_data):
    print(cleaned_data)
    return cleaned_data.get('name')+'を更新しました'
  
  def get_context_data(self, **kwargs):
        context = super(HouseUpdateView, self).get_context_data(**kwargs)
        context['slug'] = self.kwargs['pk']
        return context
  
  def post(self, request, *args, **kwargs):
    # picture_form = forms.PictureUploadForm(request.POST or None, request.FILES or None)
    # if picture_form.is_valid() and request.FILES:
    #   book = self.get_object()
    #   print(dir(self))
    #   picture_form.save(book=book)
    return super(HouseUpdateView, self).post(request, *args, **kwargs)
  
class HouseDeleteView(DeleteView):
  model = Housings
  template_name = 'house/house_delete.html'
  success_url = reverse_lazy('house:list_house')

class BookRedirectView(RedirectView):
  url = 'https://google.co.jp'
  
  def get_redirect_url(self, *args, **kwargs):
    book = Housings.objects.first()
    if 'pk' in kwargs:
      return reverse_lazy('store:detail_book', kwargs={'pk':kwargs['pk']})
    return reverse_lazy('store:edit_book', kwargs={'pk':book.pk})
  #Pkがあれば＝詳細画面に 引数なし＝編集画面に
  
def delete_picture(request, pk):
  picture = get_object_or_404(HousingPictures, pk=pk)
  picture.delete()
  import os
  if os.path.isfile(picture.picture.path):
    os.remove(picture.picture.path)
  messages.success(request, '画像を削除しました')
  return redirect('store:edit_book', pk=picture.book.id)