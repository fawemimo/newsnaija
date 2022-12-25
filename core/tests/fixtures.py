import  pytest
from django.contrib.auth.models import User
from django.core.management import  call_command



@pytest.fixture
def create_admin_user(django_user_model):
    
    return django_user_model.objects.create_superuser('admin01','admin01@gmail.com','password123')


@pytest.fixture(scope='session')
def db_fixture_setup(django_db_setup,django_db_blocker):
    # lod DB data fixures

    with django_db_blocker.unblock():
        call_command("loaddata", "db_admin_fixtures.json")
        # call_command("loaddata", "db_category_fixture.json")


