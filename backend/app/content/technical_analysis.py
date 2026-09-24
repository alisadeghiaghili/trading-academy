"""Technical Analysis module.

Benchmark depth: CMT Level 1 topic map + Murphy/Nison core + explicit
statistical honesty about edge decay. Target: 10 lessons with formulas,
worked examples, and failure modes.
"""

from __future__ import annotations

from typing import Any


TECHNICAL_ANALYSIS: dict[str, Any] = {
    "slug": "technical-analysis",
    "title": "Technical Analysis",
    "description": (
        "Market structure, Dow theory, levels, volume, candlesticks, classical "
        "patterns, oscillators, volatility tools, multi-timeframe process, and "
        "system thinking with explicit failure modes."
    ),
    "order": 2,
    "required_tier": "free",
    "lessons": [
        {
            "slug": "dow-and-market-structure",
            "title": "Dow Theory and Market Structure",
            "description": "Trend definition, swing structure, and why structure precedes indicators.",
            "lesson_type": "theory",
            "order": 1,
            "estimated_minutes": 45,
            "content": {
                "html": """
<h2>Price is a path, not a sequence of indicator colors</h2>
<p>
Technical analysis starts with structure: how price moves between
liquidity. Dow's practical residue is still useful: trend is a sequence of
higher highs/higher lows (uptrend) or lower highs/lower lows (downtrend).
Everything else is secondary.
</p>

<h3>Swing points</h3>
<p>
Define swings with an explicit rule (e.g., fractal pivots with N-bar
confirmation) so the chart is reproducible. Ambiguous "obvious" swings are
how hindsight bias sneaks in.
</p>
<ul>
  <li><strong>HH / HL:</strong> constructive uptrend.</li>
  <li><strong>LH / LL:</strong> constructive downtrend.</li>
  <li><strong>Break of structure (BOS):</strong> invalidation of the prior swing sequence.</li>
</ul>

<h3>Trend vs range</h3>
<p>
Most tools are built for one regime. Oscillators shine in ranges and
bleed in trends. Moving-average logic shines in trends and whipsaws in
ranges. Step zero is regime classification, not indicator selection.
</p>

<h3>Worked example: labeling a day chart</h3>
<ol>
  <li>Mark confirmed pivot highs/lows with a fixed N (do not redraw later).</li>
  <li>Draw the last two swings that define current trend.</li>
  <li>Only after labeling, add any indicator.</li>
</ol>
<p>
If your thesis requires redrawn pivots to be correct, it is not a thesis.
</p>

<h3>Common mistakes</h3>
<ul>
  <li>Using indicators before defining structure.</li>
  <li>Calling every pullback a reversal.</li>
  <li>Mixing timeframe definitions of trend without a hierarchy.</li>
</ul>
""",
            },
            "quizzes": [
                {
                    "question_text": {
                        "en": "An uptrend in structure terms is primarily:",
                        "fa": "روند صعودی در اصطلاح ساختار عمدتاً چیست؟",
                        "de": "Ein Aufwärtstrend ist strukturell primär:",
                    },
                    "question_type": "single_choice",
                    "options": [
                        {"optionId": "a", "text": {"en": "RSI above 70", "fa": "RSI بالای ۷۰", "de": "RSI über 70"}},
                        {"optionId": "b", "text": {"en": "Sequence of higher highs and higher lows", "fa": "توالی HH و HL", "de": "Folge von HH und HL"}},
                        {"optionId": "c", "text": {"en": "Green candle today", "fa": "کندل سبز امروز", "de": "Grüne Kerze"}},
                        {"optionId": "d", "text": {"en": "High social sentiment", "fa": "سنتیمنت مثبت", "de": "Stimmung"}},
                    ],
                    "correct_answer": {"option_id": "b"},
                    "explanation": {
                        "en": "Structure definition is independent of oscillators.",
                        "fa": "تعریف ساختار مستقل از اسیلاتور است.",
                        "de": "Strukturdefinition ist indikatorunabhängig.",
                    },
                    "difficulty": 2,
                    "order": 1,
                },
                {
                    "question_text": {
                        "en": "Why define swing pivots with a fixed rule?",
                        "fa": "چرا پیوت‌ها را با قاعده ثابت تعریف کنیم؟",
                        "de": "Warum Pivots mit fester Regel?",
                    },
                    "question_type": "single_choice",
                    "options": [
                        {"optionId": "a", "text": {"en": "To prevent hindsight bias in labeling", "fa": "برای جلوگیری از hindsight bias در برچسب‌زنی", "de": "Gegen Hindsight-Bias"}},
                        {"optionId": "b", "text": {"en": "To make charts prettier", "fa": "برای زیباتر شدن چارت", "de": "Schönere Charts"}},
                        {"optionId": "c", "text": {"en": "To reduce fees", "fa": "برای کاهش کارمزد", "de": "Weniger Gebühren"}},
                        {"optionId": "d", "text": {"en": "To avoid tax", "fa": "برای فرار مالیاتی", "de": "Steuern"}},
                    ],
                    "correct_answer": {"option_id": "a"},
                    "explanation": {
                        "en": "Reproducible rules make structure testable and honest.",
                        "fa": "قاعده تکرارپذیر ساختار را آزمودنی و صادق می‌کند.",
                        "de": "Reproduzierbare Regeln machen Struktur testbar.",
                    },
                    "difficulty": 3,
                    "order": 2,
                },
            ],
        },
        {
            "slug": "support-resistance-liquidity",
            "title": "Support, Resistance, and Liquidity Pools",
            "description": "Levels as liquidity maps, not magic lines.",
            "lesson_type": "theory",
            "order": 2,
            "estimated_minutes": 40,
            "content": {
                "html": """
<h2>Levels are decision zones</h2>
<p>
Support/resistance (S/R) are prices where order flow historically
concentrates. They are self-reinforcing because participants place
executions around them — not because the chart "remembers".
</p>

<h3>Quality filters for a level</h3>
<ul>
  <li>Touch count with rejection quality (wicks vs full closes).</li>
  <li>Volume at level (participation, not just prints).</li>
  <li>Recency and regime (fresh range edge vs ancient line).</li>
  <li>Confluence: HTF level + structure pivot + VWAP/round number.</li>
</ul>

<h3>Liquidity pools</h3>
<p>
Stop clusters sit above old highs and below old lows. "Stop hunts" are
often just price seeking liquidity before reversing. If you place stops in
obvious pools, you pay for other people's research.
</p>

<h3>Worked example</h3>
<p>
Resistance at 100 with three failed closes and heavy volume. Instead of
shorting the touch blindly, define: only short on rejection candle closing
back below 99.2 with stop above 101.2. The level creates a plan; it is not
the plan.
</p>

<h3>Common mistakes</h3>
<ul>
  <li>Drawing twenty lines and calling it analysis.</li>
  <li>Treating a wick through a level as a full breakout.</li>
  <li>Ignoring where stops cluster before entry.</li>
</ul>
""",
            },
            "quizzes": [
                {
                    "question_text": {
                        "en": "A high-quality level is best supported by:",
                        "fa": "یک سطح باکیفیت با چه چیزی تأیید می‌شود؟",
                        "de": "Ein hochwertiges Level stützt sich auf:",
                    },
                    "question_type": "single_choice",
                    "options": [
                        {"optionId": "a", "text": {"en": "One random touch in 2019", "fa": "یک لمس تصادفی در ۲۰۱۹", "de": "Ein Zufallstouch 2019"}},
                        {"optionId": "b", "text": {"en": "Multiple quality reactions, volume, and confluence", "fa": "واکنش‌های باکیفیت متعدد، حجم و همپوشانی", "de": "Mehrere Qualitätsreaktionen, Volumen, Konfluenz"}},
                        {"optionId": "c", "text": {"en": "Influencer agreement", "fa": "توافق اینفلوئنسرها", "de": "Influencer"}},
                        {"optionId": "d", "text": {"en": "A single indicator alert", "fa": "یک آلارم اندیکاتور", "de": "Ein Alarm"}},
                    ],
                    "correct_answer": {"option_id": "b"},
                    "explanation": {
                        "en": "Levels earn weight from repeated participation and confluence.",
                        "fa": "سطوح با مشارکت تکرارشده و همپوشانی وزن می‌گیرند.",
                        "de": "Qualität kommt aus Teilnahme und Konfluenz.",
                    },
                    "difficulty": 2,
                    "order": 1,
                },
                {
                    "question_text": {
                        "en": "Stops placed exactly under an obvious swing low are vulnerable because:",
                        "fa": "استاپ دقیقاً زیر swing low آشکار آسیب‌پذیر است زیرا:",
                        "de": "Stops unter offensichtlichen Swing-Lows sind gefährlich, weil:",
                    },
                    "question_type": "single_choice",
                    "options": [
                        {"optionId": "a", "text": {"en": "Liquidity/stops cluster there", "fa": "نقدشوندگی/استاپ‌ها آنجا خوشه می‌شوند", "de": "Liquidity/Stops dort clusteren"}},
                        {"optionId": "b", "text": {"en": "Brokers ban swing lows", "fa": "بروکر swing low را بن می‌کند", "de": "Broker verbieten Swing-Lows"}},
                        {"optionId": "c", "text": {"en": "It increases funding", "fa": "funding زیاد می‌شود", "de": "Funding steigt"}},
                        {"optionId": "d", "text": {"en": "It changes token supply", "fa": "عرضه عوض می‌شود", "de": "Angebot ändert sich"}},
                    ],
                    "correct_answer": {"option_id": "a"},
                    "explanation": {
                        "en": "Price often seeks obvious stop liquidity before continuation or reversal.",
                        "fa": "قیمت اغلب ابتدا نقدشوندگی استاپ‌های آشکار را جست‌وجو می‌کند.",
                        "de": "Preis sucht oft offensichtliche Stop-Liquidity.",
                    },
                    "difficulty": 3,
                    "order": 2,
                },
            ],
        },
        {
            "slug": "volume-analysis",
            "title": "Volume and Participation",
            "description": "Using volume as confirmation, not decoration.",
            "lesson_type": "theory",
            "order": 3,
            "estimated_minutes": 40,
            "content": {
                "html": """
<h2>Volume measures participation</h2>
<p>
Price without volume is an advertisement. Volume shows how much
participation backed the move. The useful heuristics:
</p>
<ul>
  <li>Breakouts on expanding volume are more trustworthy than thin prints.</li>
  <li>Climactic volume at trend ends often marks exhaustion (needs structure confirmation).</li>
  <li>Low-volume pullbacks in uptrends are healthier than high-volume dumps.</li>
</ul>

<h3>VWAP as an anchor</h3>
<p>
VWAP = <code>Σ(price × volume) / Σ(volume)</code>. Institutions benchmark
execution around VWAP. For discretionary traders it is a dynamic fair
value line for the session/period — not a magic magnet every hour.
</p>

<h3>Worked example: failed breakout</h3>
<p>
Price breaks range high on 1.2× average volume but closes back inside the
range with a large upper wick. Treat as liquidity probe unless volume and
acceptance improve on retest. Structure + volume together beat either alone.
</p>

<h3>Common mistakes</h3>
<ul>
  <li>Reading volume on low-liquidity venues as truth.</li>
  <li>Using volume as a standalone buy signal.</li>
  <li>Comparing weekend volume to weekday without normalization.</li>
</ul>
""",
            },
            "quizzes": [
                {
                    "question_text": {
                        "en": "Breakout quality improves when accompanied by:",
                        "fa": "کیفیت بریک‌اوت با چه چیزی بهتر می‌شود؟",
                        "de": "Breakout-Qualität steigt mit:",
                    },
                    "question_type": "single_choice",
                    "options": [
                        {"optionId": "a", "text": {"en": "Expanding participation/volume", "fa": "افزایش مشارکت/حجم", "de": "Steigendem Volumen"}},
                        {"optionId": "b", "text": {"en": "Falling volume and long wicks", "fa": "حجم کاهشی و سایه بلند", "de": "Fallendem Volumen"}},
                        {"optionId": "c", "text": {"en": "More social posts", "fa": "پست بیشتر شبکه اجتماعی", "de": "Mehr Posts"}},
                        {"optionId": "d", "text": {"en": "Lower open interest always", "fa": "همیشه OI پایین‌تر", "de": "Immer niedrigeres OI"}},
                    ],
                    "correct_answer": {"option_id": "a"},
                    "explanation": {
                        "en": "Participation confirms that the level break was not a thin print.",
                        "fa": "مشارکت تأیید می‌کند شکست سطح چاپ نازک نبوده.",
                        "de": "Volumen bestätigt Beteiligung.",
                    },
                    "difficulty": 2,
                    "order": 1,
                },
                {
                    "question_text": {
                        "en": "VWAP is best used as:",
                        "fa": "VWAP بهتر استفاده می‌شود به‌عنوان:",
                        "de": "VWAP nutzt man am besten als:",
                    },
                    "question_type": "single_choice",
                    "options": [
                        {"optionId": "a", "text": {"en": "A guaranteed reversal magnet", "fa": "آهنربای تضمینی برگشت", "de": "Garantierten Umkehrmagneten"}},
                        {"optionId": "b", "text": {"en": "A volume-weighted fair value anchor", "fa": "لنگر ارزش منصفانه وزن‌دار با حجم", "de": "Volumen-gewichteten Fair-Value-Anker"}},
                        {"optionId": "c", "text": {"en": "A tax calculator", "fa": "ماشین حساب مالیات", "de": "Steuerrechner"}},
                        {"optionId": "d", "text": {"en": "A wallet balance", "fa": "موجودی کیف پول", "de": "Wallet-Guthaben"}},
                    ],
                    "correct_answer": {"option_id": "b"},
                    "explanation": {
                        "en": "VWAP is an execution/fair-value reference, not a signal engine.",
                        "fa": "VWAP مرجع اجرا/ارزش منصفانه است، نه موتور سیگنال.",
                        "de": "VWAP ist Referenz, kein Signalgenerator.",
                    },
                    "difficulty": 2,
                    "order": 2,
                },
            ],
        },
        {
            "slug": "candlesticks",
            "title": "Candlesticks with Statistical Honesty",
            "description": "Wicks, bodies, and setups — without folklore overclaiming.",
            "lesson_type": "theory",
            "order": 4,
            "estimated_minutes": 45,
            "content": {
                "html": """
<h2>Candles compress four prices</h2>
<p>
OHLC candles show open/high/low/close. Bodies and wicks tell a short
story about intrabar rejection. The trader's job is to combine that story
with location (S/R, structure) and participation (volume).
</p>

<h3>High-utility patterns (context-dependent)</h3>
<ul>
  <li><strong>Pin bar / hammer:</strong> rejection wick against a level.</li>
  <li><strong>Engulfing:</strong> body covers prior body; stronger at extremes.</li>
  <li><strong>Inside bar:</strong> compression; breakout play, not direction by itself.</li>
  <li><strong>Doji:</strong> indecision; only meaningful at decision zones.</li>
</ul>

<h3>Base rates and honesty</h3>
<p>
Named candle patterns are not oracles. Published hit rates vary wildly
by market and filter. If a pattern has 55% directional accuracy with 1:1
rewards, edge is thin after fees. Always ask: accuracy × payoff − costs.
</p>

<h3>Worked example</h3>
<p>
Hammer at daily support after a downtrend with above-average volume:
location ✓, participation ✓, pattern ✓. Hammer in the middle of a choppy
range on low volume: ignore.
</p>

<h3>Common mistakes</h3>
<ul>
  <li>Memorizing 40 candle names instead of learning rejection + location.</li>
  <li>Ignoring timeframe of the candle.</li>
  <li>Treating one candle as a complete system.</li>
</ul>
""",
            },
            "quizzes": [
                {
                    "question_text": {
                        "en": "A hammer candle is most meaningful when it appears:",
                        "fa": "کندل hammer وقتی معنادارتر است که:",
                        "de": "Ein Hammer ist am bedeutsamsten bei:",
                    },
                    "question_type": "single_choice",
                    "options": [
                        {"optionId": "a", "text": {"en": "At a tested support with volume", "fa": "روی حمایت آزموده‌شده با حجم", "de": "Getestetem Support mit Volumen"}},
                        {"optionId": "b", "text": {"en": "Anywhere on any chart", "fa": "هرجای هر چارتی", "de": "Überall"}},
                        {"optionId": "c", "text": {"en": "Only in monthly charts", "fa": "فقط ماهانه", "de": "Nur Monatscharts"}},
                        {"optionId": "d", "text": {"en": "When funding is negative", "fa": "وقتی funding منفی است", "de": "Bei negativem Funding"}},
                    ],
                    "correct_answer": {"option_id": "a"},
                    "explanation": {
                        "en": "Pattern quality is conditional on location and participation.",
                        "fa": "کیفیت الگو مشروط به محل و مشارکت است.",
                        "de": "Musterqualität ist bedingt durch Kontext.",
                    },
                    "difficulty": 2,
                    "order": 1,
                },
                {
                    "question_text": {
                        "en": "Why must candle patterns be judged with payoff and costs?",
                        "fa": "چرا الگوهای کندلی باید با payoff و هزینه سنجیده شوند؟",
                        "de": "Warum Muster mit Payoff und Kosten bewerten?",
                    },
                    "question_type": "single_choice",
                    "options": [
                        {"optionId": "a", "text": {"en": "Because modest hit rates can be unprofitable after fees/slippage", "fa": "چون دقت متوسط پس از هزینه ممکن است زیان‌ده باشد", "de": "Mäßige Trefferquoten können nach Kosten unprofitabel sein"}},
                        {"optionId": "b", "text": {"en": "Because candles are fake", "fa": "چون کندل‌ها جعلی‌اند", "de": "Kerzen sind fake"}},
                        {"optionId": "c", "text": {"en": "Because brokers hide patterns", "fa": "بروکر الگو را مخفی می‌کند", "de": "Broker verstecken Muster"}},
                        {"optionId": "d", "text": {"en": "To simplify accounting only", "fa": "فقط برای حسابداری", "de": "Nur Buchhaltung"}},
                    ],
                    "correct_answer": {"option_id": "a"},
                    "explanation": {
                        "en": "Expectancy requires accuracy and payoff net of costs.",
                        "fa": "expectancy نیازمند دقت و payoff خالص هزینه است.",
                        "de": "Erwartungswert braucht Trefferquote und Payoff netto.",
                    },
                    "difficulty": 3,
                    "order": 2,
                },
            ],
        },
        {
            "slug": "classical-patterns",
            "title": "Classical Patterns and Failure Rates",
            "description": "Continuation/reversal patterns with invalidation logic.",
            "lesson_type": "theory",
            "order": 5,
            "estimated_minutes": 45,
            "content": {
                "html": """
<h2>Patterns are compressed scenarios</h2>
<p>
Head & shoulders, double top/bottom, triangles, wedges, flags — these
encode supply/demand battlegrounds. Use them as scenario templates with
explicit invalidation, not as certainty machines.
</p>

<h3>Pattern grammar</h3>
<ul>
  <li><strong>Reversal:</strong> prior trend + exhaustion structure (e.g., H&S).</li>
  <li><strong>Continuation:</strong> consolidation against trend (flags, pennants).</li>
  <li><strong>Bilateral:</strong> coils/triangles that can break either way (plan both sides).</li>
</ul>

<h3>Measured moves</h3>
<p>
Classic projection: height of pattern added to breakout. Treat measured
moves as <em>planning anchors</em> for partials, not price guarantees.
</p>

<h3>Worked example: double top</h3>
<ol>
  <li>First rejection at R with volume.</li>
  <li>Second rejection slightly lower (or equal) with weaker impulse.</li>
  <li>Trigger: close below neckline/structure low.</li>
  <li>Invalidation: acceptance back above second high.</li>
</ol>

<h3>Common mistakes</h3>
<ul>
  <li>Forcing patterns on every timeframe.</li>
  <li>Trading the pattern before the trigger level.</li>
  <li>Ignoring the broader regime (trend vs range).</li>
</ul>
""",
            },
            "quizzes": [
                {
                    "question_text": {
                        "en": "A bilateral triangle requires a plan that includes:",
                        "fa": "مثلث دوطرفه نیازمند طرحی است شامل:",
                        "de": "Ein bilaterales Dreieck braucht einen Plan für:",
                    },
                    "question_type": "single_choice",
                    "options": [
                        {"optionId": "a", "text": {"en": "Only long setups", "fa": "فقط لانگ", "de": "Nur Long"}},
                        {"optionId": "b", "text": {"en": "Both breakout directions and invalidation", "fa": "هر دو جهت بریک‌اوت و حد باطل", "de": "Beide Richtungen und Invalidierung"}},
                        {"optionId": "c", "text": {"en": "No stop loss", "fa": "بدون حد ضرر", "de": "Ohne Stop"}},
                        {"optionId": "d", "text": {"en": "Doubling size if unsure", "fa": "دو برابر کردن سایز", "de": "Doppelte Size"}},
                    ],
                    "correct_answer": {"option_id": "b"},
                    "explanation": {
                        "en": "Bilateral patterns have two scenarios until one is eliminated.",
                        "fa": "الگوهای دوطرفه تا حذف یک سناریو دو مسیر دارند.",
                        "de": "Bilaterale Muster haben zwei Szenarien.",
                    },
                    "difficulty": 2,
                    "order": 1,
                },
                {
                    "question_text": {
                        "en": "Measured-move targets should be used primarily to:",
                        "fa": "اهداف measured-move عمدتاً برای چه استفاده می‌شوند؟",
                        "de": "Measured Moves nutzt man primär zum:",
                    },
                    "question_type": "single_choice",
                    "options": [
                        {"optionId": "a", "text": {"en": "Guarantee exact fills of profit", "fa": "تضمین دقیق سود", "de": "Garantierten Gewinn"}},
                        {"optionId": "b", "text": {"en": "Plan partials and R-multiple expectations", "fa": "برنامه‌ریزی partial و انتظار R-multiple", "de": "Teilgewinne und R-Multiple planen"}},
                        {"optionId": "c", "text": {"en": "Set leverage max", "fa": "تعیین حداکثر اهرم", "de": "Leverage"}},
                        {"optionId": "d", "text": {"en": "Pick exchange", "fa": "انتخاب صرافی", "de": "Börse"}},
                    ],
                    "correct_answer": {"option_id": "b"},
                    "explanation": {
                        "en": "Projections are planning aids, not contracts with the market.",
                        "fa": "پروجکشن کمک برنامه‌ریزی است نه قرارداد با بازار.",
                        "de": "Projektionen sind Planungshilfen.",
                    },
                    "difficulty": 3,
                    "order": 2,
                },
            ],
        },
        {
            "slug": "moving-averages",
            "title": "Moving Averages and Trend Filters",
            "description": "SMA/EMA math, lag trade-offs, and non-magical uses.",
            "lesson_type": "theory",
            "order": 6,
            "estimated_minutes": 40,
            "content": {
                "html": """
<h2>Definitions</h2>
<p>
SMA(n) is the arithmetic mean of the last n closes:
<code>SMA = (P1 + ... + Pn) / n</code>.
EMA applies exponential weights:
<code>EMA_t = α·P_t + (1-α)·EMA_{t-1}</code> with
<code>α = 2/(n+1)</code>.
</p>
<p>
EMA reacts faster; SMA is steadier. Faster is not better — it just shifts
the whipsaw/lag trade-off.
</p>

<h3>Legitimate uses</h3>
<ul>
  <li>Regime filter (price vs 200-period as broad bias).</li>
  <li>Dynamic support/resistance in strong trends.</li>
  <li>Entry timing component (pullback to MA) inside a structure plan.</li>
</ul>

<h3>Illegitimate uses</h3>
<ul>
  <li>Golden cross as a money printer.</li>
  <li>Using MA crosses in pure ranges without filters.</li>
  <li>Curve-fitting n until backtest looks perfect.</li>
</ul>

<h3>Worked example</h3>
<p>
Trend filter: only long when price &gt; 200 EMA and structure is HH/HL.
Pullback longs toward 20 EMA with stop below swing. In chop where price
oscillates 200 EMA, the system stands aside. The filter's job is to avoid
bleed, not to add signals.
</p>
""",
            },
            "quizzes": [
                {
                    "question_text": {
                        "en": "Compared with SMA of the same period, EMA typically:",
                        "fa": "EMA در مقایسه با SMA با همان دوره معمولاً:",
                        "de": "EMA im Vergleich zu SMA:",
                    },
                    "question_type": "single_choice",
                    "options": [
                        {"optionId": "a", "text": {"en": "Reacts faster to new prices", "fa": "به قیمت جدید سریع‌تر واکنش می‌دهد", "de": "reagiert schneller"}},
                        {"optionId": "b", "text": {"en": "Is always more profitable", "fa": "همیشه سودآورتر است", "de": "ist immer profitabler"}},
                        {"optionId": "c", "text": {"en": "Uses only the first and last close", "fa": "فقط اولین و آخرین close", "de": "nutzt nur erste/letzte"}},
                        {"optionId": "d", "text": {"en": "Removes all whipsaws", "fa": "همه whipsaw را حذف می‌کند", "de": "entfernt Whipsaws"}},
                    ],
                    "correct_answer": {"option_id": "a"},
                    "explanation": {
                        "en": "Exponential weighting reduces lag and increases sensitivity — not magic profitability.",
                        "fa": "وزن‌دهی نمایی lag را کم و حساسیت را زیاد می‌کند؛ سود جادویی نیست.",
                        "de": "Exponentielle Gewichtung reduziert Lag.",
                    },
                    "difficulty": 2,
                    "order": 1,
                },
                {
                    "question_text": {
                        "en": "MA crossover systems fail most in:",
                        "fa": "سیستم‌های کراس MA بیشتر در کجا شکست می‌خورند؟",
                        "de": "MA-Crossover-Systeme scheitern meist in:",
                    },
                    "question_type": "single_choice",
                    "options": [
                        {"optionId": "a", "text": {"en": "Ranges/chop", "fa": "رنج/چاپ", "de": "Ranges/Chop"}},
                        {"optionId": "b", "text": {"en": "Strong trends", "fa": "روند قوی", "de": "starken Trends"}},
                        {"optionId": "c", "text": {"en": "Weekends only", "fa": "فقط آخر هفته", "de": "Wochenenden"}},
                        {"optionId": "d", "text": {"en": "High volume days", "fa": "روزهای حجم بالا", "de": "Volumenstarken Tagen"}},
                    ],
                    "correct_answer": {"option_id": "a"},
                    "explanation": {
                        "en": "Lagging trend logic bleeds under repeated crosses in ranges.",
                        "fa": "منطق روند کند در رنج با کراس‌های تکراری خونریزی می‌کند.",
                        "de": "Trendfolge blutet in Ranges.",
                    },
                    "difficulty": 2,
                    "order": 2,
                },
            ],
        },
        {
            "slug": "oscillators-rsi-macd-stoch",
            "title": "Oscillators: RSI, MACD, Stochastics",
            "description": "Formulas, divergence, and why oscillator folklore overfits.",
            "lesson_type": "theory",
            "order": 7,
            "estimated_minutes": 50,
            "content": {
                "html": """
<h2>RSI</h2>
<p>
Wilder's RSI compares average gains/losses over n periods:
<code>RS = avgGain/avgLoss</code>, <code>RSI = 100 - 100/(1+RS)</code>.
Classic thresholds 30/70 are conventions, not laws. In strong trends RSI
can pin at extremes for long stretches.
</p>

<h2>MACD</h2>
<p>
<code>MACD = EMA(fast) - EMA(slow)</code>, signal = EMA of MACD,
histogram = MACD − signal. Crossovers are lagged trend-following logic in
oscillator clothing.
</p>

<h2>Stochastics</h2>
<p>
<code>%K = 100 * (C - L_n) / (H_n - L_n)</code> with %D as SMA of %K.
Useful in ranges for stretch/reversion, poor as trend engine.
</p>

<h3>Divergence, carefully</h3>
<p>
Bullish divergence: price makes lower low, oscillator makes higher low.
It is a <em>weakening momentum hypothesis</em>, not a buy order. Require
structure confirmation (break of minor lower high) before execution.
</p>

<h3>Worked example</h3>
<p>
Range-bound market: RSI(14) dips to 28 at range low with double-bottom
structure — reversion long candidate with stop under range. Trending
market: ignore "overbought" RSI while structure remains HH/HL.
</p>

<h3>Common mistakes</h3>
<ul>
  <li>Selling solely because RSI &gt; 70.</li>
  <li>Stacking three oscillators and thinking it is confluence (they are correlated).</li>
  <li>Using default parameters without regime awareness.</li>
</ul>
""",
            },
            "quizzes": [
                {
                    "question_text": {
                        "en": "RSI formula uses:",
                        "fa": "فرمول RSI از چه استفاده می‌کند؟",
                        "de": "Die RSI-Formel nutzt:",
                    },
                    "question_type": "single_choice",
                    "options": [
                        {"optionId": "a", "text": {"en": "Ratio of average gains to average losses", "fa": "نسبت میانگین سود به زیان", "de": "Verhältnis ØGewinn/ØVerlust"}},
                        {"optionId": "b", "text": {"en": "Only closing price", "fa": "فقط close", "de": "nur Close"}},
                        {"optionId": "c", "text": {"en": "Open interest", "fa": "open interest", "de": "Open Interest"}},
                        {"optionId": "d", "text": {"en": "Funding rates", "fa": "funding", "de": "Funding"}},
                    ],
                    "correct_answer": {"option_id": "a"},
                    "explanation": {
                        "en": "RSI is a smoothed gain/loss ratio mapped to 0–100.",
                        "fa": "RSI نسبت صاف‌شده سود/زیان در بازه ۰–۱۰۰ است.",
                        "de": "RSI ist ein geglättetes Verhältnis.",
                    },
                    "difficulty": 2,
                    "order": 1,
                },
                {
                    "question_text": {
                        "en": "MACD is fundamentally a form of:",
                        "fa": "MACD در ذات نوعی از چیست؟",
                        "de": "MACD ist im Kern eine Form von:",
                    },
                    "question_type": "single_choice",
                    "options": [
                        {"optionId": "a", "text": {"en": "Lagging momentum/trend logic", "fa": "منطق مومنتوم/روند کند", "de": "verzögerter Momentum/Trend-Logik"}},
                        {"optionId": "b", "text": {"en": "Order book depth", "fa": "عمق order book", "de": "Orderbuch"}},
                        {"optionId": "c", "text": {"en": "Valuation model", "fa": "مدل ارزش‌گذاری", "de": "Bewertungsmodell"}},
                        {"optionId": "d", "text": {"en": "Wallet security", "fa": "امنیت کیف پول", "de": "Wallet-Sicherheit"}},
                    ],
                    "correct_answer": {"option_id": "a"},
                    "explanation": {
                        "en": "EMA differences are trend/momentum filters with lag.",
                        "fa": "تفاوت EMA فیلتر روند/مومنتوم با lag است.",
                        "de": "EMA-Differenzen sind Trendfilter.",
                    },
                    "difficulty": 2,
                    "order": 2,
                },
                {
                    "question_text": {
                        "en": "Bullish divergence should be treated as:",
                        "fa": "واگرایی صعودی باید در نظر گرفته شود به‌عنوان:",
                        "de": "Bullische Divergenz ist zu behandeln als:",
                    },
                    "question_type": "single_choice",
                    "options": [
                        {"optionId": "a", "text": {"en": "An automatic market-buy", "fa": "خرید بازار خودکار", "de": "Sofortkauf"}},
                        {"optionId": "b", "text": {"en": "A momentum-weakening hypothesis needing confirmation", "fa": "فرض تضعیف مومنتوم نیازمند تأیید", "de": "Hypothese mit Bestätigungsbedarf"}},
                        {"optionId": "c", "text": {"en": "A guarantee of reversal", "fa": "تضمین برگشت", "de": "Garantie"}},
                        {"optionId": "d", "text": {"en": "A funding signal", "fa": "سیگنال funding", "de": "Funding-Signal"}},
                    ],
                    "correct_answer": {"option_id": "b"},
                    "explanation": {
                        "en": "Divergence is evidence, not an order type.",
                        "fa": "واگرایی شاهد است نه نوع سفارش.",
                        "de": "Divergenz ist Evidenz, kein Order-Typ.",
                    },
                    "difficulty": 3,
                    "order": 3,
                },
            ],
        },
        {
            "slug": "volatility-tools",
            "title": "Volatility Tools: ATR, Bollinger, Channels",
            "description": "Measuring range to size risk and judge stretch.",
            "lesson_type": "theory",
            "order": 8,
            "estimated_minutes": 40,
            "content": {
                "html": """
<h2>ATR</h2>
<p>
True Range:
<code>TR = max(H-L, |H-C_prev|, |L-C_prev|)</code>.
ATR is a moving average of TR. It answers: how wide is normal movement?
That makes it a stop-distance and position-size input — not a direction tool.
</p>

<h2>Bollinger Bands</h2>
<p>
Middle = SMA(n). Bands = middle ± k·stddev(close).
Width expands/contracts with volatility. "Walk the bands" happens in
trends; mean-reversion logic on bands alone is regime-fragile.
</p>

<h3>Operational use</h3>
<ul>
  <li>Stop = entry − 1.5×ATR (example policy) instead of arbitrary $ amount.</li>
  <li>Breakout filter: require range expansion (band width / ATR rising).</li>
  <li>Position sizing inverse to ATR to normalize risk per symbol.</li>
</ul>

<h3>Worked example</h3>
<p>
BTC ATR(14) on 4h = $900. If stop is 1.5 ATR, stop distance ≈ $1,350.
Risk $500 → size = 500/1350 ≈ 0.37 BTC notional units. Volatility-aware
sizing beats fixed quantity across symbols.
</p>

<h3>Common mistakes</h3>
<ul>
  <li>Using Bollinger as a pure counter-trend system without filters.</li>
  <li>Same $ stop on low- and high-volatility assets.</li>
</ul>
""",
            },
            "quizzes": [
                {
                    "question_text": {
                        "en": "ATR is primarily useful for:",
                        "fa": "ATR عمدتاً برای چه مفید است؟",
                        "de": "ATR ist primär nützlich für:",
                    },
                    "question_type": "single_choice",
                    "options": [
                        {"optionId": "a", "text": {"en": "Direction prediction", "fa": "پیش‌بینی جهت", "de": "Richtung"}},
                        {"optionId": "b", "text": {"en": "Stop distance and volatility-normalized sizing", "fa": "فاصله حد ضرر و سایز نرمال‌شده نوسان", "de": "Stopdistanz und volatilitätsnormierte Size"}},
                        {"optionId": "c", "text": {"en": "KYC", "fa": "KYC", "de": "KYC"}},
                        {"optionId": "d", "text": {"en": "Token unlock schedules", "fa": "زمان‌بندی unlock", "de": "Unlocks"}},
                    ],
                    "correct_answer": {"option_id": "b"},
                    "explanation": {
                        "en": "ATR measures typical range; use it to normalize risk.",
                        "fa": "ATR دامنه معمول را می‌سنجد؛ برای نرمال‌سازی ریسک.",
                        "de": "ATR misst typische Range.",
                    },
                    "difficulty": 2,
                    "order": 1,
                },
                {
                    "question_text": {
                        "en": "Bollinger band width contraction typically indicates:",
                        "fa": "انقباض عرض باند بولینگر معمولاً نشان‌دهنده:",
                        "de": "Kontrahierte Bollinger-Breite zeigt typisch:",
                    },
                    "question_type": "single_choice",
                    "options": [
                        {"optionId": "a", "text": {"en": "Lower volatility / compression", "fa": "نوسان کمتر / فشردگی", "de": "niedrigere Volatilität"}},
                        {"optionId": "b", "text": {"en": "Guaranteed breakout direction", "fa": "جهت تضمینی بریک‌اوت", "de": "garantierte Richtung"}},
                        {"optionId": "c", "text": {"en": "Exchange insolvency", "fa": "ورشکستگی صرافی", "de": "Insolvenz"}},
                        {"optionId": "d", "text": {"en": "Higher fees", "fa": "کارمزد بالاتر", "de": "höhere Fees"}},
                    ],
                    "correct_answer": {"option_id": "a"},
                    "explanation": {
                        "en": "Compression is a volatility state, not a direction forecast.",
                        "fa": "فشردگی وضعیت نوسان است نه پیش‌بینی جهت.",
                        "de": "Kompression ist Volatilitätszustand.",
                    },
                    "difficulty": 2,
                    "order": 2,
                },
            ],
        },
        {
            "slug": "multi-timeframe-process",
            "title": "Multi-Timeframe Decision Process",
            "description": "HTF bias → MTF structure → LTF trigger, without conflict soup.",
            "lesson_type": "practice",
            "order": 9,
            "estimated_minutes": 45,
            "content": {
                "html": """
<h2>Hierarchy, not democracy</h2>
<p>
Timeframes must not vote equally. A clean process:
</p>
<ol>
  <li><strong>HTF (daily/weekly):</strong> bias and major levels.</li>
  <li><strong>MTF (4h/1h):</strong> tradable structure and zones.</li>
  <li><strong>LTF (15m/5m):</strong> trigger and risk placement.</li>
</ol>
<p>
If LTF says long and HTF is bearish into resistance, the trade is optional
at best — usually skip. Conflict is information.
</p>

<h3>Practice workflow</h3>
<ul>
  <li>Write HTF bias in one sentence before opening LTF.</li>
  <li>Mark 3 key HTF levels max.</li>
  <li>Only look for setups that align with bias or are explicit countertrend with smaller risk.</li>
</ul>

<h3>Worked example</h3>
<p>
Daily: uptrend into prior weekly supply. 4h: distribution wicks. 5m: long
signal triggers. Action: skip or tiny risk. The trigger is not the boss.
</p>

<h3>Common mistakes</h3>
<ul>
  <li>Trading 1m with 1w bias and 1h confusion.</li>
  <li>Cherry-picking the timeframe that agrees with hope.</li>
</ul>
""",
            },
            "quizzes": [
                {
                    "question_text": {
                        "en": "If LTF long signal conflicts with HTF resistance bias, best default action:",
                        "fa": "اگر سیگنال لانگ LTF با بایاس مقاومتی HTF در تضاد باشد، اقدام پیش‌فرض:",
                        "de": "Bei Konflikt LTF-Long vs. HTF-Widerstand standardmäßig:",
                    },
                    "question_type": "single_choice",
                    "options": [
                        {"optionId": "a", "text": {"en": "Max leverage long", "fa": "لانگ حداکثر اهرم", "de": "Max-Hebel Long"}},
                        {"optionId": "b", "text": {"en": "Skip or cut risk drastically", "fa": "رد شدن یا کاهش شدید ریسک", "de": "Skip oder Risiko stark senken"}},
                        {"optionId": "c", "text": {"en": "Ignore HTF always", "fa": "همیشه HTF نادیده", "de": "HTF ignorieren"}},
                        {"optionId": "d", "text": {"en": "Add three oscillators", "fa": "اضافه کردن سه اسیلاتور", "de": "Drei Oszillatoren"}},
                    ],
                    "correct_answer": {"option_id": "b"},
                    "explanation": {
                        "en": "Higher-timeframe context gates lower-timeframe triggers.",
                        "fa": "بستر تایم‌فریم بالاتر تریگر پایین‌تر را فیلتر می‌کند.",
                        "de": "HTF-Kontext filtert LTF-Trigger.",
                    },
                    "difficulty": 3,
                    "order": 1,
                },
            ],
        },
        {
            "slug": "systems-and-expectancy",
            "title": "From Signals to Systems: Expectancy and Validation",
            "description": "Turning analysis into testable rules with positive expectancy.",
            "lesson_type": "practice",
            "order": 10,
            "estimated_minutes": 55,
            "content": {
                "html": """
<h2>Expectancy is the scoreboard</h2>
<p>
For a trade distribution:
<code>E[win] = p·W - (1-p)·L</code> (in R units where W,L are average win/loss).
Positive expectancy requires either hit-rate edge, payoff edge, or both —
after costs.
</p>

<h3>Minimum viable system spec</h3>
<ul>
  <li>Markets + session + regime filter.</li>
  <li>Entry trigger (binary, testable).</li>
  <li>Invalidation (stop rule).</li>
  <li>Exits (scale plan / trail / time stop).</li>
  <li>Position sizing rule.</li>
  <li>Max daily loss / mistake rules.</li>
</ul>

<h3>Validation hygiene</h3>
<ul>
  <li>In-sample / out-of-sample split; walk-forward if parameters exist.</li>
  <li>Count fees, spread, slippage.</li>
  <li>Watch overfitting: too many parameters vs trade count.</li>
  <li>Process metrics: plan adherence %, not just PnL.</li>
</ul>

<h3>Worked example</h3>
<p>
Setup: pullback long in HH/HL above 200 EMA, trigger break of minor LH,
stop below pulllow, scale 50% at 2R, trail rest. Simulate 100 trades with
fees. If E[R] ≤ 0.05 after costs, either improve filters or discard —
do not "believe harder".
</p>

<h3>Common mistakes</h3>
<ul>
  <li>Journaling screenshots without R multiples.</li>
  <li>Optimizing parameters until equity curve is beautiful.</li>
  <li>Changing the system weekly during drawdown.</li>
</ul>
""",
            },
            "quizzes": [
                {
                    "question_text": {
                        "en": "Expectancy in R units is approximately:",
                        "fa": "expectancy در واحد R تقریباً:",
                        "de": "Erwartungswert in R ist ungefähr:",
                    },
                    "question_type": "single_choice",
                    "options": [
                        {"optionId": "a", "text": {"en": "p·W - (1-p)·L", "fa": "p·W - (1-p)·L", "de": "p·W - (1-p)·L"}},
                        {"optionId": "b", "text": {"en": "Always win rate", "fa": "همیشه win rate", "de": "nur Winrate"}},
                        {"optionId": "c", "text": {"en": "Number of indicators", "fa": "تعداد اندیکاتور", "de": "Anzahl Indikatoren"}},
                        {"optionId": "d", "text": {"en": "Leverage", "fa": "اهرم", "de": "Hebel"}},
                    ],
                    "correct_answer": {"option_id": "a"},
                    "explanation": {
                        "en": "Expectancy blends hit rate and payoff net of losses/costs.",
                        "fa": "expectancy ترکیب دقت و payoff خالص است.",
                        "de": "Erwartungswert kombiniert Trefferquote und Payoff.",
                    },
                    "difficulty": 3,
                    "order": 1,
                },
                {
                    "question_text": {
                        "en": "A system edge must be evaluated:",
                        "fa": "edge یک سیستم باید ارزیابی شود:",
                        "de": "System-Edge bewertet man:",
                    },
                    "question_type": "single_choice",
                    "options": [
                        {"optionId": "a", "text": {"en": "After fees, spread, and slippage", "fa": "پس از کارمزد، اسپرد و slippage", "de": "nach Kosten"}},
                        {"optionId": "b", "text": {"en": "On screenshots", "fa": "روی اسکرین‌شات", "de": "per Screenshot"}},
                        {"optionId": "c", "text": {"en": "Without sample", "fa": "بدون نمونه", "de": "ohne Stichprobe"}},
                        {"optionId": "d", "text": {"en": "In one lucky week", "fa": "در یک هفته خوش‌شانس", "de": "eine Glückwoche"}},
                    ],
                    "correct_answer": {"option_id": "a"},
                    "explanation": {
                        "en": "Net of costs is the only tradable definition of edge.",
                        "fa": "تنها تعریف قابل‌معامله edge، خالص هزینه‌هاست.",
                        "de": "Netto-Kosten sind der einzige handelbare Edge.",
                    },
                    "difficulty": 2,
                    "order": 2,
                },
            ],
        },
    ],
}
