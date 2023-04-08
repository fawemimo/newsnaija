from rest_framework import serializers

from news.models import *


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ['id', 'name', 'slug']


class PostNewsSerializer(serializers.ModelSerializer):
    tag = TagSerializer(many=True, read_only=True)


    class Meta:
        model = PostNews
        fields = ['id', 'category', 'title', 'content', 'tag', 'source', 'status', 'date_created', 'slug', 'seo_title', 'seo_descriptions', 'date_updated']

        lookup_value = 'slug'


class DetailPostNewsSerializer(serializers.Serializer):
    title = serializers.CharField()
    slug = serializers.SlugField()


class PostWithSimilarTagsSerializer(serializers.ModelSerializer):
    post = serializers.SerializerMethodField()

    class Meta:
        model = Tag
        fields= ['id','name','slug','post']


class PostNewsDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostNews
        fields = ['id','title','status']