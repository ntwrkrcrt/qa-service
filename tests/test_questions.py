import pytest
from httpx import AsyncClient


@pytest.mark.api
class TestQuestions:
    """Test question endpoints."""

    @pytest.mark.asyncio
    async def test_create_question(self, async_client: AsyncClient):
        """Test creating a question."""
        response = await async_client.post(
            "/question/",
            params={"text": "What is Python?"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["text"] == "What is Python?"
        assert "id" in data
        assert "created_at" in data

    @pytest.mark.asyncio
    async def test_get_questions(self, async_client: AsyncClient):
        """Test getting all questions."""
        # Create a question first
        await async_client.post(
            "/question/",
            params={"text": "Test question"}
        )
        
        response = await async_client.get("/question/")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 1
        assert data[0]["text"] == "Test question"

    @pytest.mark.asyncio
    async def test_get_questions_with_limit(self, async_client: AsyncClient):
        """Test getting questions with limit."""
        # Create multiple questions
        for i in range(3):
            await async_client.post(
                "/question/",
                params={"text": f"Question {i}"}
            )
        
        response = await async_client.get("/question/?limit=2")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2

    @pytest.mark.asyncio
    async def test_get_question_with_answers(self, async_client: AsyncClient):
        """Test getting a specific question with answers."""
        # Create a question
        response = await async_client.post(
            "/question/",
            params={"text": "Test question"}
        )
        question_id = response.json()["id"]
        
        # Add an answer
        await async_client.post(
            f"/question{question_id}/answers/",
            params={
                "text": "Test answer",
                "user_id": "user123"
            }
        )
        
        # Get question with answers
        response = await async_client.get(f"/question/{question_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["text"] == "Test question"
        assert len(data["answers"]) == 1
        assert data["answers"][0]["text"] == "Test answer"

    @pytest.mark.asyncio
    async def test_get_nonexistent_question(self, async_client: AsyncClient):
        """Test getting a non-existent question."""
        response = await async_client.get("/question/999999")
        assert response.status_code == 404

    @pytest.mark.asyncio
    async def test_add_answer_to_question(self, async_client: AsyncClient):
        """Test adding an answer to a question."""
        # Create a question
        response = await async_client.post(
            "/question/",
            params={"text": "Test question"}
        )
        question_id = response.json()["id"]
        
        # Add an answer
        response = await async_client.post(
            f"/question{question_id}/answers/",
            params={
                "text": "Test answer",
                "user_id": "user123"
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert data["text"] == "Test answer"
        assert data["user_id"] == "user123"
        assert data["question_id"] == question_id

    @pytest.mark.asyncio
    async def test_add_answer_to_nonexistent_question(self, async_client: AsyncClient):
        """Test adding an answer to a non-existent question."""
        response = await async_client.post(
            "/question999999/answers/",
            params={
                "text": "Test answer",
                "user_id": "user123"
            }
        )
        assert response.status_code == 404

    @pytest.mark.asyncio
    async def test_delete_question(self, async_client: AsyncClient):
        """Test deleting a question."""
        # Create a question
        response = await async_client.post(
            "/question/",
            params={"text": "Question to delete"}
        )
        question_id = response.json()["id"]
        
        # Delete the question
        response = await async_client.delete(f"/question/{question_id}")
        assert response.status_code == 204
        
        # Verify it's gone
        response = await async_client.get(f"/question/{question_id}")
        assert response.status_code == 404