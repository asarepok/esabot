from tortoise import fields
from tortoise.models import Model
from core.enums import MaterialType


class Material(Model):
    id = fields.IntField(primary_key=True)

    course = fields.ForeignKeyField("models.Course", related_name="materials", on_delete=fields.CASCADE)
    uploaded_by = fields.ForeignKeyField("models.User", related_name="uploaded_materials", on_delete=fields.SET_NULL, null=True)
    material_type = fields.CharEnumField(MaterialType, null=True)

    academic_year = fields.IntField(max_length=20, null=True)
    semester = fields.IntField(null=True)

    telegram_file_id = fields.CharField(max_length=255)
    telegram_chat_id = fields.BigIntField()
    telegram_message_id = fields.BigIntField()

    file_name = fields.CharField(max_length=255)
    mime_type = fields.CharField(max_length=100, null=True)
    file_size = fields.BigIntField(null=True)

    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    class Meta:
        indexes = (
            ("course_id", "material_type"),
            ("course_id", "academic_year"),
            ("course_id", "semester")
        )

    def __str__(self):
        return self.file_name