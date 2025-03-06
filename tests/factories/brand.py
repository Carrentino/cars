import factory

from src.db.models.brand import Brand
from tests.factories.base import BaseSqlAlchemyFactory


class BrandFactory(BaseSqlAlchemyFactory):
    class Meta:
        model = Brand

    title = factory.Faker("word")
