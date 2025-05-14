from sqladmin import ModelView

from src.db.models.car_attachment import CarAttachment


class CarAttachmentAdmin(ModelView, model=CarAttachment):
    column_list = [CarAttachment.id, CarAttachment.car]  # noqa: RUF012
