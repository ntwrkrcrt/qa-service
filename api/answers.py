from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession

from database.connection import get_db
from database.storage import Storage
from models.qa import Answer

router = APIRouter(prefix="/answers", tags=["answers"])


def get_storage(db: AsyncSession = Depends(get_db)) -> Storage:
    return Storage(db)


@router.get("/{id}", response_model=Answer)
async def get_exact_answer(
    id: int, storage: Storage = Depends(get_storage)
) -> Optional[Answer]:
    try:
        answer: Optional[Answer] = await storage.get_answer_by_id(id)
    except Exception as e:
        logger.error(f"Failed to get answer: {e}")
        raise HTTPException(status_code=500, detail="Failed to get answer")

    if not answer:
        raise HTTPException(status_code=404, detail="Answer not found")

    return answer


@router.delete("/{id}", status_code=204)
async def delete_answer(id: int, storage: Storage = Depends(get_storage)) -> None:
    try:
        await storage.delete_answer(id)
    except Exception as e:
        logger.error(f"Failed to delete answer: {e}")
        raise HTTPException(status_code=500, detail="Failed to delete answer")
