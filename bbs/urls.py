from django.urls import path
from bbs.views import home_view,home_ajax  # bbs\views.pyからhome_view関数をインポート

urlpatterns = [
    path('', home_view, name='bbs_home'),  # ルートにhome_viewを指定
    path('ajax', home_ajax, name='bbs_ajax'),  # ルートにhome_viewを指定

]