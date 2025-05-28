import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from telegram_bot.handlers.manage_start import handle_start


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "user_id, username, is_new_user, i18n_responses, expected_welcome",
    [
        (111, "tester", True, ["Welcome Message", "Help Message"], "Welcome Message"),
        (222, "existing", False, ["Welcome Back Message", "Help Message"], "Welcome Back Message"),
    ]
)
async def test_handle_start(user_id, username, is_new_user, i18n_responses, expected_welcome):
    language_code = "en"

    message = MagicMock()
    message.from_user.id = user_id
    message.from_user.username = username
    message.from_user.first_name = username
    message.from_user.language_code = language_code
    message.answer = AsyncMock()

    with patch("telegram_bot.handlers.manage_start.SessionLocal") as mock_session_local, \
         patch("telegram_bot.handlers.manage_start.User") as MockUser, \
         patch("telegram_bot.handlers.manage_start.set_user_lang", new=AsyncMock()), \
         patch("telegram_bot.handlers.manage_start.clear_user_lang", new=AsyncMock()), \
         patch("telegram_bot.handlers.manage_start.initialize_user_categories", new=AsyncMock()), \
         patch("telegram_bot.handlers.manage_start.i18n.get", new=AsyncMock(side_effect=i18n_responses)):

        mock_session = MagicMock()
        if is_new_user:
            mock_session.query().filter_by().first.return_value = None
        else:
            mock_session.query().filter_by().first.return_value = MagicMock()
        mock_session_local.return_value = mock_session

        await handle_start(message)

        message.answer.assert_any_await(expected_welcome)
        message.answer.assert_awaited_with(i18n_responses[1])
