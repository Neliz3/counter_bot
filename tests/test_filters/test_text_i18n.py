import pytest
import datetime
from unittest.mock import AsyncMock, patch
from aiogram.types import Message, User, Chat
from telegram_bot.filters.text_i18n import TextI18nFilter


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "message_text, i18n_text, expected_result",
    [
        ("Expected translation text", "Expected translation text", True),
        ("Wrong text", "Expected translation text", False),
    ]
)
@patch("telegram_bot.filters.text_i18n.i18n.get", new_callable=AsyncMock)
async def test_text_i18n_filter(mock_i18n_get, message_text, i18n_text, expected_result):
    user_id = 123
    key = "some.key"

    mock_i18n_get.return_value = i18n_text

    filter_instance = TextI18nFilter(key=key)

    message = Message(
        message_id=1,
        from_user=User(id=user_id, is_bot=False, first_name="Test"),
        chat=Chat(id=user_id, type="private"),
        date=datetime.datetime.now(),
        text=message_text
    )

    result = await filter_instance(message)
    assert result == expected_result
