import factory
from factory.alchemy import SQLAlchemyModelFactory
from faker import Factory as FakerFactory
from pytest_factoryboy import register

from app.models import User
from tests.database import test_scoped_session

faker = FakerFactory.create()


@register(_name="user")
class UserFactory(SQLAlchemyModelFactory):
    class Meta:
        model = User
        sqlalchemy_session = test_scoped_session

    id = factory.LazyFunction(lambda: faker.random_int())
    email = factory.LazyFunction(lambda: faker.email())
    password = factory.LazyFunction(
        lambda: faker.password(
            length=12,
            special_chars=True,
            digits=True,
            upper_case=True,
            lower_case=True,
        )
    )
