import pytest
from unittest.mock import AsyncMock, patch

from telegram_bot.ai_cat_detection.classifier import CategoryClassifier, get_category


def test_category_classifier_classify():
    examples = {
        "food": ["market", "eggs", "apples"],
        "travel": ["trip", "vacation", "flight"]
    }
    classifier = CategoryClassifier(examples)

    assert classifier.classify("I bought apples") == "food"
    assert classifier.classify("New flight") == "travel"


@pytest.mark.asyncio
@patch("telegram_bot.ai_cat_detection.classifier.get_user_category_samples", new_callable=AsyncMock)
async def test_get_category(mock_get_samples):
    user_id = 123
    desc = "Vacation organizing"

    mock_get_samples.return_value = {
        "food": ["market", "eggs", "apples"],
        "travel": ["trip", "vacation", "flight"]
    }

    category = await get_category(user_id, desc)
    assert category == "travel"
