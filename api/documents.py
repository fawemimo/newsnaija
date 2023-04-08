from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry

from news.models import *


@registry.register_document
class PostNewsDocument(Document):

    class Index:
        name = 'postnews'

    class Django:
        model = PostNews
        fields = ['id','title','status']   