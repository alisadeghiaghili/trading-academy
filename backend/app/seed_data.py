"""Seed database with curriculum content from app.content package."""

from __future__ import annotations

import asyncio
import sys
from pathlib import Path
from uuid import uuid4

sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlalchemy import select

from app.db.session import get_db_context
from app.db.models import Module, Lesson, QuizQuestion
from app.content import CURRICULUM


async def seed_data() -> None:
    """Populate database with curriculum content."""
    print("Starting database seed...")

    async with get_db_context() as db:
        result = await db.execute(select(Module).limit(1))
        if result.scalar_one_or_none():
            print("Modules already exist. Skipping curriculum seed.")
            return

        for module_data in CURRICULUM:
            module_id = uuid4()
            module = Module(
                id=module_id,
                slug=module_data["slug"],
                title=module_data["title"],
                description=module_data["description"],
                order=module_data["order"],
                required_tier=module_data["required_tier"],
                is_published=True,
            )
            db.add(module)
            print(f"Created module: {module_data['title']}")

            for lesson_data in module_data["lessons"]:
                lesson_id = uuid4()
                lesson = Lesson(
                    id=lesson_id,
                    module_id=module_id,
                    slug=lesson_data["slug"],
                    title=lesson_data["title"],
                    description=lesson_data["description"],
                    lesson_type=lesson_data["lesson_type"],
                    content=lesson_data["content"],
                    order=lesson_data["order"],
                    estimated_minutes=lesson_data["estimated_minutes"],
                    required_tier="free",
                    is_published=True,
                )
                db.add(lesson)
                print(f"  Created lesson: {lesson_data['title']}")

                for quiz_data in lesson_data.get("quizzes", []):
                    quiz = QuizQuestion(
                        id=uuid4(),
                        lesson_id=lesson_id,
                        question_text=quiz_data["question_text"],
                        question_type=quiz_data["question_type"],
                        options=quiz_data["options"],
                        correct_answer=quiz_data["correct_answer"],
                        explanation=quiz_data["explanation"],
                        difficulty=quiz_data["difficulty"],
                        order=quiz_data["order"],
                    )
                    db.add(quiz)
                    print("    Added quiz question")

        await db.commit()
        total_lessons = sum(len(m["lessons"]) for m in CURRICULUM)
        total_quizzes = sum(
            len(lesson.get("quizzes", []))
            for module in CURRICULUM
            for lesson in module["lessons"]
        )
        print("\nDatabase seeded successfully!")
        print(f"   Modules: {len(CURRICULUM)}")
        print(f"   Lessons: {total_lessons}")
        print(f"   Quiz questions: {total_quizzes}")


if __name__ == "__main__":
    asyncio.run(seed_data())
