import pytest
from tortoise.exceptions import IntegrityError

from apps.school.models import School, Faculty, Programme, Level, Course


async def make_school(name="Test University"):
    return await School.create(name=name)


async def make_faculty(school=None, name="Engineering"):
    if school is None:
        school = await make_school()
    return await Faculty.create(school=school, name=name)


async def make_programme(faculty=None, name="Computer Science", level_count=4):
    if faculty is None:
        faculty = await make_faculty()
    return await Programme.create(faculty=faculty, name=name, level_count=level_count)


async def make_level(programme=None, number=1):
    if programme is None:
        programme = await make_programme()
    return await Level.create(programme=programme, number=number)


async def make_course(programme=None, level=None, name="Intro to CS", code="CS101", semester=1):
    if programme is None:
        programme = await make_programme()
    if level is None:
        level = await Level.create(programme=programme, number=1)
    return await Course.create(programme=programme, level=level, name=name, code=code, semester=semester)


class TestAcademicHierarchy:
    async def test_school_can_have_multiple_faculties(self):
        school = await make_school()
        await Faculty.create(school=school, name="Engineering")
        await Faculty.create(school=school, name="Sciences")

        count = await Faculty.filter(school=school).count()
        assert count == 2

    async def test_faculty_belongs_to_school(self):
        school = await make_school()
        faculty = await Faculty.create(school=school, name="Engineering")

        fetched = await Faculty.get(id=faculty.id)
        assert fetched.school_id == school.id

    async def test_programme_belongs_to_faculty(self):
        faculty = await make_faculty()
        programme = await Programme.create(faculty=faculty, name="CS", level_count=4)

        fetched = await Programme.get(id=programme.id)
        assert fetched.faculty_id == faculty.id

    async def test_level_belongs_to_programme(self):
        programme = await make_programme()
        level = await Level.create(programme=programme, number=1)

        fetched = await Level.get(id=level.id)
        assert fetched.programme_id == programme.id

    async def test_course_belongs_to_programme_and_level(self):
        programme = await make_programme()
        level = await Level.create(programme=programme, number=1)
        course = await Course.create(
            programme=programme, level=level, name="Algorithms", code="CS201", semester=1
        )

        fetched = await Course.get(id=course.id)
        assert fetched.programme_id == programme.id
        assert fetched.level_id == level.id


class TestUniqueConstraints:
    async def test_faculty_name_unique_within_school(self):
        school = await make_school()
        await Faculty.create(school=school, name="Engineering")

        with pytest.raises(IntegrityError):
            await Faculty.create(school=school, name="Engineering")

    async def test_faculty_same_name_allowed_in_different_schools(self):
        school_a = await make_school("University A")
        school_b = await make_school("University B")
        await Faculty.create(school=school_a, name="Engineering")

        faculty_b = await Faculty.create(school=school_b, name="Engineering")

        assert faculty_b.id is not None

    async def test_programme_name_unique_within_faculty(self):
        faculty = await make_faculty()
        await Programme.create(faculty=faculty, name="CS", level_count=4)

        with pytest.raises(IntegrityError):
            await Programme.create(faculty=faculty, name="CS", level_count=3)

    async def test_programme_same_name_allowed_in_different_faculties(self):
        school = await make_school()
        eng = await Faculty.create(school=school, name="Engineering")
        sci = await Faculty.create(school=school, name="Sciences")
        await Programme.create(faculty=eng, name="CS", level_count=4)

        prog = await Programme.create(faculty=sci, name="CS", level_count=4)

        assert prog.id is not None

    async def test_level_number_unique_within_programme(self):
        programme = await make_programme()
        await Level.create(programme=programme, number=1)

        with pytest.raises(IntegrityError):
            await Level.create(programme=programme, number=1)

    async def test_level_same_number_allowed_in_different_programmes(self):
        faculty = await make_faculty()
        prog_a = await Programme.create(faculty=faculty, name="CS", level_count=4)
        prog_b = await Programme.create(faculty=faculty, name="EE", level_count=4)
        await Level.create(programme=prog_a, number=1)

        level_b = await Level.create(programme=prog_b, number=1)

        assert level_b.id is not None

    async def test_course_unique_together_on_programme_level_semester_code(self):
        programme = await make_programme()
        level = await Level.create(programme=programme, number=1)
        await Course.create(programme=programme, level=level, code="CS101", name="Intro", semester=1)

        with pytest.raises(IntegrityError):
            await Course.create(programme=programme, level=level, code="CS101", name="Different Name", semester=1)

    async def test_course_same_code_different_semester_is_allowed(self):
        programme = await make_programme()
        level = await Level.create(programme=programme, number=1)
        await Course.create(programme=programme, level=level, code="CS101", name="Intro", semester=1)

        course2 = await Course.create(programme=programme, level=level, code="CS101", name="Intro II", semester=2)

        assert course2.id is not None


class TestCascadeDeletion:
    async def test_delete_school_cascades_to_faculties(self):
        school = await make_school()
        await Faculty.create(school=school, name="Engineering")

        school_id = school.id
        await school.delete()

        assert await Faculty.filter(school_id=school_id).count() == 0

    async def test_delete_faculty_cascades_to_programmes(self):
        faculty = await make_faculty()
        await Programme.create(faculty=faculty, name="CS", level_count=4)

        faculty_id = faculty.id
        await faculty.delete()

        assert await Programme.filter(faculty_id=faculty_id).count() == 0

    async def test_delete_programme_cascades_to_levels(self):
        programme = await make_programme()
        await Level.create(programme=programme, number=1)
        await Level.create(programme=programme, number=2)

        programme_id = programme.id
        await programme.delete()

        assert await Level.filter(programme_id=programme_id).count() == 0

    async def test_delete_programme_cascades_to_courses(self):
        programme = await make_programme()
        level = await Level.create(programme=programme, number=1)
        await Course.create(programme=programme, level=level, name="Intro", code="CS101", semester=1)

        programme_id = programme.id
        await programme.delete()

        assert await Course.filter(programme_id=programme_id).count() == 0

    async def test_delete_level_cascades_to_courses(self):
        programme = await make_programme()
        level = await Level.create(programme=programme, number=1)
        await Course.create(programme=programme, level=level, name="Intro", code="CS101", semester=1)

        level_id = level.id
        await level.delete()

        assert await Course.filter(level_id=level_id).count() == 0
