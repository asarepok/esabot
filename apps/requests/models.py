from tortoise import fields
from tortoise.models import Model
from core.enums import MaterialType


class MaterialRequest(Model):
    id = fields.IntField(primary_key=True)
    user = fields.ForeignKeyField("models.User", related_name="material_requests", on_delete=fields.CASCADE)

    course = fields.ForeignKeyField("models.Course",related_name="material_requests",on_delete=fields.CASCADE)
    material_type = fields.CharEnumField(MaterialType)
    semester = fields.IntField(null=True)

    created_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        indexes = (
            ("course_id", "material_type"),
            ("course_id", "semester")
        )