import pytest
from unittest.mock import patch
import main


# Mock the pipeline used in filter_comment
def mock_pipeline(comment: str):
    if "idiot" in comment.lower():
        return [{"label": "HATE", "score": 0.99}]
    return [{"label": "NOT_HATE", "score": 0.99}]


@pytest.mark.asyncio
async def test_filter_comment():
    with patch("main.pipe", side_effect=mock_pipeline):
        # Good comment
        response = await main.filter_comment("Hello")
        assert response is False

        # Hateful comment
        response = await main.filter_comment("You are an idiot")
        assert response is True
