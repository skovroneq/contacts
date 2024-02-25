import unittest
from unittest.mock import MagicMock

from sqlalchemy.orm import Session

from src.database.models import User
from src.schemas import UserModel
from src.repository.users import (
    get_user_by_email,
    create_user,
    update_token,
    confirmed_email,
    update_avatar
)


class TestUsers(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.session = MagicMock(spec=Session)

    async def test_get_user_by_email_found(self):
        user = User
        self.session.query().filter().first.return_value = user
        result = await get_user_by_email(email=user.email, db=self.session)
        self.assertEqual(result, user)

    async def test_get_user_by_email_not_found(self):
        email = "example@example.com"
        self.session.query().filter().first.return_value = None
        result = await get_user_by_email(email=email, db=self.session)

        self.assertIsNone(result)

    async def test_create_user(self):
        body = UserModel(username="test_user", email="test@example.com", password="password", avatar=None,
                         confirmed=False)
        result = await create_user(body=body, db=self.session)
        self.assertEqual(result.username, body.username)
        self.assertEqual(result.email, body.email)
        self.assertEqual(result.password, body.password)
        self.assertIsNone(result.avatar)
        self.assertFalse(result.confirmed)
        self.assertTrue(hasattr(result, "id"))

    async def test_update_token(self):
        user = User(email="test@example.com")
        self.session.commit.return_value = None
        await update_token(user, "token", self.session)
        self.assertEqual(user.refresh_token, "token")

    async def test_confirmed_email(self):
        user = User(email="test@example.com")
        self.session.query().filter().first.return_value = user
        self.session.commit.return_value = None
        await confirmed_email("test@example.com", self.session)
        self.assertTrue(user.confirmed)

    async def test_update_avatar(self):
        user = User(email="test@example.com")
        self.session.query().filter().first.return_value = user
        self.session.commit.return_value = None
        result = await update_avatar("test@example.com", "url", self.session)
        self.assertEqual(result, user)
        self.assertEqual(user.avatar, "url")
