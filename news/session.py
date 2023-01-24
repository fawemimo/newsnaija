"""
class NewsPostList(ListView): 
    model = PostNews
    template_name = "news/newspost.html"
    context_object_name = "posts"
    paginate_by = 5

    # getting the category model along with the postnews
    def get_context_data(self, **kwargs):
        context = super(NewsPostList, self).get_context_data(**kwargs)
        # context['']
        return context


def newspostlist(request):

    posts = PostNews.objects.all()

    # tag = None

    # if tag_slug:
    #     tag = get_object_or_404(Tag, name=tag_slug)
    #     posts = PostNews.objects.filter(tag__in=[tag])

    context = {"posts": posts}


    return render(request, "news/newspost.html",context)
    





def newspostdetailview(request, slug):

    objec = PostNews.objects.get(slug=slug)
    news_tags_ids = PostNews.objects.values_list("slug", flat=True)
    similar_news = (
        PostNews.objects.filter(tag__in=news_tags_ids)
        .exclude(slug=object.slug)
        .annotate(same_tags=Count("tag"))
    ).order_by("?")[:2]

    
    recently_view_news_sorting = None
    if 'recently_view'in request.session:
        if slug in request.session['recently_view'] :
            request.session['recently_view'].remove(slug)

        recently_view_news= PostNews.objects.filter(pk__in=request.session['recently_view'])
        recently_view_news_sorting = sorted(recently_view_news.values(), key=lambda x: request.session['recently_view'].index(x.id))
        request.session['recently_view'].insert(0, slug)

        if len(request.session['recently_view']) > 5:
            request.session['recently_view'].pop()
    else:
        request.session['recently_view'] = [slug]

    request.session.modified = True    

    context = {"objec": objec}

    return render(request, "news/postnew_detail.html", context)





def post_news_by_category(request, slug):

   
    newscategory = PostNews.objects.filter(category__slug=slug).values(
        "id",
        "title",
        "content",
        "category__name",
        "date_created",
        "status",
        "source",
        "user__first_name",
    )

    context = {"newscategory": newscategory}

    return render(request, "news/post_news_by_category.html", context)
"""