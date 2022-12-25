import  factory 
import pytest
from  faker import Faker 
from pytest_factoryboy import register   
from news.models import *

fake = Faker()

class NewsCategoryFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = NewsCategory

    name = factory.Sequence(lambda n: "cat_slug_%d" % n)
    slug = fake.lexify(text="cat_slug_??????")    

register(NewsCategoryFactory)

# pytest -m "not selenium" -rp

