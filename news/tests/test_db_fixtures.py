import pytest
from news.models import *


@pytest.mark.dbfixture
@pytest.mark.parametrize(
    "id,name,slug,is_active", 
    [
        (1,"Politics Today","politics-today",True),
        (2,"Arise news","arise-news",True),
        (3,"Sunday Night News","sunday-night-news",True),
   
    ],
)
def test_news_category_dbfixture( db,db_fixture_setup,id,name,slug,is_active):
    
    newscategory = NewsCategory.objects.get(id=id)
    assert newscategory.name == name
    assert newscategory.slug == slug
    assert newscategory.is_active == is_active


@pytest.mark.parametrize(
    "name,slug,is_active", 
    [
        ("Politics Today","politics-today",1),
        ("Arise news","arise-news",1),
        ("Sunday Night News","sunday-night-news",1),
   
    ],
)
def test_news_category_db_insert(db,newscategory_factory,name,slug,is_active):

    newscat_factory = newscategory_factory.create(name=name,slug=slug,is_active=is_active)
    assert newscat_factory.name == name
    assert newscat_factory.slug == slug
    assert newscat_factory.is_active == is_active

    