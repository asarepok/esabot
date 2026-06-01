from tortoise import fields
from tortoise.models import Model
from core.enums import Role


class User(Model):
    id = fields.IntField(pk=True)
    telegram_id = fields.BigIntField(unique=True)

    programme = fields.ForeignKeyField("models.Programme", related_name="users", on_delete=fields.SET_NULL)
    level = fields.ForeignKeyField("models.Level", related_name="users", on_delete=fields.SET_NULL)

    onboarded = fields.BooleanField(default=False)
    role = fields.CharEnumField(Role, default=Role.STUDENT)

    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    def __str__(self):
        return str(self.telegram_id)

    class Meta:
        indexes = (("programme_id", "level_id"))