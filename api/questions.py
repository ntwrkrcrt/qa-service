from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession

from database.connection import get_db
from database.storage import Storage
from models.qa import Answer, Question, QuestionWithAnswers

router = APIRouter(prefix="/question", tags=["question"])


def get_storage(db: AsyncSession = Depends(get_db)) -> Storage:
    return Storage(db)


@router.post("/", response_model=Question)
async def create_question(text: str, storage: Storage = Depends(get_storage)):
    try:
        created_question = await storage.create_question(text)
    except Exception as e:
        logger.error(f"Failed to create question: {e}")
        raise HTTPException(status_code=500, detail="Failed to create question")

    return created_question


@router.get("/", response_model=list[Question])
async def get_questions(
    limit: Optional[int] = None, storage: Storage = Depends(get_storage)
):
    try:
        all_questions = await storage.get_questions(limit=limit)
    except Exception as e:
        logger.error(f"Failed to create question: {e}")
        raise HTTPException(status_code=500, detail="Failed to get questions")

    return all_questions


@router.get("/{id}", response_model=QuestionWithAnswers)
async def get_question_answers(id: int, storage: Storage = Depends(get_storage)):
    try:
        question_answers = await storage.get_question_answers(id)
    except Exception as e:
        logger.error(f"Failed to get question answers: {e}")
        raise HTTPException(status_code=500, detail="Failed to get question answers")

    if not question_answers:
        raise HTTPException(status_code=404, detail="Question not found")

    return question_answers


@router.delete("/{id}", status_code=204)
async def delete_question(id: int, storage: Storage = Depends(get_storage)):
    try:
        await storage.delete_question(id)
    except Exception as e:
        logger.error(f"Failed to delete question: {e}")
        raise HTTPException(status_code=500, detail="Failed to delete question")


@router.post("{id}/answers/", response_model=Answer)
async def add_answer(
    id: int,
    text: str,
    user_id: str,
    storage: Storage = Depends(get_storage),
):
    try:
        answer = await storage.add_answer(question_id=id, text=text, user_id=user_id)
    except Exception as e:
        logger.error(f"Failed to add answer: {e}")
        raise HTTPException(status_code=500, detail="Failed to add answer")

    if not answer:
        raise HTTPException(status_code=404, detail="Question not found")

    return answer
