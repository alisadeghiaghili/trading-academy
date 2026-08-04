import { useEffect, useState } from "react";
import { useParams, Link } from "react-router-dom";
import { useTranslation } from "react-i18next";
import {
  BookOpen,
  ChevronLeft,
  CheckCircle,
  Clock,
  Award,
} from "lucide-react";
import { useAppStore } from "@/store";
import { api } from "@/services/api";
import { LoadingSpinner, ErrorMessage } from "@/components/common";
import { cn } from "@/utils";

export function LessonPage() {
  const { t } = useTranslation();
  const { lessonId } = useParams();
  const { user } = useAppStore();
  const [lesson, setLesson] = useState<any>(null);
  const [content, setContent] = useState<any>(null);
  const [progress, setProgress] = useState<any>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [isCompleting, setIsCompleting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const loadLesson = async () => {
      setIsLoading(true);
      try {
        const lessonData = await api.getLesson(lessonId!);
        setLesson(lessonData);
        setProgress(lessonData.progress);

        const contentData = await api.getLessonContent(lessonId!);
        setContent(contentData);

        // Auto-start lesson
        if (!lessonData.progress || lessonData.progress?.status === "not_started") {
          await api.startLesson(lessonId!);
        }
      } catch (err: any) {
        setError(err.message);
      } finally {
        setIsLoading(false);
      }
    };
    loadLesson();
  }, [lessonId]);

  const handleComplete = async () => {
    setIsCompleting(true);
    try {
      const result = await api.completeLesson(lessonId!);
      setProgress(result);
    } catch (err: any) {
      setError(err.message);
    } finally {
      setIsCompleting(false);
    }
  };

  if (isLoading) return <LoadingSpinner size="lg" label={t("app.loading")} />;
  if (error) return <ErrorMessage message={error} onRetry={() => window.location.reload()} />;
  if (!lesson) return <ErrorMessage message={t("app.not_found")} />;

  return (
    <div className="space-y-6">
      {/* Back button */}
      <Link
        to={`/modules/${lesson.moduleId}`}
        className="inline-flex items-center gap-2 text-surface-600 dark:text-surface-400 hover:text-surface-900 dark:hover:text-surface-50 transition-colors"
      >
        <ChevronLeft className="h-5 w-5 rtl:rotate-180" />
        <span>{t("lessons.previous")}</span>
      </Link>

      {/* Lesson Header */}
      <div className="card p-6">
        <div className="flex items-center justify-between">
          <div>
            <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-primary-100 dark:bg-primary-900/30 text-primary-700 dark:text-primary-300 text-sm font-medium mb-3 capitalize">
              {lesson.lessonType}
            </div>
            <h1 className="text-2xl font-bold text-surface-900 dark:text-surface-50 mb-2">{lesson.title}</h1>
            <p className="text-surface-600 dark:text-surface-400">{lesson.description}</p>
          </div>
          <div className="flex items-center gap-4 text-surface-500 dark:text-surface-400">
            <div className="flex items-center gap-1">
              <Clock className="h-4 w-4" />
              <span className="text-sm">{lesson.estimatedMinutes} {t("modules.minutes")}</span>
            </div>
          </div>
        </div>

        {/* Progress bar */}
        {progress && (
          <div className="mt-4 pt-4 border-t border-surface-200 dark:border-surface-700">
            <div className="flex items-center justify-between text-sm text-surface-600 dark:text-surface-400 mb-2">
              <span>{t("lessons.progress")}</span>
              <span className="capitalize">{progress.status?.replace("_", " ")}</span>
            </div>
            <div className="w-full bg-surface-200 dark:bg-surface-700 rounded-full h-2">
              <div
                className={cn(
                  "rounded-full h-2 transition-all duration-500",
                  progress.status === "completed" ? "bg-green-600" : "bg-primary-600"
                )}
                style={{
                  width: progress.status === "completed" ? "100%" : progress.status === "in_progress" ? "50%" : "0%",
                }}
              />
            </div>
          </div>
        )}
      </div>

      {/* Lesson Content */}
      <div className="card p-6">
        <div className="lesson-content space-y-6">
          {content?.html ? (
            <div dangerouslySetInnerHTML={{ __html: content.html }} />
          ) : (
            <div className="prose max-w-none dark:text-surface-300">
              {content?.questions ? (
                <QuizSection lessonId={lessonId!} questions={content.questions} onComplete={handleComplete} />
              ) : (
                <div className="text-center py-12">
                  <BookOpen className="h-16 w-16 text-primary-600 mx-auto mb-4" />
                  <h2 className="text-xl font-semibold text-surface-900 dark:text-surface-50 mb-2">{lesson.title}</h2>
                  <p className="text-surface-500 dark:text-surface-400">{t("app.coming_soon")}</p>
                </div>
              )}
            </div>
          )}
        </div>
      </div>

      {/* Complete Button */}
      <div className="flex justify-end gap-4">
        {progress?.status !== "completed" && (
          <button
            onClick={handleComplete}
            disabled={isCompleting}
            className="btn-primary btn-lg"
          >
            {isCompleting ? (
              <span className="spinner spinner-sm" />
            ) : (
              <>
                <CheckCircle className="h-5 w-5" />
                {t("lessons.complete")}
              </>
            )}
          </button>
        )}
      </div>
    </div>
  );
}

// Inline Quiz Component
function QuizSection({ lessonId, questions, onComplete }: { lessonId: string; questions: any[]; onComplete: () => void }) {
  const { t } = useTranslation();
  const [currentIndex, setCurrentIndex] = useState(0);
  const [answers, setAnswers] = useState<Record<string, any>>({});
  const [submitted, setSubmitted] = useState(false);
  const [score, setScore] = useState(0);
  const [isSubmitting, setIsSubmitting] = useState(false);

  const currentQuestion = questions[currentIndex];

  const handleAnswer = (questionId: string, answer: any) => {
    setAnswers((prev) => ({ ...prev, [questionId]: answer }));
  };

  const handleSubmitAll = async () => {
    setIsSubmitting(true);
    let correct = 0;
    for (const q of questions) {
      const userAnswer = answers[q.id];
      if (userAnswer) {
        try {
          const result = await api.submitQuizAttempt({
            questionId: q.id,
            userAnswer: { option_id: userAnswer },
            timeSpentSeconds: 5,
          });
          if (result.isCorrect) correct++;
        } catch (err) {}
      }
    }
    setScore(correct);
    setSubmitted(true);
    setIsSubmitting(false);
  };

  if (submitted) {
    return (
      <div className="text-center py-8">
        <Award className={cn("h-16 w-16 mx-auto mb-4", score >= questions.length * 0.7 ? "text-green-600" : "text-yellow-600")} />
        <h2 className="text-2xl font-bold text-surface-900 dark:text-surface-50 mb-2">{t("lessons.score")}: {score}/{questions.length}</h2>
        <p className="text-surface-600 dark:text-surface-400 mb-6">
          {score >= questions.length * 0.7 ? t("lessons.pass") : t("lessons.fail")}
        </p>
        <div className="flex justify-center gap-4">
          <button onClick={() => { setCurrentIndex(0); setSubmitted(false); setScore(0); setAnswers({}); }} className="btn-secondary">
            {t("lessons.retake")}
          </button>
          <button onClick={onComplete} className="btn-primary">{t("lessons.complete")}</button>
        </div>
      </div>
    );
  }

  return (
    <div>
      <div className="flex items-center justify-between mb-6">
        <h2 className="text-lg font-semibold text-surface-900 dark:text-surface-50">{t("lessons.quiz")}</h2>
        <span className="text-sm text-surface-500">{currentIndex + 1}/{questions.length}</span>
      </div>

      {currentQuestion && (
        <div className="space-y-6">
          <div key={currentQuestion.id} className="card-hover p-4 border-2 border-surface-200 dark:border-surface-700">
            <p className="font-medium text-surface-900 dark:text-surface-50 mb-4">
              {currentQuestion.questionText?.en || currentQuestion.questionText}
            </p>
            <div className="space-y-3">
              {currentQuestion.options?.map((option: any) => {
                const optionText = option.text?.en || option.text;
                return (
                  <label
                    key={option.optionId}
                    className={cn(
                      "flex items-center gap-3 p-3 rounded-lg border cursor-pointer transition-colors",
                      answers[currentQuestion.id] === option.optionId
                        ? "border-primary-500 bg-primary-50 dark:bg-primary-900/20"
                        : "border-surface-200 dark:border-surface-700 hover:border-surface-300"
                    )}
                  >
                    <input
                      type="radio"
                      name={currentQuestion.id}
                      value={option.optionId}
                      checked={answers[currentQuestion.id] === option.optionId}
                      onChange={() => handleAnswer(currentQuestion.id, option.optionId)}
                      className="accent-primary-600"
                    />
                    <span className="text-surface-700 dark:text-surface-300">{optionText}</span>
                  </label>
                );
              })}
            </div>
          </div>

          <div className="flex justify-between">
            <button
              onClick={() => setCurrentIndex((i) => Math.max(0, i - 1))}
              disabled={currentIndex === 0}
              className="btn-secondary btn-sm"
            >
              {t("lessons.previous")}
            </button>

            {currentIndex < questions.length - 1 ? (
              <button
                onClick={() => setCurrentIndex((i) => i + 1)}
                className="btn-primary btn-sm"
              >
                {t("lessons.next")}
              </button>
            ) : (
              <button
                onClick={handleSubmitAll}
                disabled={isSubmitting}
                className="btn-primary"
              >
                {isSubmitting ? <span className="spinner spinner-sm" /> : t("lessons.submit")}
              </button>
            )}
          </div>
        </div>
      )}
    </div>
  );
}