import pytest
from news.models import *
from django.db import IntegrityError
from uuid import uuid4, UUID


@pytest.mark.dbfixture
@pytest.mark.parametrize(
    "id,name,slug,is_active",
    [
        ("30530813-740b-42f0-bcdd-6e6e230ea0f6", "SPORTS", "sports", 1),
        ("445ee699-a2d1-470a-a4ba-157f5a8a7cee", "POLITICS", "politics", 1),
        ("46f5aa3b-3cdf-405b-86cf-e1f5952651fc", "ENTERTAINMENT", "entertainment", 1),
    ],
)
def test_news_category_dbfixture(db, db_fixture_setup, id, name, slug, is_active):

    """
    UTILIZING THE  CATEGORY DATA FIXTURES

    """
    newscategory = NewsCategory.objects.get(id=id)
    assert newscategory.name == name
    assert newscategory.slug == slug
    assert newscategory.is_active == is_active


@pytest.mark.parametrize(
    "name,slug,is_active",
    [
        ("SPORTS", "sports", 1),
        ("POLITICS", "politics", 1),
        ("ENTERTAINMENT", "entertainment", 1),
    ],
)
def test_news_category_db_insert(db, news_category_factory, name, slug, is_active):

    news_category_factory = news_category_factory.create(name=name, slug=slug, is_active=is_active)
    assert news_category_factory.name == name
    assert news_category_factory.slug == slug
    assert news_category_factory.is_active == is_active


@pytest.mark.django_db
def test_news_category_uniqueness_integrity(news_category_factory):
    category = news_category_factory.create(id="e6e76a4a-3b30-43dd-81af-a5e725c576b8")

    with pytest.raises(IntegrityError):
        news_category_factory.create(id="e6e76a4a-3b30-43dd-81af-a5e725c576b8")


@pytest.mark.dbfixture
@pytest.mark.parametrize(
    "id,category,title,content,status,slug",
    [
        (
            UUID("090a4cf8-fab7-43bc-96e3-36b1fa731ca4"),
            UUID("46f5aa3b-3cdf-405b-86cf-e1f5952651fc"),
            "CARDI B",
            "<p>dcgnglntng</p>",
            "published",
            "cardi-b",
        )
    ],
)
def test_news_post_dbfixture(
    db,
    db_fixture_setup,
    id,
    category,
    title,
    content,
    status,
    slug,
):
    post_news = PostNews.objects.get(id=id)

    assert post_news.category.id == category
    assert post_news.title == title
    assert post_news.content == content
    assert post_news.status == status
    assert post_news.slug == slug


@pytest.mark.django_db
def test_news_db_post_news_uniqueness_integrity(post_news_factory):
    uuid = post_news_factory.create(id="e10d0516-55a0-445d-ab8b-17cf3b701bdb")

    with pytest.raises(IntegrityError):
        post_news_factory.create(id=uuid)


@pytest.mark.parametrize(
    "category,title,content,status,slug",
    [(uuid4, "CARDI B", "<p>dcgnglntng</p>", "published", "cardi-b")],
)
def test_post_news_db_insert(
    db,
    category,
    post_news_factory,
    title,
    content,
    status,
    slug,
):

    post_news_factory = post_news_factory.create(
        category__name="POLTICS", title=title, content=content, status=status, slug=slug
    )

    assert post_news_factory.category.name == "POLTICS"
    assert post_news_factory.title == title
    assert post_news_factory.content == content
    assert post_news_factory.status == status
    assert post_news_factory.slug == slug
