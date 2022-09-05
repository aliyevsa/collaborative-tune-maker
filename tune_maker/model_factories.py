import factory
from random import randint
from .models import *

class UserFactory(factory.django.DjangoModelFactory):
    username = factory.Faker('user_name')
    password = factory.Faker('password')

    class Meta:
        model = User

class ProjectFactory(factory.django.DjangoModelFactory):
    name = factory.Faker('sentence', nb_words=3)
    length = randint(1, 100)
    owner = factory.SubFactory(UserFactory)
    collaborator = factory.SubFactory(UserFactory)

    class Meta:
        model = Project
