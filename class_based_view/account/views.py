from django.shortcuts import render, redirect, get_object_or_404
from . import forms
from django.core.exceptions import ValidationError
from .models import UserActivateTokens
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import update_session_auth_hash
from datetime import datetime
from django.views.generic.base import (
    View, TemplateView, RedirectView,
)
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import (
  CreateView, UpdateView, DeleteView,FormView,
)
from .forms import RegistForm, LoginForm, CommentAddForm
from django.urls import reverse_lazy
from .models import Users, Comments
from django.contrib.messages.views import SuccessMessageMixin

# Create your views here.
class HomeView(TemplateView):
  template_name = 'account/home.html'

class WelcomeView(TemplateView):
  template_name = 'account/welcome.html'
  
class RegistUserView(CreateView):
  template_name = 'account/regist.html'
  form_class = RegistForm
  success_url = reverse_lazy("account:user_login")
  
class UserLoginView(FormView):
  template_name = 'account/user_login.html'
  form_class = LoginForm
  
  def post(self, request, *args, **kwargs):
    email = request.POST['email']
    password = request.POST['password']
    user = authenticate(email=email, password=password)
    next_url = request.POST['next']
    if user is not None and user.is_active:
      login(request, user)
    if next_url:
      return redirect(next_url)
    return redirect('account:home')
  
class UserLogoutView(View):
  
  def get(self, request, *args, **kwargs):
    logout(request)
    return redirect('account:user_login')
  
class UserUpdateView(SuccessMessageMixin, UpdateView):
  template_name = 'account/user_update.html'
  model = Users
  form_class = forms.UserUpdateForm
  success_message = '更新に成功しました'
  
  def get_success_url(self):
    return reverse_lazy('account:home', kwargs={'id': self.object.id})
  
  def get_success_message(self, cleaned_data):
    return cleaned_data.get('name')+'を更新しました'
  
  def get_context_data(self, **kwargs):
        context = super(UserUpdateView, self).get_context_data(**kwargs)
        context['id'] = self.kwargs['pk']
        return context
  
class UserCommentListView(ListView):
  model = Comments #一覧表示するモデル
  template_name = 'account/list_comment.html'
  
class CommentAddView(LoginRequiredMixin, CreateView):
  model = Comments
  template_name = 'account/add_comment.html'
  form_class = CommentAddForm
  success_url = reverse_lazy('account:list_comment')
  
  def form_valid(self, form):
    form.instance.create_at = datetime.now()
    form.instance.update_at = datetime.now()
    object = form.save(commit=False)
    object.user = self.request.user
    object.save()
    return super(CommentAddView, self).form_valid(form)

#  #htmlテンプレートに渡すデータを定義
#   def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['post'] = get_object_or_404(Comments, pk=self.kwargs['pk'])
#         return context
  
def activate_user(request, token): #pathを設定したactivate_userを定義しよう
#tokenを元にuser_activate_tokensをアクティベートする
  user_activate_token = UserActivateTokens.objects.activate_user_by_token(token)
  return render(
    request, 'accounts/activate_user.html'
  )
  
def user_login(request): #まずログイン用のformを記載
  login_form = forms.LoginForm(request.POST or None)
  if login_form.is_valid():
    email = login_form.cleaned_data.get('email')
    password = login_form.cleaned_data.get('password')
    #ログイン時の2つの入力データが正しいかどうかを確認する↓
    user = authenticate(email=email, password=password)
    if user:
      if user.is_active:
        login(request, user)
        messages.success(request, 'ログイン完了しました')#ログイン成功時のメッセージ
        return redirect('accounts:home')
      else:
        messages.warning(request, 'ユーザーがアクティブではありません') #ログインに成功したがアクティブユーザーでない場合
    else:
      messages.warning(request, 'ユーザーかパスワードが間違っています') #ログイン失敗した場合
  return render(
    request, 'accounts/user_login.html', context={
      'login_form':login_form
    }
  )
  
@login_required
def change_password(request):
  password_change_form = forms.PasswordChangeForm(request.POST or None, instance=request.user)
  if password_change_form.is_valid():
    try:
      password_change_form.save()
      messages.success(request, 'パスワードの更新完了しました')
      #下でセッションも更新する必要があるのでインポート＋記載
      update_session_auth_hash(request, request.user) #第二引数＝ユーザー情報（認証されたユーザー情報を対象にしている）
    except ValidationError as e:
      password_change_form.add_error('password', e)
  return render(
    request, 'accounts/change_password.html', context={
      'password_change_form':password_change_form
    }
  )