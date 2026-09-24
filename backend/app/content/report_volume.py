"""Report curriculum content volume per module."""

from __future__ import annotations

import re

from app.content import CURRICULUM


def main() -> None:
    total_words = 0
    total_quizzes = 0
    for module in CURRICULUM:
        words = 0
        quizzes = 0
        for lesson in module["lessons"]:
            html = lesson["content"]["html"]
            words += len(re.sub(r"<[^>]+>", " ", html).split())
            quizzes += len(lesson.get("quizzes", []))
        total_words += words
        total_quizzes += quizzes
        print(
            f"{module['slug']}: lessons={len(module['lessons'])} "
            f"words={words} quizzes={quizzes}"
        )
    print(f"TOTAL: modules={len(CURRICULUM)} words={total_words} quizzes={total_quizzes}")


if __name__ == "__main__":
    main()
