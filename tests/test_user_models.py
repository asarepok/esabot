import pytest
from tortoise.exceptions import IntegrityError

from apps.users.models import User
from apps.school.models import School, Faculty, Programme, Level
from core.enums import Role


async def make_hierarchy():
    school = await School.create(name="Test University")
    faculty = await Faculty.create(school=school, name="Engineering")
    programme = await Programme.create(faculty=faculty, name="CS", level_count=4)
    level = await Level.create(programme=programme, number=1)
    return programme, level


class TestUserCreation:
    async def test_user_creation_with_defaults(self):
        user = await User.create(telegram_id=123456789)

        assert user.id is not None
        assert user.telegram_id == 123456789
        assert user.onboarded is False
        assert user.role == Role.STUDENT

    async def test_user_programme_and_level_are_nullable_by_default(self):
        user = await User.create(telegram_id=111111111)

        assert user.programme_id is None
        assert user.level_id is None

    async def test_user_belongs_to_programme(self):
        programme, level = await make_hierarchy()
        user = await User.create(telegram_id=222222222, programme=programme, level=level)

        fetched = await User.get(id=user.id)
        assert fetched.programme_id == programme.id

    async def test_user_belongs_to_level(self):
        programme, level = await make_hierarchy()
        user = await User.create(telegram_id=333333333, programme=programme, level=level)

        fetched = await User.get(id=user.id)
        assert fetched.level_id == level.id

    async def test_telegram_id_uniqueness_enforced(self):
        await User.create(telegram_id=999888777)

        with pytest.raises(IntegrityError):
            await User.create(telegram_id=999888777)


class TestUserForeignKeyCascade:
    async def test_programme_deletion_sets_user_programme_null(self):
        programme, level = await make_hierarchy()
        user = await User.create(telegram_id=444444444, programme=programme, level=level)

        await programme.delete()

        await user.refresh_from_db()
        assert user.programme_id is None

    async def test_level_deletion_sets_user_level_null(self):
        programme, level = await make_hierarchy()
        user = await User.create(telegram_id=555555555, programme=programme, level=level)

        await level.delete()

        await user.refresh_from_db()
        assert user.level_id is None
