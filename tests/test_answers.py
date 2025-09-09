import pytest
from httpx import AsyncClient


@pytest.mark.api
class TestAnswers:
    """Test answer endpoints."""

    @pytest.mark.asyncio
    async def test_get_answer(self, async_client: AsyncClient):
        """Test getting a specific answer."""
        # Create question
        question_response = await async_client.post(
            "/question/",
            params={"text": "Test question"}
        )
        question_id = question_response.json()["id"]
        
        # Add an answer
        answer_response = await async_client.post(
            f"/question{question_id}/answers/",
            params={
                "text": "Test answer",
                "user_id": "user123"
            }
        )
        answer_id = answer_response.json()["id"]
        
        # Get the answer
        response = await async_client.get(f"/answers/{answer_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["text"] == "Test answer"
        assert data["user_id"] == "user123"
        assert data["question_id"] == question_id

    @pytest.mark.asyncio
    async def test_get_nonexistent_answer(self, async_client: AsyncClient):
        """Test getting a non-existent answer."""
        response = await async_client.get("/answers/999999")
        assert response.status_code == 404

    @pytest.mark.asyncio
    async def test_delete_answer(self, async_client: AsyncClient):
        """Test deleting an answer."""
        # Create question
        question_response = await async_client.post(
            "/question/",
            params={"text": "Test question"}
        )
        question_id = question_response.json()["id"]
        
        # Add an answer
        answer_response = await async_client.post(
            f"/question{question_id}/answers/",
            params={
                "text": "Answer to delete",
                "user_id": "user123"
            }
        )
        answer_id = answer_response.json()["id"]
        
        # Delete the answer
        response = await async_client.delete(f"/answers/{answer_id}")
        assert response.status_code == 204
        
        # Verify
        response = await async_client.get(f"/answers/{answer_id}")
        assert response.status_code == 404