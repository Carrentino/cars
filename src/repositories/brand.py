from helpers.sqlalchemy.base_repo import ISqlAlchemyRepository

from src.db.models.brand import Brand


class BrandRepository(ISqlAlchemyRepository[Brand]):
    _model = Brand
