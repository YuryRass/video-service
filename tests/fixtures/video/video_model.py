import factory
from factory.alchemy import SQLAlchemyModelFactory
from faker import Factory as FakerFactory
from pytest_factoryboy import register

from app.models import Video
from tests.database import test_scoped_session
from tests.fixtures.user.user_model import UserFactory

faker = FakerFactory.create()


@register(_name="video")
class VideoFactory(SQLAlchemyModelFactory):
    class Meta:
        model = Video
        sqlalchemy_session = test_scoped_session

    id = factory.LazyFunction(lambda: faker.random_int())
    title = factory.LazyFunction(lambda: faker.sentence())
    url = factory.LazyFunction(lambda: faker.url())
    user_id = factory.RelatedFactory(UserFactory)
