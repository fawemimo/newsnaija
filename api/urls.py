from django.urls import include, path
from drf_spectacular.views import (SpectacularAPIView, SpectacularRedocView,
                                   SpectacularSwaggerView)
from rest_framework_nested import routers

from . import views

router = routers.DefaultRouter()
router.register('postnews',views.PostNewsViewSet, basename='postnews')
router.register('postnewswithsimilartags', views.PostWithSimilarTagsViewSet, basename='postnewswithsimilartags')
# router.register('postnewsearch', views.PostsNewsSearchViewSet, basename='postnewsearch')


urlpatterns = [
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('schema/frontend/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('schema/docs/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    path('', include(router.urls)),

]