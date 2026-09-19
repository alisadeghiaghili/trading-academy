"""Seed gamification data - badges, challenges, tutorials, pattern games."""

import asyncio
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path
from uuid import uuid4

sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlalchemy import select
from app.db.session import get_db_context
from app.db.gamification_models import (
    Badge,
    DailyChallenge,
    Tutorial,
    PatternGame,
    EconomicEvent,
    NewsItem,
    ChallengeType,
    AchievementCategory,
    BadgeTier,
)


BADGES = [
    # Learning badges
    {"code": "first_lesson", "name": {"en": "First Steps", "fa": "قدم اول", "de": "Erste Schritte"}, "description": {"en": "Complete your first lesson", "fa": "اولین درس خود را کامل کنید", "de": "Schließe deine erste Lektion ab"}, "category": "learning", "tier": "bronze", "icon_emoji": "📖", "xp_reward": 25, "criteria": {"type": "lessons_completed", "target": 1}},
    {"code": "lesson_collector", "name": {"en": "Knowledge Seeker", "fa": "جستجوگر دانش", "de": "Wissenssucher"}, "description": {"en": "Complete 5 lessons", "fa": "۵ درس را کامل کنید", "de": "Schließe 5 Lektionen ab"}, "category": "learning", "tier": "bronze", "icon_emoji": "📚", "xp_reward": 50, "criteria": {"type": "lessons_completed", "target": 5}},
    {"code": "lesson_master", "name": {"en": "Scholar", "fa": "دانشمند", "de": "Gelehrter"}, "description": {"en": "Complete 20 lessons", "fa": "۲۰ درس را کامل کنید", "de": "Schließe 20 Lektionen ab"}, "category": "learning", "tier": "gold", "icon_emoji": "🎓", "xp_reward": 200, "criteria": {"type": "lessons_completed", "target": 20}},
    {"code": "module_complete", "name": {"en": "Module Master", "fa": "استاد ماژول", "de": "Modul-Meister"}, "description": {"en": "Complete an entire module", "fa": "یک ماژول کامل را تمام کنید", "de": "Schließe ein ganzes Modul ab"}, "category": "learning", "tier": "silver", "icon_emoji": "🏆", "xp_reward": 100, "criteria": {"type": "modules_completed", "target": 1}},

    # Quiz badges
    {"code": "quiz_ace", "name": {"en": "Quiz Ace", "fa": "آس آزمون", "de": "Quiz-Ass"}, "description": {"en": "Get a perfect score on a quiz", "fa": "نمره کامل در یک آزمون بگیرید", "de": "Erreiche die Höchstpunktzahl in einem Quiz"}, "category": "quiz", "tier": "silver", "icon_emoji": "💯", "xp_reward": 75, "criteria": {"type": "perfect_quizzes", "target": 1}},
    {"code": "quiz_master", "name": {"en": "Quiz Master", "fa": "استاد آزمون", "de": "Quiz-Meister"}, "description": {"en": "Pass 10 quizzes", "fa": "۱۰ آزمون را قبول شوید", "de": "Bestehe 10 Quizze"}, "category": "quiz", "tier": "gold", "icon_emoji": "🧠", "xp_reward": 150, "criteria": {"type": "quizzes_passed", "target": 10}},

    # Trading badges
    {"code": "first_trade", "name": {"en": "First Trade", "fa": "اولین معامله", "de": "Erster Trade"}, "description": {"en": "Place your first paper trade", "fa": "اولین معامله آزمایشی خود را انجام دهید", "de": "Platziere deinen ersten Papier-Trade"}, "category": "trading", "tier": "bronze", "icon_emoji": "📈", "xp_reward": 50, "criteria": {"type": "trades_completed", "target": 1}},
    {"code": "trader_10", "name": {"en": "Active Trader", "fa": "معامله‌گر فعال", "de": "Aktiver Trader"}, "description": {"en": "Complete 10 paper trades", "fa": "۱۰ معامله آزمایشی انجام دهید", "de": "Schließe 10 Papier-Trades ab"}, "category": "trading", "tier": "silver", "icon_emoji": "💹", "xp_reward": 100, "criteria": {"type": "trades_completed", "target": 10}},
    {"code": "trader_50", "name": {"en": "Veteran Trader", "fa": "معامله‌گر باتجربه", "de": "Erfahrener Trader"}, "description": {"en": "Complete 50 paper trades", "fa": "۵۰ معامله آزمایشی انجام دهید", "de": "Schließe 50 Papier-Trades ab"}, "category": "trading", "tier": "gold", "icon_emoji": "🥇", "xp_reward": 300, "criteria": {"type": "trades_completed", "target": 50}},

    # Streak badges
    {"code": "streak_3_days", "name": {"en": "3-Day Streak", "fa": "استریک ۳ روزه", "de": "3-Tage-Serie"}, "description": {"en": "Login 3 days in a row", "fa": "۳ روز پیاپی وارد شوید", "de": "3 Tage hintereinander anmelden"}, "category": "streak", "tier": "bronze", "icon_emoji": "🔥", "xp_reward": 30, "criteria": {"type": "login_streak", "target": 3}},
    {"code": "streak_7_days", "name": {"en": "Week Warrior", "fa": "جنگجوی هفته", "de": "Wochenkrieger"}, "description": {"en": "Login 7 days in a row", "fa": "۷ روز پیاپی وارد شوید", "de": "7 Tage hintereinander anmelden"}, "category": "streak", "tier": "silver", "icon_emoji": "⚡", "xp_reward": 100, "criteria": {"type": "login_streak", "target": 7}},
    {"code": "streak_30_days", "name": {"en": "Monthly Champion", "fa": "قهرمان ماهانه", "de": "Monats-Champion"}, "description": {"en": "Login 30 days in a row", "fa": "۳۰ روز پیاپی وارد شوید", "de": "30 Tage hintereinander anmelden"}, "category": "streak", "tier": "gold", "icon_emoji": "👑", "xp_reward": 500, "criteria": {"type": "login_streak", "target": 30}},

    # Level badges
    {"code": "level_5_novice", "name": {"en": "Rising Star", "fa": "ستاره درخشان", "de": "Aufsteigender Stern"}, "description": {"en": "Reach level 5", "fa": "به سطح ۵ برسید", "de": "Erreiche Level 5"}, "category": "mastery", "tier": "bronze", "icon_emoji": "⭐", "xp_reward": 50, "criteria": {"type": "level", "target": 5}},
    {"code": "level_10_expert", "name": {"en": "Trading Expert", "fa": "متخصص معامله‌گری", "de": "Trading-Experte"}, "description": {"en": "Reach level 10", "fa": "به سطح ۱۰ برسید", "de": "Erreiche Level 10"}, "category": "mastery", "tier": "gold", "icon_emoji": "🌟", "xp_reward": 200, "criteria": {"type": "level", "target": 10}},
    {"code": "level_20_legend", "name": {"en": "Trading Legend", "fa": "افسانه معامله‌گری", "de": "Trading-Legende"}, "description": {"en": "Reach level 20", "fa": "به سطح ۲۰ برسید", "de": "Erreiche Level 20"}, "category": "mastery", "tier": "diamond", "icon_emoji": "💎", "xp_reward": 1000, "criteria": {"type": "level", "target": 20}},
]

DAILY_CHALLENGES = [
    {"challenge_type": "daily_lesson", "title": {"en": "Complete 1 Lesson", "fa": "۱ درس را کامل کنید", "de": "Schließe 1 Lektion ab"}, "description": {"en": "Complete at least one lesson today", "fa": "امروز حداقل یک درس را کامل کنید", "de": "Schließe heute mindestens eine Lektion ab"}, "target": 1, "xp_reward": 80, "coin_reward": 10},
    {"challenge_type": "daily_quiz", "title": {"en": "Quiz Challenge", "fa": "چالش آزمون", "de": "Quiz-Herausforderung"}, "description": {"en": "Answer 3 quiz questions correctly", "fa": "به ۳ سؤال آزمون درست پاسخ دهید", "de": "Beantworte 3 Quizfragen richtig"}, "target": 3, "xp_reward": 100, "coin_reward": 15},
    {"challenge_type": "daily_trade", "title": {"en": "Paper Trader", "fa": "معامله‌گر آزمایشی", "de": "Papier-Trader"}, "description": {"en": "Place 2 paper trades today", "fa": "امروز ۲ معامله آزمایشی انجام دهید", "de": "Platziere heute 2 Papier-Trades"}, "target": 2, "xp_reward": 60, "coin_reward": 8},
]

TUTORIALS = [
    {
        "slug": "how-to-read-charts",
        "title": {"en": "How to Read Trading Charts", "fa": "نحوه خواندن نمودارهای معاملاتی", "de": "Wie man Trading-Charts liest"},
        "description": {"en": "Learn the basics of reading candlestick charts, timeframes, and price action", "fa": "مبانی خواندن نمودارهای کندل‌استیک، تایم‌فریم‌ها و اکشن قیمت را بیاموزید", "de": "Lerne die Grundlagen des Lesens von Kerzencharts, Zeitrahmen und Price Action"},
        "category": "basics",
        "difficulty": 1,
        "estimated_minutes": 15,
        "xp_reward": 50,
        "order": 1,
        "steps": [
            {"type": "text", "content": {"en": "A candlestick chart shows the open, high, low, and close prices for a time period.", "fa": "نمودار کندل‌استیک قیمت‌های باز، بالا، پایین و بسته را برای یک بازه زمانی نشان می‌دهد.", "de": "Ein Kerzenchart zeigt die Eröffnungs-, Hoch-, Tief- und Schlusskurse für einen Zeitraum."}},
            {"type": "text", "content": {"en": "The body shows the range between open and close. Green = close > open (bullish), Red = close < open (bearish).", "fa": "بدنه محدوده بین باز و بسته را نشان می‌دهد. سبز = بسته > باز (صعودی)، قرمز = بسته < باز (نزولی).", "de": "Der Körper zeigt den Bereich zwischen Eröffnung und Schluss. Grün = Schluss > Eröffnung (bullisch), Rot = Schluss < Eröffnung (bärisch)."}},
            {"type": "text", "content": {"en": "Wicks (shadows) show the high and low prices reached during the period.", "fa": "سایه‌ها بالاترین و پایین‌ترین قیمت‌های رسیده در آن بازه را نشان می‌دهند.", "de": "Dochte (Schatten) zeigen die Hoch- und Tiefpreise, die während des Zeitraums erreicht wurden."}},
            {"type": "quiz", "content": {"question": {"en": "What does a green candle body mean?", "fa": "بدنه سبز کندل چه معنایی دارد؟", "de": "Was bedeutet ein grüner Kerzenkörper?"}, "options": [{"id": "a", "text": {"en": "Price closed higher than open", "fa": "قیمت بالاتر از باز بسته شده", "de": "Schlusskurs höher als Eröffnungskurs"}}, {"id": "b", "text": {"en": "Price closed lower than open", "fa": "قیمت پایین‌تر از باز بسته شده", "de": "Schlusskurs niedriger als Eröffnungskurs"}}, {"id": "c", "text": {"en": "No price movement", "fa": "بدون حرکت قیمت", "de": "Keine Preisbewegung"}}], "correct": "a"}},
        ],
    },
    {
        "slug": "placing-first-trade",
        "title": {"en": "Placing Your First Trade", "fa": "انجام اولین معامله", "de": "Deinen ersten Trade platzieren"},
        "description": {"en": "Step-by-step guide to placing your first paper trade with risk management", "fa": "راهنمای گام‌به‌گام انجام اولین معامله آزمایشی با مدیریت ریسک", "de": "Schritt-für-Schritt-Anleitung zum Platzieren deines ersten Papier-Trades mit Risikomanagement"},
        "category": "trading",
        "difficulty": 2,
        "estimated_minutes": 20,
        "xp_reward": 75,
        "order": 2,
        "steps": [
            {"type": "text", "content": {"en": "Before trading, always set a stop-loss to define your maximum acceptable loss.", "fa": "قبل از معامله، همیشه یک حد ضرر تعیین کنید تا حداکثر ضرر قابل قبول خود را مشخص کنید.", "de": "Setze vor dem Trading immer einen Stop-Loss, um deinen maximal akzeptablen Verlust zu definieren."}},
            {"type": "text", "content": {"en": "Never risk more than 1-2% of your total capital on a single trade.", "fa": "هرگز بیش از ۱-۲٪ از کل سرمایه خود را در یک معامله واحد ریسک نکنید.", "de": "Risikiere niemals mehr als 1-2% deines Gesamtkapitals bei einem einzelnen Trade."}},
            {"type": "text", "content": {"en": "Use a minimum 1:2 risk-reward ratio - for every $1 risked, aim for at least $2 profit.", "fa": "حداقل از نسبت ریسک به ریوارد ۱:۲ استفاده کنید - به ازای هر ۱ دلار ریسک، حداقل ۲ دلار سود هدف بگذارید.", "de": "Verwende ein Mindest-Risiko-Ertrags-Verhältnis von 1:2 - für jeden riskierten 1 $ ziele auf mindestens 2 $ Gewinn ab."}},
            {"type": "quiz", "content": {"question": {"en": "What is the recommended maximum risk per trade?", "fa": "حداکثر ریسک توصیه‌شده برای هر معامله چقدر است؟", "de": "Was ist das empfohlene maximale Risiko pro Trade?"}, "options": [{"id": "a", "text": {"en": "1-2% of capital", "fa": "۱-۲٪ از سرمایه", "de": "1-2% des Kapitals"}}, {"id": "b", "text": {"en": "10-20% of capital", "fa": "۱۰-۲۰٪ از سرمایه", "de": "10-20% des Kapitals"}}, {"id": "c", "text": {"en": "50% of capital", "fa": "۵۰٪ از سرمایه", "de": "50% des Kapitals"}}], "correct": "a"}},
        ],
    },
    {
        "slug": "understanding-rsi",
        "title": {"en": "Understanding RSI Indicator", "fa": "درک اندیکاتور RSI", "de": "Den RSI-Indikator verstehen"},
        "description": {"en": "Learn how to use the Relative Strength Index to identify overbought and oversold conditions", "fa": "یاد بگیرید چگونه از شاخص قدرت نسبی برای شناسایی شرایط اشباع خرید و فروش استفاده کنید", "de": "Lerne, wie du den Relative Strength Index verwendest, um überkaufte und überverkaufte Bedingungen zu identifizieren"},
        "category": "technical",
        "difficulty": 2,
        "estimated_minutes": 15,
        "xp_reward": 60,
        "order": 3,
        "steps": [
            {"type": "text", "content": {"en": "RSI oscillates between 0 and 100. It measures the speed and change of price movements.", "fa": "RSI بین ۰ تا ۱۰۰ نوسان می‌کند. سرعت و تغییر حرکات قیمت را اندازه‌گیری می‌کند.", "de": "RSI oszilliert zwischen 0 und 100. Er misst die Geschwindigkeit und Änderung der Preisbewegungen."}},
            {"type": "text", "content": {"en": "RSI above 70 = Overbought (potential sell signal). RSI below 30 = Oversold (potential buy signal).", "fa": "RSI بالای ۷۰ = اشباع خرید (سیگنال فروش احتمالی). RSI زیر ۳۰ = اشباع فروش (سیگنال خرید احتمالی).", "de": "RSI über 70 = Überkauft (potenzielles Verkaufssignal). RSI unter 30 = Überverkauft (potenzielles Kaufsignal)."}},
            {"type": "quiz", "content": {"question": {"en": "What does RSI above 70 indicate?", "fa": "RSI بالای ۷۰ چه نشانه‌ای است؟", "de": "Was bedeutet RSI über 70?"}, "options": [{"id": "a", "text": {"en": "Overbought condition", "fa": "شرایط اشباع خرید", "de": "Überkaufte Bedingung"}}, {"id": "b", "text": {"en": "Oversold condition", "fa": "شرایط اشباع فروش", "de": "Überverkaufte Bedingung"}}, {"id": "c", "text": {"en": "Neutral condition", "fa": "شرایط خنثی", "de": "Neutrale Bedingung"}}], "correct": "a"}},
        ],
    },
]

PATTERN_GAMES = [
    {
        "slug": "double-top-bearish",
        "title": {"en": "Double Top Pattern", "fa": "الگوی دو قله‌ای", "de": "Double-Top-Muster"},
        "description": {"en": "Identify this classic reversal pattern", "fa": "این الگوی کلاسیک برگشتی را شناسایی کنید", "de": "Identifiziere dieses klassische Umkehrmuster"},
        "difficulty": 2,
        "pattern_type": "double_top",
        "correct_answer": "double_top",
        "options": [
            {"id": "double_top", "name": {"en": "Double Top", "fa": "دو قله‌ای", "de": "Double Top"}},
            {"id": "double_bottom", "name": {"en": "Double Bottom", "fa": "دو کفی", "de": "Double Bottom"}},
            {"id": "head_shoulders", "name": {"en": "Head and Shoulders", "fa": "سر و شانه", "de": "Kopf und Schultern"}},
            {"id": "triangle", "name": {"en": "Triangle", "fa": "مثلثی", "de": "Dreieck"}},
        ],
        "explanation": {"en": "A Double Top forms after an uptrend when price reaches a high, retraces, and reaches a similar high again. It signals a potential bearish reversal.", "fa": "الگوی دو قله‌ای پس از یک روند صعودی شکل می‌گیرد وقتی قیمت به یک سقف می‌رسد، اصلاح می‌کند و دوباره به سقف مشابهی می‌رسد. نشان‌دهنده برگشت نزولی احتمالی است.", "de": "Ein Double Top bildet sich nach einem Aufwärtstrend, wenn der Preis ein Hoch erreicht, korrigiert und ein ähnliches Hoch erneut erreicht. Es signalisiert eine potenzielle bärische Umkehr."},
        "xp_reward": 30,
        "chart_data": [],  # Would be populated with synthetic OHLCV data
    },
    {
        "slug": "head-shoulders-bearish",
        "title": {"en": "Head and Shoulders Pattern", "fa": "الگوی سر و شانه", "de": "Kopf-Schultern-Muster"},
        "description": {"en": "Identify this powerful reversal pattern", "fa": "این الگوی قدرتمند برگشتی را شناسایی کنید", "de": "Identifiziere dieses starke Umkehrmuster"},
        "difficulty": 3,
        "pattern_type": "head_shoulders",
        "correct_answer": "head_shoulders",
        "options": [
            {"id": "double_top", "name": {"en": "Double Top", "fa": "دو قله‌ای", "de": "Double Top"}},
            {"id": "double_bottom", "name": {"en": "Double Bottom", "fa": "دو کفی", "de": "Double Bottom"}},
            {"id": "head_shoulders", "name": {"en": "Head and Shoulders", "fa": "سر و شانه", "de": "Kopf und Schultern"}},
            {"id": "triangle", "name": {"en": "Triangle", "fa": "مثلثی", "de": "Dreieck"}},
        ],
        "explanation": {"en": "Head and Shoulders has three peaks: a higher middle peak (head) with two lower peaks on either side (shoulders). It's one of the most reliable bearish reversal patterns.", "fa": "الگوی سر و شانه سه قله دارد: یک قله میانی بلندتر (سر) با دو قله کوتاه‌تر در هر طرف (شانه‌ها). یکی از قابل‌اعتمادترین الگوهای برگشت نزولی است.", "de": "Kopf und Schultern hat drei Gipfel: einen höheren mittleren Gipfel (Kopf) mit zwei niedrigeren Gipfeln auf jeder Seite (Schultern). Es ist eines der zuverlässigsten bärischen Umkehrmuster."},
        "xp_reward": 40,
        "chart_data": [],
    },
    {
        "slug": "bullish-engulfing",
        "title": {"en": "Bullish Engulfing", "fa": "الگوی پوششی صعودی", "de": "Bullisches Umkehrmuster"},
        "description": {"en": "Spot this bullish candlestick reversal", "fa": "این برگشت صعودی کندل‌استیک را شناسایی کنید", "de": "Erkenne diese bullische Kerzen-Umkehr"},
        "difficulty": 1,
        "pattern_type": "bullish_engulfing",
        "correct_answer": "bullish_engulfing",
        "options": [
            {"id": "bullish_engulfing", "name": {"en": "Bullish Engulfing", "fa": "پوششی صعودی", "de": "Bullisch Engulfing"}},
            {"id": "bearish_engulfing", "name": {"en": "Bearish Engulfing", "fa": "پوششی نزولی", "de": "Bärisch Engulfing"}},
            {"id": "hammer", "name": {"en": "Hammer", "fa": "چکش", "de": "Hammer"}},
            {"id": "shooting_star", "name": {"en": "Shooting Star", "fa": "ستاره تیرانداز", "de": "Sternschnuppe"}},
        ],
        "explanation": {"en": "Bullish Engulfing occurs when a large green candle completely engulfs the previous red candle. It signals strong buying pressure and potential reversal upward.", "fa": "الگوی پوششی صعودی زمانی رخ می‌دهد که یک کندل سبز بزرگ کاملاً کندل قرمز قبلی را در بر بگیرد. نشان‌دهنده فشار خرید قوی و برگشت احتمالی صعودی است.", "de": "Bullisches Engulfing tritt auf, wenn eine große grüne Kerze die vorherige rote Kerze vollständig einschließt. Es signalisiert starken Kaufruck und potenzielle Aufwärtsumkehr."},
        "xp_reward": 25,
        "chart_data": [],
    },
]


async def seed_gamification():
    """Populate database with gamification data."""
    print("🎮 Seeding gamification data...")

    async with get_db_context() as db:
        # Check if already seeded
        result = await db.execute(select(Badge).limit(1))
        if result.scalar_one_or_none():
            print("⚠️  Gamification data already exists. Skipping.")
            return

        # Seed badges
        for badge_data in BADGES:
            badge = Badge(
                id=uuid4(),
                code=badge_data["code"],
                name=badge_data["name"],
                description=badge_data["description"],
                category=badge_data["category"],
                tier=badge_data["tier"],
                icon_emoji=badge_data["icon_emoji"],
                xp_reward=badge_data["xp_reward"],
                criteria=badge_data["criteria"],
            )
            db.add(badge)
        print(f"  ✅ Created {len(BADGES)} badges")

        # Seed daily challenges
        today = datetime.now(timezone.utc)
        for challenge_data in DAILY_CHALLENGES:
            challenge = DailyChallenge(
                id=uuid4(),
                challenge_type=challenge_data["challenge_type"],
                title=challenge_data["title"],
                description=challenge_data["description"],
                target=challenge_data["target"],
                xp_reward=challenge_data["xp_reward"],
                coin_reward=challenge_data["coin_reward"],
                start_date=today.replace(hour=0, minute=0, second=0, microsecond=0),
                end_date=today.replace(hour=23, minute=59, second=59, microsecond=0),
                is_active=True,
            )
            db.add(challenge)
        print(f"  ✅ Created {len(DAILY_CHALLENGES)} daily challenges")

        # Seed tutorials
        for tutorial_data in TUTORIALS:
            tutorial = Tutorial(
                id=uuid4(),
                slug=tutorial_data["slug"],
                title=tutorial_data["title"],
                description=tutorial_data["description"],
                category=tutorial_data["category"],
                difficulty=tutorial_data["difficulty"],
                steps=tutorial_data["steps"],
                estimated_minutes=tutorial_data["estimated_minutes"],
                xp_reward=tutorial_data["xp_reward"],
                order=tutorial_data["order"],
                is_published=True,
            )
            db.add(tutorial)
        print(f"  ✅ Created {len(TUTORIALS)} tutorials")

        # Seed pattern games
        for game_data in PATTERN_GAMES:
            game = PatternGame(
                id=uuid4(),
                slug=game_data["slug"],
                title=game_data["title"],
                description=game_data["description"],
                difficulty=game_data["difficulty"],
                pattern_type=game_data["pattern_type"],
                chart_data=game_data["chart_data"],
                correct_answer=game_data["correct_answer"],
                options=game_data["options"],
                explanation=game_data["explanation"],
                xp_reward=game_data["xp_reward"],
                is_published=True,
            )
            db.add(game)
        print(f"  ✅ Created {len(PATTERN_GAMES)} pattern games")

        await db.commit()
        print("\n✅ Gamification data seeded successfully!")
        print(f"   Badges: {len(BADGES)}")
        print(f"   Challenges: {len(DAILY_CHALLENGES)}")
        print(f"   Tutorials: {len(TUTORIALS)}")
        print(f"   Pattern Games: {len(PATTERN_GAMES)}")


if __name__ == "__main__":
    asyncio.run(seed_gamification())
