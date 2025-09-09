from typing import List, Optional

from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from models.database import Answer, Question
from models.qa import Answer as AnswerModel
from models.qa import Question as QuestionModel
from models.qa import QuestionWithAnswers


class Storage:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_question(self, text: str) -> QuestionModel:
        stmt = insert(Question).values(text=text).returning(Question)
        result = await self.session.execute(stmt)
        question_row = result.fetchone()
        question = question_row[0]

        return QuestionModel(
            id=question.id, text=question.text, created_at=question.created_at
        )

    async def get_questions(self, limit: Optional[int]) -> List[QuestionModel]:
        stmt = select(Question)
        if limit:
            stmt = stmt.limit(limit)
        result = await self.session.execute(stmt)
        questions = result.scalars().all()
        return [
            QuestionModel(id=q.id, text=q.text, created_at=q.created_at)
            for q in questions
        ]

    async def get_question_answers(
        self, question_id: int
    ) -> Optional[QuestionWithAnswers]:
        stmt = (
            select(Question)
            .where(Question.id == question_id)
            .options(selectinload(Question.answers))
        )
        result = await self.session.execute(stmt)
        question = result.scalar_one_or_none()

        if not question:
            return None

        return QuestionWithAnswers(
            id=question.id,
            text=question.text,
            created_at=question.created_at,
            answers=[
                AnswerModel(
                    id=ans.id,
                    question_id=ans.question_id,
                    user_id=ans.user_id,
                    text=ans.text,
                    created_at=ans.created_at,
                )
                for ans in question.answers
            ],
        )

    async def delete_question(self, question_id: int) -> None:
        stmt = select(Question).where(Question.id == question_id)
        result = await self.session.execute(stmt)
        question = result.scalar_one_or_none()

        if question:
            await self.session.delete(question)
            await self.session.commit()

    async def add_answer(
        self, question_id: int, text: str, user_id: str
    ) -> Optional[AnswerModel]:
        check_stmt = select(Question).where(Question.id == question_id)
        check_result = await self.session.execute(check_stmt)
        if not check_result.scalar_one_or_none():
            return None

        stmt = (
            insert(Answer)
            .values(question_id=question_id, text=text, user_id=user_id)
            .returning(Answer)
        )
        result = await self.session.execute(stmt)
        answer_row = result.fetchone()
        answer = answer_row[0]

        return AnswerModel(
            id=answer.id,
            question_id=answer.question_id,
            user_id=answer.user_id,
            text=answer.text,
            created_at=answer.created_at,
        )

    async def get_answer_by_id(self, answer_id: int) -> Optional[Answer]:
        stmt = select(Answer).where(Answer.id == answer_id)
        result = await self.session.execute(stmt)
        answer = result.scalar_one_or_none()
        if not answer:
            return None

        return answer

    async def delete_answer(self, answer_id: int) -> None:
        stmt = select(Answer).where(Answer.id == answer_id)
        result = await self.session.execute(stmt)
        answer = result.scalar_one_or_none()

        if answer:
            await self.session.delete(answer)
            await self.session.commit()
