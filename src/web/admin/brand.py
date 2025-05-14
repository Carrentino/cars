from sqladmin import ModelView

from src.db.models.brand import Brand


class BrandAdmin(ModelView, model=Brand):
    column_list = [Brand.id, Brand.title]  # noqa: RUF012
