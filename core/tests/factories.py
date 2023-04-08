import factory
from faker import Faker
from pytest_factoryboy import register

from accounts.models import User
from news.models import *

fake = Faker()


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    email = factory.Sequence(lambda n: "_@_%d" % n)
    username = fake.lexify(text="username__????????")


class NewsCategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = NewsCategory

    name = factory.Sequence(lambda n: "cat_slug_%d" % n)
    slug = fake.lexify(text="cat_slug_??????")


register(NewsCategoryFactory)


class PostNewsFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = PostNews

    title = factory.Sequence(lambda n: "%d" % n)
    slug = fake.lexify(text="slug__????????")
    content = fake.text()
    status = factory.Sequence(lambda n: "%d" % n)
    category = factory.SubFactory(NewsCategoryFactory)
    user = factory.SubFactory(UserFactory)


register(PostNewsFactory)


class PostNewsMediaFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = PostNewsMedia

    postnews = factory.SubFactory(PostNewsFactory)    
    images = "images/9japointers.png"
    file = "bulk/video.mp4"
    alt_text = "9japointers resources"
    is_feature = True

register(PostNewsMediaFactory)
