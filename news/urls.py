from django.urls import path
from . import views


urlpatterns = [
    path('', views.NewsPostList.as_view(), name='newspostlist'),
    path('<slug:slug>/', views.post_news_by_category, name='newspostlistcategorybase'),
    path('<slug:slug>/<uuid:id>/', views.newspostdetailview, name='newspostdetail'),
    path('<slug:slug>/<uuid:id>/delete', views.NewsPostDeleteView.as_view(), name='newspostdelete'),
]