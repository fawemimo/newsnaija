import datetime
import requests
import asyncio
import json
from django.http import HttpResponse
from datetime import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import DeleteView
import aiohttp
from .models import *


def articles_list(request, tag_slug=None):
    posts = PostNews.postnewsobjects.all()
    posts_cat = NewsCategory.objects.all()
    tag = None

    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        posts = PostNews.postnewsobjects.filter(tag__in=[tag])

    context = {"posts": posts, "posts_cat": posts_cat,'tag':tag}
    return render(request, "news/articles.html", context)


def articles_detail(request, slug):
    post = PostNews.postnewsobjects.filter(slug=slug) 

    # recently view post
    recently_view_news_sorting = None
    if 'recently_view' in request.session:
        if slug in request.session['recently_view'] :
            request.session['recently_view'].remove(slug)

        posts = PostNews.postnewsobjects.filter(slug__in=request.session['recently_view'])
        recently_view_news_sorting = sorted(posts, key=lambda x: request.session['recently_view'].index(x.slug))
        request.session['recently_view'].insert(0, slug)

        if len(request.session['recently_view']) > 5:
            request.session['recently_view'].pop()
    else:
        request.session['recently_view'] = [slug]
    request.session.modified = True  

    # similar posts for 7days past
    next_day = datetime.today() - timezone.timedelta(days=7)
    today = datetime.today()
    similar_posts = PostNews.postnewsobjects.filter(slug=slug).select_related('category').filter(date_created__range=(next_day,today))
# .exclude(id=post.id)[:5]
    # similar posts with tags
    news_tag = Tag.objects.prefetch_related('postnews_set')
    similar_posts_by_tag = PostNews.postnewsobjects.filter(tag__in=news_tag)
    # .exclude(id=post.id)
    similar_posts_by_tag = similar_posts_by_tag.annotate(same_tag=Count('tag'))[:5]
    context = {
        'post':post,
        'recently_view_news_sorting':recently_view_news_sorting,
        'similar_posts':similar_posts,
        'similar_posts_by_tag': similar_posts_by_tag
    }


    return render(request,'news/postnews_detail.html', context)


class NewsPostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """
    News Post Delete for each post

    """

    model = PostNews
    success_url = reverse_lazy("newspostlist")

    def test_func(self):
        post = self.get_object()
        if self.request.user.id == post.user.id:
            return True

        return False


async def load_quotes(request):
    # async with aiohttp.ClientSession() as session:
    #     async with session.get('https://www.goodreads.com/quotes/tag/life') as res:
    #         data = await res.json()
    #         print(data)
    r = requests.get('https://www.goodreads.com/quotes/tag/life')
    print(r.json())
    # post = PostNews()
    # post.save()
    return render(request,  "news/in.html")