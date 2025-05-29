import pytest
import datetime
from unittest.mock import AsyncMock, patch, MagicMock
from aiogram.types import Message, User, Chat, ReplyKeyboardRemove
from telegram_bot.handlers import add_income


@pytest.mark.asyncio
@patch("aiogram.types.message.Message.answer", new_callable=AsyncMock)
@patch("telegram_bot.handlers.add_income.set_state", new_callable=AsyncMock)
@patch("telegram_bot.handlers.add_income.i18n.get", new_callable=AsyncMock)
async def test_start_income(mock_i18n_get, mock_set_state, mock_answer):
    user_id = 123
    expected_text = "Please enter income"

    mock_i18n_get.return_value = expected_text

    message = Message(
        message_id=1,
        from_user=User(id=user_id, is_bot=False, first_name="Test"),
        chat=Chat(id=user_id, type="private"),
        date=datetime.datetime.now(),
        text="irrelevant"
    )

    result = await add_income.start_income(message, user_id)

    mock_set_state.assert_awaited_with(user_id, "awaiting_income")
    assert mock_answer.await_args[0][0] == expected_text
    assert result is not None


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "text,expected_income,expected_reply,expected_set_state",
    [
        ("100.5", 100.5, "Please confirm income", "confirm_income"),
        ("200", 200.0, "Please confirm income", "confirm_income"),
    ]
)
@patch("aiogram.types.message.Message.answer", new_callable=AsyncMock)
@patch("telegram_bot.handlers.add_income.set_state", new_callable=AsyncMock)
@patch("telegram_bot.handlers.add_income.set_temp_income", new_callable=AsyncMock)
@patch("telegram_bot.handlers.add_income.i18n.get", new_callable=AsyncMock)
@patch("telegram_bot.handlers.add_income.confirm_keyboard", new_callable=AsyncMock)
async def test_handle_income_value_valid(
    mock_confirm_keyboard, mock_i18n_get, mock_set_temp_income, mock_set_state, mock_answer,
    text, expected_income, expected_reply, expected_set_state
):
    user_id = 123

    mock_i18n_get.return_value = expected_reply
    mock_confirm_keyboard.return_value = "keyboard"

    message = Message(
        message_id=1,
        from_user=User(id=user_id, is_bot=False, first_name="Test"),
        chat=Chat(id=user_id, type="private"),
        date=datetime.datetime.now(),
        text=text
    )

    result = await add_income.handle_income_value(message, user_id)

    mock_set_temp_income.assert_awaited_with(user_id, expected_income)
    mock_set_state.assert_awaited_with(user_id, expected_set_state)
    mock_answer.assert_awaited_with(expected_reply, reply_markup="keyboard")
    assert result is not None


@pytest.mark.asyncio
@pytest.mark.parametrize("invalid_text", ["abc", "one hundred", ""])
@patch("aiogram.types.message.Message.answer", new_callable=AsyncMock)
@patch("telegram_bot.handlers.add_income.i18n.get", new_callable=AsyncMock)
async def test_handle_income_value_invalid(mock_i18n_get, mock_answer, invalid_text):
    user_id = 123
    error_text = "Invalid value"

    mock_i18n_get.return_value = error_text

    message = Message(
        message_id=1,
        from_user=User(id=user_id, is_bot=False, first_name="Test"),
        chat=Chat(id=user_id, type="private"),
        date=datetime.datetime.now(),
        text=invalid_text
    )

    result = await add_income.handle_income_value(message, user_id)

    mock_answer.assert_awaited_with(error_text)
    assert result is not None


@pytest.mark.asyncio
@patch("aiogram.types.message.Message.answer", new_callable=AsyncMock)
@patch("telegram_bot.handlers.add_income.get_temp_income", new_callable=AsyncMock)
@patch("telegram_bot.handlers.add_income.clear_state", new_callable=AsyncMock)
@patch("telegram_bot.handlers.add_income.i18n.get", new_callable=AsyncMock)
@patch("telegram_bot.handlers.add_income.SessionLocal")
async def test_handle_income_confirmation_yes(
    mock_session_local, mock_i18n_get, mock_clear_state, mock_get_temp_income, mock_answer
):
    user_id = 123
    yes_text = "Yes"
    success_text = "Income added"

    mock_i18n_get.side_effect = [yes_text, yes_text, success_text]
    mock_get_temp_income.return_value = 100.0

    mock_session = MagicMock()
    mock_session_local.return_value = mock_session

    class MockStats:
        income = None

        def recalculate_total(self):
            pass

    MockStats.get_or_create = MagicMock(return_value=MockStats())

    message = Message(
        message_id=1,
        from_user=User(id=user_id, is_bot=False, first_name="Test"),
        chat=Chat(id=user_id, type="private"),
        date=datetime.datetime.now(),
        text=yes_text
    )

    with patch("telegram_bot.handlers.add_income.DailyStats", MockStats):
        result = await add_income.handle_income_confirmation(message, user_id)

    mock_clear_state.assert_awaited()
    mock_answer.assert_awaited_with(success_text, reply_markup=ReplyKeyboardRemove())
    assert result is not None


@pytest.mark.asyncio
@patch("aiogram.types.message.Message.answer", new_callable=AsyncMock)
@patch("telegram_bot.handlers.add_income.clear_state", new_callable=AsyncMock)
@patch("telegram_bot.handlers.add_income.i18n.get", new_callable=AsyncMock)
async def test_handle_income_confirmation_no(mock_i18n_get, mock_clear_state, mock_answer):
    user_id = 123
    no_text = "No"
    cancel_text = "Cancelled"

    def i18n_get_side_effect(*args, **kwargs):
        key = kwargs.get("key")
        if key == "messages.confirm.no":
            return no_text
        elif key == "messages.cancel":
            return cancel_text
        return "unknown"

    mock_i18n_get.side_effect = i18n_get_side_effect

    message = Message(
        message_id=1,
        from_user=User(id=user_id, is_bot=False, first_name="Test"),
        chat=Chat(id=user_id, type="private"),
        date=datetime.datetime.now(),
        text=no_text
    )

    result = await add_income.handle_income_confirmation(message, user_id)

    mock_clear_state.assert_awaited()
    mock_answer.assert_awaited_with(cancel_text, reply_markup=ReplyKeyboardRemove())
    assert result is not None


@pytest.mark.asyncio
@patch("aiogram.types.message.Message.answer", new_callable=AsyncMock)
@patch("telegram_bot.handlers.add_income.i18n.get", new_callable=AsyncMock)
async def test_handle_income_confirmation_other_text(mock_i18n_get, mock_answer):
    user_id = 123
    unknown_text = "Maybe"
    error_text = "Unknown response"

    mock_i18n_get.return_value = error_text

    message = Message(
        message_id=1,
        from_user=User(id=user_id, is_bot=False, first_name="Test"),
        chat=Chat(id=user_id, type="private"),
        date=datetime.datetime.now(),
        text=unknown_text
    )

    result = await add_income.handle_income_confirmation(message, user_id)

    mock_answer.assert_awaited_with(error_text)
    assert result is not None
