from tortoise import fields
from tortoise.models import Model



class School(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=255)
    created_at = fields.DatetimeField(auto_now_add=True)

    def __str__(self):
        return self.name



class Faculty(Model):
    id = fields.IntField(pk=True)
    school = fields.ForeignKeyField("models.School",related_name="faculties",on_delete=fields.CASCADE)
    name = fields.CharField(max_length=255)
    created_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        unique_together = (("school", "name"))

    def __str__(self):
        return self.name



class Programme(Model):
    id = fields.IntField(pk=True)
    faculty = fields.ForeignKeyField("models.Faculty", related_name="programmes", on_delete=fields.CASCADE)
    name = fields.CharField(max_length=255)
    level_count = fields.IntField()
    level_label = fields.CharField(max_length=50, default="Level")
    created_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        unique_together = (("faculty", "name"))

    def __str__(self):
        return self.name



class Level(Model):
    id = fields.IntField(pk=True)
    programme = fields.ForeignKeyField("models.Programme", related_name="levels", on_delete=fields.CASCADE)
    number = fields.IntField()
    created_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        unique_together = (("programme", "number"))

    def __str__(self):
        return f"{self.programme.level_label} {self.number * 100}"



class Course(Model):
    id = fields.IntField(pk=True)
    programme = fields.ForeignKeyField("models.Programme", related_name="courses", on_delete=fields.CASCADE)
    level = fields.ForeignKeyField("models.Level", related_name="courses", on_delete=fields.CASCADE)
    code = fields.CharField(max_length=50, null=True)
    name = fields.CharField(max_length=255)
    semester = fields.IntField()
    created_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        unique_together = (("programme", "level", "semester", "code"))

    def __str__(self):
        return f"{self.name}"