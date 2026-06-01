from apps.requests.models import MaterialRequest
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


class TestMaterialRequestCreation:
    async def test_request_creation_succeeds(self):
        user = await make_user()
        course = await make_course()

        request = await MaterialRequest.create(user=user, course=course, material_type=MaterialType.SLIDES)

        assert request.id is not None

    async def test_request_belongs_to_user(self):
        user = await make_user()
        course = await make_course()

        request = await MaterialRequest.create(user=user, course=course, material_type=MaterialType.BOOK)

        fetched = await MaterialRequest.get(id=request.id)
        assert fetched.user_id == user.id

    async def test_request_belongs_to_course(self):
        user = await make_user()
        course = await make_course()

        request = await MaterialRequest.create(user=user, course=course, material_type=MaterialType.COURSE_OUTLINE)

        fetched = await MaterialRequest.get(id=request.id)
        assert fetched.course_id == course.id

    async def test_material_type_stored_correctly(self):
        user = await make_user()
        course = await make_course()

        request = await MaterialRequest.create(user=user, course=course, material_type=MaterialType.PAST_QUESTIONS)

        fetched = await MaterialRequest.get(id=request.id)
        assert fetched.material_type == MaterialType.PAST_QUESTIONS

    async def test_semester_is_null_by_default(self):
        user = await make_user()
        course = await make_course()

        request = await MaterialRequest.create(user=user, course=course, material_type=MaterialType.SLIDES)

        assert request.semester is None

    async def test_semester_stores_value_when_provided(self):
        user = await make_user()
        course = await make_course()

        request = await MaterialRequest.create(
            user=user, course=course, material_type=MaterialType.SLIDES, semester=2
        )

        fetched = await MaterialRequest.get(id=request.id)
        assert fetched.semester == 2


class TestMaterialRequestCascade:
    async def test_user_deletion_cascades_to_requests(self):
        user = await make_user(300000)
        course = await make_course()
        await MaterialRequest.create(user=user, course=course, material_type=MaterialType.SLIDES)

        user_id = user.id
        await user.delete()

        assert await MaterialRequest.filter(user_id=user_id).count() == 0

    async def test_course_deletion_cascades_to_requests(self):
        user = await make_user(400000)
        course = await make_course()
        await MaterialRequest.create(user=user, course=course, material_type=MaterialType.BOOK)

        course_id = course.id
        await course.delete()

        assert await MaterialRequest.filter(course_id=course_id).count() == 0
