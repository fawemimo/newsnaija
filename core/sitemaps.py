from django.contrib.sitemaps import Sitemap

from news.models import *


class AllNewsSite(Sitemap):
    def items(self):       
        return PostNews.postnewsobjects.all()

    def lastmod(self, obj) :
        return obj.date_updated   

       