
from django.db.models import Count
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from drf_spectacular.utils import extend_schema
from elasticsearch_dsl import Q  # noqa
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from news.models import *

from .serializers import *


class PostNewsViewSet(viewsets.ModelViewSet):
    http_method_names = ["get"]

    serializer_class = PostNewsSerializer
    lookup_field = "slug"
    lookup_value_regex = "[^/]+"

    def get_queryset(self):
        return PostNews.postnewsobjects.select_related("category").prefetch_related(
            "tag"
        )

    @extend_schema(
        tags=["recent posts"],
        request=PostNewsSerializer,
        responses={200: PostNewsSerializer},
        methods=["POST"],
        description="View recent posts",
        operation_id="recent_posts",
    )
    @action(detail=True)
    def recentlyviewposts(self, request, slug):

        recently_view_news_sorting = None
        if "recently_view" in request.session:
            if slug in request.session["recently_view"]:
                request.session["recently_view"].remove(slug)

            posts = PostNews.postnewsobjects.filter(
                slug__in=request.session["recently_view"]
            )
            recently_view_news_sorting = sorted(
                posts, key=lambda x: request.session["recently_view"].index(x.slug)
            )
            request.session["recently_view"].insert(0, slug)
            serializer = DetailPostNewsSerializer(recently_view_news_sorting)

            if len(request.session["recently_view"]) > 5:
                request.session["recently_view"].pop()

        else:
            request.session["recently_view"] = [slug]
        request.session.modified = True

        serializer = DetailPostNewsSerializer(recently_view_news_sorting, many=True)
        return Response(serializer.data)

    @method_decorator(cache_page(60*2))
    def dispatch(self, request, *args, **kwargs):
       return super().dispatch(request, *args, **kwargs)


class PostWithSimilarTagsViewSet(viewsets.ModelViewSet):
    http_method_names = ["get"]

    serializer_class = TagSerializer
    lookup_field = "slug"
    lookup_value_regex = "[^/]+"

    def get_queryset(self):
        news_tag = Tag.objects.prefetch_related("postnews_set")
        similar_posts_by_tag = PostNews.postnewsobjects.filter(tag__in=news_tag)
        return similar_posts_by_tag.annotate(same_tag=Count("tag"))[:5]


# class PostsNewsSearchViewSet(viewsets.ModelViewSet):
#     serializer_class = PostNewsDocumentSerializer
#     search_document = PostNewsDocument
#     queryset = PostNews.objects.all()
#     pagination_class = [pagination.LimitOffsetPagination]

#     def get_object(self, request=None, query=None):
#         try:
#             q = Q("multi_match", query=query, fields=["title"])

#             search = self.search_document.search().query(q)
#             response = search.execute()

#             results = self.paginate_queryset(response, request, view=self)

#             serializer = self.serializer(results, many=True)

#             # return self.get_paginated_response(serializer.data)
#             return Response(serializer.data)
#         except Exception as e:
#             return Response(e, status=500)
