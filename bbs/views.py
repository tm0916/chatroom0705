from bbs.forms import PostForm
from django.shortcuts import render,redirect
from bbs.models import Post  # modelsからPostモデルをインポート
from django.http import HttpResponse
import json
from django.core import serializers
from django.http import JsonResponse

#一番最初にアクセスする関数 /bbs
def home_view(request):

    # print(request)
    # print(request.method)

    # request.methodによって処理を分岐
    if request.method == 'GET':
        return home_view_get(request)
    elif request.method == 'POST':
        if "submit" in request.POST:#投稿 submitはbuttonに付けたname
            return home_view_post(request)
        elif "delete_all" in request.POST:#全削除　delete_allはbuttonに付けたname
            return home_view_delete_all(request)
    else:
        return HttpResponse('invalid method', status=400)

#参考サイト
#Djangoでフォーム内でクリックされたボタンによって異なる処理を行う
#https://yura2.hateblo.jp/entry/2015/04/04/Django%E3%81%A7%E3%83%95%E3%82%A9%E3%83%BC%E3%83%A0%E5%86%85%E3%81%A7%E3%82%AF%E3%83%AA%E3%83%83%E3%82%AF%E3%81%95%E3%82%8C%E3%81%9F%E3%83%9C%E3%82%BF%E3%83%B3%E3%81%AB%E3%82%88%E3%81%A3%E3%81%A6%E7%95%B0

#################################################################################
#関数-表示の関数
def home_view_get(request,form=None):#formはデフォルト
    context = {} # コンテキストを作成
    context['title'] = "WOW CHATROOM"
    context['form'] = PostForm() #forms.pyから PostFormのオブジェクトを保存

    if form:#formにデータが入っている場合
        context['form'] = form #データが不正な場合
    else:
        context['form'] = PostForm()  # フォームを保存⇒HTMLにフォームの入力部分が表示される

    return render(request, 'bbs/home.html', context)
#################################################################################
#関数-データベースにデータを追加
def home_view_post(request):
    form = PostForm(request.POST)#ユーザーが投稿した内容が入っている
    # print(form) 
    if not form.is_valid():#フォームのデータが不正であれば～
        return home_view_get(request, form=form) #データが不正なのでhome_view_getに返す

    form.save()#データが生の場合　投稿したデータを保存する

    return redirect('bbs_home')#urls.pyで付けた名前
#################################################################################
#関数　データ全削除 20210703
def home_view_delete_all(request):
    Post.objects.all().delete()#全て削除

    return redirect('bbs_home')

#################################################################################
#関数-データベースにあるデータを全て取得して Ajax用　Ajaxでの別の処理はこの関数にアクセスしてくる
def home_ajax(request):

    # print(Post.objects.all())#データベースにあるすべてのデータを表示
    # <QuerySet [<Post: Post object (1)>, <Post: Post object (2)>, <Post: Post object (3)>, <Post: Post object (4)>, <Post: Post object (8)>, <Post: Post object (9)>]>

    #Django オブジェクトを他の形式に「翻 訳」
    #第1引数はフォーマット、第2引数はQueryset　jsonに変換
    list = serializers.serialize("json", Post.objects.all())

    print(list)
    #参考例 [{"model": "bbs.post", "pk": 1, "fields": {"content": "test1"}}, {"model": "bbs.post", "pk": 2, "fields": {"content": "test2"}}, {"model": "bbs.post", "pk": 3, "fields": {"content": "test3"}}, {"model": "bbs.post", "pk": 4, "fields": {"content": "test4"}}, {"model": "bbs.post", "pk": 8, "fields": {"content": "テスト"}}, {"model": "bbs.post", "pk": 9, "fields": {"content": "aa"}}]

    #json化したデータをリスポンスする
    return JsonResponse(list,safe=False)


