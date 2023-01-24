from django.urls import path
from . import views


urlpatterns = [
    path('', views.articles_list, name='articles_list'),
    # path('<slug:slug>/', views.post_news_by_category, name='newspostlistcategorybase'),
    path('<slug:slug>/', views.articles_detail, name='newspostdetail'),
    # path('<slug:slug>/<uuid:id>/delete', views.NewsPostDeleteView.as_view(), name='newspostdelete'),
    path('tag/<slug:tag_slug>/',views.articles_list,name='postnewstag')
]