"""HuaJingAM URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from account import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.login),
    url(r'^login/', views.login),
    url(r'^logout/', views.logout),
    url(r'^home/', views.home),                                        # 主页界面
    url(r'^credit_rating/(.*)/$', views.credit_rating),                      # 进行信用评级
    #url(r'^credit_rating_history/(.*)/$', views.user_rating_history),  # 某一用户的所有评级历史
    url(r'^credit_rating_history/(.*)/(.*)/(.*)/$', views.user_rating_history),  # 某一用户的所有评级历史
    url(r'^credit_rating_result/(.*)/(.*)/(.*)/$', views.rating_result),         # 债券评级结果
    url(r'^credit_rating_detail/(\d+)/$', views.rating_detail),        # 某一条结果的详细记录
    url(r'^delete_result/(\d+)/$', views.delete_result),          # 删除某一条result（管理员操作）
    url(r'^download_file/(\d+)/$', views.download_file),                # 下载文件
]
