import datetime
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, TemplateView, UpdateView, View
from .models import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages


class NewsPostList(ListView):
    """
    News Post List of the total news page

    """

    model = PostNews
    template_name = "news/newspost.html"
    context_object_name = "posts"
    paginate_by = 5

    # getting the category model along with the postnews
    # def get_context_data(self, *, object_list=None, **kwargs):
    #     posts = PostNews.objects.all()
    # cat = NewsCategory.objects.values("name")

    # context = {"posts": posts,
    # #  "cat": cat
    #  }

    # return context


def post_news_by_category(request, slug):

    """
    Listing the categories based on News Post

    """
    newscategory = PostNews.objects.filter(category__slug=slug).values(
        "id", "title", "content", "category__name", "date_created", "status", "source", "user__first_name"
    )

    context = {"newscategory": newscategory}

    return render(request, "news/post_news_by_category.html", context)


def newspostdetailview(request,slug, id):

    """
    Individual Post News Details

    object: the params rendering in the template

    @id : object variable

    @slug : url object variable
    """

    object = PostNews.objects.get(slug=slug,id=id)

    context = {"object": object}

    return render(request, "news/postnews_detail.html", context)


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
