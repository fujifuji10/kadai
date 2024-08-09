from django.shortcuts import render, redirect, get_object_or_404
from . import forms
from django.contrib import messages
from .models import Themes, Comments
from django.http import Http404

# Create your views here.
def create_theme(request):
  create_theme_form = forms.CreateThemeForm(request.POST or None)
  if create_theme_form.is_valid():
    create_theme_form.instance.user=request.user #現在ログインしているユーザーを取得できて、そのユーザーが作成したという意味になる
    create_theme_form.save() #themeにuserが外部キーで入っているため、誰がタイトルを作成したかを記載する必要がある↑①行上
    messages.success(request, '掲示板を作成しました')
    return redirect('boards:list_themes')
  return render(
    request, 'boards/create_theme.html', context={
      'create_theme_form':create_theme_form,
    }
  )
  
def list_themes(request):
  themes = Themes.objects.fetch_all_themes()
  return render(
    request, 'boards/list_themes.html', context={
      'themes':themes
    }
  )
  
def edit_theme(request, id):
  theme = get_object_or_404(Themes, id=id) #themeをidからget_object_or_404から取得します
  if theme.user.id != request.user.id: #ログイン者のuser.idと編集希望者のリクエストのuser.idが違っていればエラーを発生させる
    raise Http404
  edit_theme_form = forms.CreateThemeForm(request.POST or None, instance=theme)
  if edit_theme_form.is_valid():
    edit_theme_form.save()
    messages.success(request, '掲示板を更新しました')
    return redirect('boards:list_themes')
  return render( #上のリダイレクトする場合以外は以下を渡してね（返す）
    request, 'boards/edit_theme.html', context={
      'edit_theme_form':edit_theme_form,
      'id':id,
    }
  )
  
def delete_theme(request, id):
  theme = get_object_or_404(Themes, id=id)
  if theme.user.id != request.user.id:
    raise Http404
  delete_theme_form = forms.DeleteThemeForm(request.POST or None)
  if delete_theme_form.is_valid(): #csrf_tokenのチェック！
    theme.delete()
    messages.success(request, '掲示板を削除しました')
    return redirect('boards:list_themes')
  return render(
    request, 'boards/delete_theme.html', context={
      'delete_theme_form':
        delete_theme_form
    }
  )
  
def post_comments(request, theme_id):
  post_comment_form = forms.PostCommentForm(request.POST or None) #requestを送信した結果をコメントモデルに挿入するためのform
  theme = get_object_or_404(Themes, id=theme_id)
  comments = Comments.objects.fetch_by_theme_id(theme_id) #テーマに対してのコメントを全て取得
  if post_comment_form.is_valid():
    post_comment_form.instance.theme = theme #作成されたテーマが対象
    post_comment_form.instance.user = request.user #ログインしているログインユーザーが対象
    post_comment_form.save() #ここまでだとどのテーマに対するコメント？誰がコメント？かわからないので要素を入れる
    return redirect('boards:post_comments', theme_id=theme_id)
  return render(
    request, 'boards/post_comments.html', context={
      'post_comment_form':post_comment_form,
      'theme':theme,
      'comments':comments,
    }
  )
  