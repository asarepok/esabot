from apps.materials.models import Material
from apps.users.models import User
from apps.school.models import School, Faculty, Programme, Level, Course
from core.enums import MaterialType


async def make_course():
    school = await School.create(name="Test University")
    faculty = await Faculty.create(school=school, name="Engineering")
    programme = await Programme.create(faculty=faculty, name="CS", level_count=4)
    level = await Level.create(programme=programme, number=1)
    return await Course.create(programme=programme, level=level, name="Intro", code="CS101", semester=1)


async def make_user(telegram_id=100000):
    return await User.create(telegram_id=telegram_id)


def required_fields(course, uploaded_by=None):
    return dict(
        course=course,
        uploaded_by=uploaded_by,
        telegram_file_id="file_abc123",
        telegram_chat_id=10000,
        telegram_message_id=200,
        file_name="lecture_notes.pdf",
    )


class TestMaterialCreation:
    async def test_material_creation_succeeds(self):
        course = await make_course()
        user = await make_user()

        material = await Material.create(**required_fields(course, user))

        assert material.id is not None
        assert material.course_id == course.id
        assert material.uploaded_by_id == user.id

    async def test_material_belongs_to_course(self):
        course = await make_course()

        material = await Material.create(**required_fields(course))

        fetched = await Material.get(id=material.id)
        assert fetched.course_id == course.id

    async def test_material_belongs_to_uploader(self):
        course = await make_course()
        user = await make_user(200000)

        material = await Material.create(**required_fields(course, user))

        fetched = await Material.get(id=material.id)
        assert fetched.uploaded_by_id == user.id

    async def test_material_type_persists_correctly(self):
        course = await make_course()

        material = await Material.create(**required_fields(course), material_type=MaterialType.PAST_QUESTIONS)

        fetched = await Material.get(id=material.id)
        assert fetched.material_type == MaterialType.PAST_QUESTIONS

    async def test_nullable_fields_accept_none(self):
        course = await make_course()

        material = await Material.create(**required_fields(course))

        assert material.material_type is None
        assert material.academic_year is None
        assert material.semester is None
        assert material.mime_type is None
        assert material.file_size is None
        assert material.uploaded_by_id is None

    async def test_nullable_fields_store_values_when_provided(self):
        course = await make_course()
        user = await make_user(300000)
        kwargs = required_fields(course, user)
        kwargs.update(
            material_type=MaterialType.SLIDES,
            academic_year=2024,
            semester=1,
            mime_type="application/pdf",
            file_size=204800,
        )

        material = await Material.create(**kwargs)
        fetched = await Material.get(id=material.id)

        assert fetched.material_type == MaterialType.SLIDES
        assert fetched.academic_year == 2024
        assert fetched.semester == 1
        assert fetched.mime_type == "application/pdf"
        assert fetched.file_size == 204800


class TestMaterialCascade:
    async def test_course_deletion_cascades_to_materials(self):
        course = await make_course()
        await Material.create(**required_fields(course))

        course_id = course.id
        await course.delete()

        assert await Material.filter(course_id=course_id).count() == 0

    async def test_user_deletion_sets_uploaded_by_null(self):
        course = await make_course()
        user = await make_user(400000)
        material = await Material.create(**required_fields(course, user))

        await user.delete()

        await material.refresh_from_db()
        assert material.uploaded_by_id is None
