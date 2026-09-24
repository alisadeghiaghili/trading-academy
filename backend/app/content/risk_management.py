"""Risk Management module.

Benchmark depth: Van Tharp position sizing + Elder risk pillars + CFA-style
risk metrics (VaR/ES) with operational trading use. Target: 8 lessons with
formulas and worked examples.
"""

from __future__ import annotations

from typing import Any


RISK_MANAGEMENT: dict[str, Any] = {
    "slug": "risk-management",
    "title": "Risk Management",
    "description": (
        "Position sizing families, expectancy-linked risk, drawdown math, "
        "risk of ruin, correlation heat, VaR/ES, stop policy, and R-based trading."
    ),
    "order": 3,
    "required_tier": "free",
    "lessons": [
        {
            "slug": "r-multiples-expectancy",
            "title": "R-Multiples and Expectancy-First Risk",
            "description": "Define risk in R before thinking in dollars.",
            "lesson_type": "theory",
            "order": 1,
            "estimated_minutes": 40,
            "content": {
                "html": """
<h2>One unit of risk</h2>
<p>
Define <strong>1R</strong> as the loss taken if the trade is wrong and the
stop executes as planned. If entry 100, stop 96, size 25 units →
risk = 4 × 25 = $100 = 1R. A win of $250 is +2.5R.
</p>
<p>
This normalizes all markets and timeframes. Journal in R first, dollars
second.
</p>

<h3>Expectancy in R</h3>
<p>
<code>Expectancy = (Win% × AvgWinR) - (Loss% × AvgLossR)</code>
With symmetric 1R loss: <code>E = p·W - (1-p)·1</code>.
Break-even win rate at W=2R is 33.4%. This is why payoff design beats
prediction obsession.
</p>

<h3>Worked example</h3>
<ul>
  <li>40 trades, 45% win, avg win 2.1R, avg loss 1R.</li>
  <li>E = 0.45×2.1 − 0.55×1 = 0.945 − 0.55 = 0.395R per trade.</li>
  <li>Over 40 trades ≈ +15.8R gross before fees/slippage.</li>
</ul>
<p>
If costs consume 0.08R per trade, net E = 0.315R — still viable, but size
must respect drawdown math (next lessons).
</p>

<h3>Common mistakes</h3>
<ul>
  <li>Moving stops "because news" after risk was defined.</li>
  <li>Measuring success in dollars without R normalization.</li>
</ul>
""",
            },
            "quizzes": [
                {
                    "question_text": {
                        "en": "Entry 100, stop 96, size 25. What is 1R here?",
                        "fa": "ورود ۱۰۰، استاپ ۹۶، سایز ۲۵. اینجا 1R چیست؟",
                        "de": "Entry 100, Stop 96, Size 25. Was ist 1R?",
                    },
                    "question_type": "single_choice",
                    "options": [
                        {"optionId": "a", "text": {"en": "$4", "fa": "۴ دلار", "de": "$4"}},
                        {"optionId": "b", "text": {"en": "$100", "fa": "۱۰۰ دلار", "de": "$100"}},
                        {"optionId": "c", "text": {"en": "$25", "fa": "۲۵ دلار", "de": "$25"}},
                        {"optionId": "d", "text": {"en": "$1", "fa": "۱ دلار", "de": "$1"}},
                    ],
                    "correct_answer": {"option_id": "b"},
                    "explanation": {
                        "en": "1R = (entry-stop) × size = 4 × 25 = $100.",
                        "fa": "1R = (ورود-استاپ) × سایز = ۴ × ۲۵ = ۱۰۰.",
                        "de": "1R = Abstand × Size.",
                    },
                    "difficulty": 2,
                    "order": 1,
                },
                {
                    "question_text": {
                        "en": "At average win 2R and 1R losses, roughly what win rate breaks even (pre-costs)?",
                        "fa": "با میانگین برد ۲R و باخت ۱R، چه نرخ بردی تقریباً سر به سر است؟",
                        "de": "Bei 2R-Sieg und 1R-Verlust: Break-even-Trefferquote?",
                    },
                    "question_type": "single_choice",
                    "options": [
                        {"optionId": "a", "text": {"en": "33%", "fa": "۳۳٪", "de": "33%"}},
                        {"optionId": "b", "text": {"en": "50%", "fa": "۵۰٪", "de": "50%"}},
                        {"optionId": "c", "text": {"en": "67%", "fa": "۶۷٪", "de": "67%"}},
                        {"optionId": "d", "text": {"en": "90%", "fa": "۹۰٪", "de": "90%"}},
                    ],
                    "correct_answer": {"option_id": "a"},
                    "explanation": {
                        "en": "Break-even p = 1/(1+W) = 1/3 when W=2R.",
                        "fa": "p = 1/(1+W) = ۱/۳ وقتی W=2R.",
                        "de": "p = 1/(1+W).",
                    },
                    "difficulty": 3,
                    "order": 2,
                },
            ],
        },
        {
            "slug": "position-sizing-families",
            "title": "Position Sizing Families",
            "description": "Fixed fractional, fixed R, volatility targeting, and Kelly (bounded).",
            "lesson_type": "theory",
            "order": 2,
            "estimated_minutes": 50,
            "content": {
                "html": """
<h2>Size is the strategy's volume knob</h2>
<p>
A mediocre setup with right size can survive; a great setup with reckless
size can end the account. Sizing must be a rule, not a mood.
</p>

<h3>Fixed fractional</h3>
<p>
Risk a fixed fraction <code>f</code> of equity per trade:
<code>Size = (Equity × f) / StopDistance</code>.
Example: Equity $20,000, f = 0.5% → risk $100. Stop distance $5 → size 20 units.
</p>

<h3>Volatility-normalized (ATR) sizing</h3>
<p>
<code>Size = RiskDollars / (k × ATR)</code>. Same risk across symbols with
different noise. k often 1.5–3 depending on style.
</p>

<h3>Kelly criterion (theory and danger)</h3>
<p>
For binary odds: <code>f* = p - q</code> (edge fraction) in simple bet form;
more generally <code>f* = (bp - q)/b</code> where b = odds received.
Kelly maximizes long-run growth <em>if</em> p, b are known exactly. In markets
they are estimated poorly → practical use is fractional Kelly (0.25–0.5×)
with hard caps.
</p>

<h3>Worked example: comparing methods</h3>
<ul>
  <li>Equity $50k, planned risk 0.75% = $375.</li>
  <li>Stop distance $12 → fixed size 31.25 units.</li>
  <li>ATR = $8, k=2 → size = 375/16 = 23.4 units.</li>
</ul>
<p>
Volatility sizing is smaller because noise is high — correct behavior.
</p>

<h3>Common mistakes</h3>
<ul>
  <li>Full Kelly with estimated edge.</li>
  <li>Same quantity for BTC and a low-cap (different vol).</li>
  <li>Scaling size during emotional drawdown without a rule.</li>
</ul>
""",
            },
            "quizzes": [
                {
                    "question_text": {
                        "en": "Fixed fractional sizing formula is:",
                        "fa": "فرمول سایز fixed fractional:",
                        "de": "Fixed-Fractional-Formel:",
                    },
                    "question_type": "single_choice",
                    "options": [
                        {"optionId": "a", "text": {"en": "Size = (Equity × f) / StopDistance", "fa": "سایز = (سرمایه × f) / فاصله استاپ", "de": "Size = (Equity×f)/Stop"}},
                        {"optionId": "b", "text": {"en": "Size = Equity × 10", "fa": "سایز = سرمایه × ۱۰", "de": "Size = Equity×10"}},
                        {"optionId": "c", "text": {"en": "Size = ATR + RSI", "fa": "سایز = ATR + RSI", "de": "ATR+RSI"}},
                        {"optionId": "d", "text": {"en": "Size = random", "fa": "تصادفی", "de": "zufällig"}},
                    ],
                    "correct_answer": {"option_id": "a"},
                    "explanation": {
                        "en": "Risk dollars divided by stop distance gives quantity.",
                        "fa": "دلار ریسک تقسیم بر فاصله استاپ = تعداد.",
                        "de": "Risikodollar durch Stopdistanz.",
                    },
                    "difficulty": 2,
                    "order": 1,
                },
                {
                    "question_text": {
                        "en": "Full Kelly is dangerous in markets mainly because:",
                        "fa": "Kelly کامل در بازارها خطرناک است عمدتاً زیرا:",
                        "de": "Volles Kelly ist gefährlich, weil:",
                    },
                    "question_type": "single_choice",
                    "options": [
                        {"optionId": "a", "text": {"en": "Edge parameters are estimated with error", "fa": "پارامترهای edge با خطا تخمین می‌خورند", "de": "Edge-Parameter unsicher sind"}},
                        {"optionId": "b", "text": {"en": "It is copyrighted", "fa": "کپی‌رایت دارد", "de": "Copyright"}},
                        {"optionId": "c", "text": {"en": "It only works for stocks", "fa": "فقط سهام", "de": "nur Aktien"}},
                        {"optionId": "d", "text": {"en": "It requires KYC", "fa": "KYC می‌خواهد", "de": "KYC"}},
                    ],
                    "correct_answer": {"option_id": "a"},
                    "explanation": {
                        "en": "Parameter error + fat tails make full Kelly ruinous; use fractional caps.",
                        "fa": "خطای پارامتر و دم‌های چاق Kelly کامل را مخرب می‌کند؛ fractional سقف‌دار.",
                        "de": "Parameterschätzung + Fat Tails.",
                    },
                    "difficulty": 3,
                    "order": 2,
                },
            ],
        },
        {
            "slug": "drawdown-math",
            "title": "Drawdown Mathematics",
            "description": "Why 50% loss requires 100% gain — and ruin curves.",
            "lesson_type": "theory",
            "order": 3,
            "estimated_minutes": 40,
            "content": {
                "html": """
<h2>Loss asymmetry</h2>
<p>
Recovery multiple: to recover a loss L (as fraction), required gain is
<code>g = L / (1 - L)</code>.
</p>
<ul>
  <li>-10% → +11.1%</li>
  <li>-20% → +25%</li>
  <li>-50% → +100%</li>
  <li>-75% → +300%</li>
</ul>
<p>
This is why professional risk focuses on <em>depth and duration</em> of
drawdown, not only terminal wealth.
</p>

<h3>Maximum drawdown (MDD)</h3>
<p>
MDD = <code>max(1 - equity_t / peak_t)</code> over the path. A strategy
with high return and 60% MDD is not superior for capital that must survive.
</p>

<h3>Worked example: ruin from big bets</h3>
<p>
Two traders, same 55% win rate at 1:1. Trader A risks 2% per trade, B
risks 20%. Path volatility explodes for B; hitting -50% is likely enough
to make recovery psychologically and mathematically brutal. Survival
dominates.
</p>

<h3>Common mistakes</h3>
<ul>
  <li>Chasing max CAGR without MDD constraints.</li>
  <li>Restarting size after drawdown from the old base (should use current equity).</li>
</ul>
""",
            },
            "quizzes": [
                {
                    "question_text": {
                        "en": "To recover a 50% loss you need approximately:",
                        "fa": "برای جبران ضرر ۵۰٪ تقریباً نیاز است:",
                        "de": "Für -50% braucht man ungefähr:",
                    },
                    "question_type": "single_choice",
                    "options": [
                        {"optionId": "a", "text": {"en": "50% gain", "fa": "۵۰٪ سود", "de": "+50%"}},
                        {"optionId": "b", "text": {"en": "100% gain", "fa": "۱۰۰٪ سود", "de": "+100%"}},
                        {"optionId": "c", "text": {"en": "75% gain", "fa": "۷۵٪ سود", "de": "+75%"}},
                        {"optionId": "d", "text": {"en": "10% gain", "fa": "۱۰٪ سود", "de": "+10%"}},
                    ],
                    "correct_answer": {"option_id": "b"},
                    "explanation": {
                        "en": "g = L/(1-L) = 0.5/0.5 = 100%.",
                        "fa": "g = L/(1-L) = ۱۰۰٪.",
                        "de": "g = L/(1-L).",
                    },
                    "difficulty": 2,
                    "order": 1,
                },
                {
                    "question_text": {
                        "en": "Position size after a drawdown should be based on:",
                        "fa": "سایز موقعیت بعد از drawdown باید مبتنی بر:",
                        "de": "Size nach Drawdown basiert auf:",
                    },
                    "question_type": "single_choice",
                    "options": [
                        {"optionId": "a", "text": {"en": "Current equity", "fa": "سرمایه فعلی", "de": "aktuellem Equity"}},
                        {"optionId": "b", "text": {"en": "Peak equity", "fa": "اوج سرمایه", "de": "Peak-Equity"}},
                        {"optionId": "c", "text": {"en": "Last month's PnL", "fa": "سود ماه قبل", "de": "letztem Monat"}},
                        {"optionId": "d", "text": {"en": "Social sentiment", "fa": "سنتیمنت", "de": "Stimmung"}},
                    ],
                    "correct_answer": {"option_id": "a"},
                    "explanation": {
                        "en": "Risk is a fraction of what you have, not what you had.",
                        "fa": "ریسک کسری از دارایی فعلی است نه قبلی.",
                        "de": "Risiko ist Anteil des aktuellen Equity.",
                    },
                    "difficulty": 2,
                    "order": 2,
                },
            ],
        },
        {
            "slug": "risk-of-ruin",
            "title": "Risk of Ruin",
            "description": "When bad size + mediocre edge becomes fatal.",
            "lesson_type": "theory",
            "order": 4,
            "estimated_minutes": 40,
            "content": {
                "html": """
<h2>Ruin is a probability, not a vibe</h2>
<p>
Risk of ruin is the probability of hitting a loss threshold (e.g., -50% or
-100%) given win rate, payoff, and bet size. Larger fraction risk raises
ruin probability even with positive expectancy if tails and variance are
unbounded.
</p>

<h3>Intuition</h3>
<p>
For biased coin-type trades with risk fraction <code>f</code>, path variance
grows with f. Eventually a losing streak meets the ruin boundary. The
relationship is non-linear: doubling f more than doubles ruin risk.
</p>

<h3>Operational policy</h3>
<ul>
  <li>Cap f per trade (e.g., 0.25%–1% for leveraged crypto day trading).</li>
  <li>Cap concurrent open risk (e.g., ≤ 3R total exposure).</li>
  <li>Daily/weekly stop: halt trading at -3R day / -8R week examples.</li>
</ul>

<h3>Worked example</h3>
<p>
Strategy E = +0.2R, but f = 5% of equity per trade in leveraged perps.
A 10-loss streak is not "bad luck" — at 55% win it happens. Equity path
-40%+ creates pressure to oversize. Ruin often arrives via behavior after
drawdown, not one stop-out.
</p>

<h3>Common mistakes</h3>
<ul>
  <li>Confusing positive expectancy with safe sizing.</li>
  <li>Ignoring correlated concurrent positions as one risk.</li>
</ul>
""",
            },
            "quizzes": [
                {
                    "question_text": {
                        "en": "Risk of ruin rises sharply when:",
                        "fa": "risk of ruin وقتی تیز بالا می‌رود که:",
                        "de": "Ruinrisiko steigt stark, wenn:",
                    },
                    "question_type": "single_choice",
                    "options": [
                        {"optionId": "a", "text": {"en": "Bet fraction per trade increases", "fa": "کسر شرط هر معامله زیاد شود", "de": "Einsatzanteil steigt"}},
                        {"optionId": "b", "text": {"en": "You read more news", "fa": "اخبار بیشتر بخوانید", "de": "mehr News"}},
                        {"optionId": "c", "text": {"en": "Spread narrows", "fa": "اسپرد کم شود", "de": "Spread sinkt"}},
                        {"optionId": "d", "text": {"en": "You diversify brokers", "fa": "بروکر متنوع کنید", "de": "Broker diversifizieren"}},
                    ],
                    "correct_answer": {"option_id": "a"},
                    "explanation": {
                        "en": "Path risk is dominated by size fraction.",
                        "fa": "ریسک مسیر با کسر سایز تعیین می‌شود.",
                        "de": "Pfadrisiko hängt an der Size-Fraction.",
                    },
                    "difficulty": 3,
                    "order": 1,
                },
                {
                    "question_text": {
                        "en": "Positive expectancy with 5% risk per trade is:",
                        "fa": "expectancy مثبت با ۵٪ ریسک هر معامله:",
                        "de": "Positiver Erwartungswert mit 5% Risiko ist:",
                    },
                    "question_type": "single_choice",
                    "options": [
                        {"optionId": "a", "text": {"en": "Not automatically safe", "fa": "خودبه‌خود ایمن نیست", "de": "nicht automatisch sicher"}},
                        {"optionId": "b", "text": {"en": "Impossible", "fa": "غیرممکن", "de": "unmöglich"}},
                        {"optionId": "c", "text": {"en": "Guaranteed growth", "fa": "رشد تضمینی", "de": "garantiertes Wachstum"}},
                        {"optionId": "d", "text": {"en": "Only for BTC", "fa": "فقط BTC", "de": "nur BTC"}},
                    ],
                    "correct_answer": {"option_id": "a"},
                    "explanation": {
                        "en": "Expectancy is a mean; ruin is about path and tails.",
                        "fa": "expectancy میانگین است؛ ruin مربوط به مسیر و دم است.",
                        "de": "Erwartungswert ≠ Pfadsicherheit.",
                    },
                    "difficulty": 3,
                    "order": 2,
                },
            ],
        },
        {
            "slug": "correlation-and-portfolio-heat",
            "title": "Correlation and Portfolio Heat",
            "description": "Why five trades can still be one bet.",
            "lesson_type": "theory",
            "order": 4,
            "estimated_minutes": 45,
            "content": {
                "html": """
<h2>Hidden concentration</h2>
<p>
Long BTC, ETH, SOL majors is often one macro bet. Portfolio heat =
aggregate open risk under correlation stress. If each trade is 1R but all
move together, realized portfolio risk can approach 5R in a gap.
</p>

<h3>Simple heat control</h3>
<ul>
  <li>Cap total open R.</li>
  <li>Reduce size when pairwise 30d correlation &gt; threshold (e.g., 0.7).</li>
  <li>Treat same-direction correlated cluster as one trade for heat purposes.</li>
</ul>

<h3>Correlation is unstable</h3>
<p>
Crypto cross-asset correlations often jump toward 1 in liquidations. Use
stress correlation (crisis windows), not only calm-sample averages.
</p>

<h3>Worked example</h3>
<p>
Four longs: BTC, ETH, high-beta L1, meme beta. Calm correlations 0.4–0.8.
In a flush all dump with beta &gt; 1. Heat plan should have assumed
correlation → 0.9–1.0. If not, stop clustering turns 4R planned into 8R+
realized.
</p>
""",
            },
            "quizzes": [
                {
                    "question_text": {
                        "en": "Five highly correlated longs should be treated roughly as:",
                        "fa": "پنج لانگ با همبستگی بالا تقریباً باید دیده شوند به‌عنوان:",
                        "de": "Fünf korrelierte Longs sind ungefähr:",
                    },
                    "question_type": "single_choice",
                    "options": [
                        {"optionId": "a", "text": {"en": "One larger clustered exposure", "fa": "یک افشای خوشه‌ای بزرگ‌تر", "de": "eine größere Klumpenposition"}},
                        {"optionId": "b", "text": {"en": "Full diversification", "fa": "تنوع کامل", "de": "volle Diversifikation"}},
                        {"optionId": "c", "text": {"en": "Risk-free", "fa": "بدون ریسک", "de": "risikofrei"}},
                        {"optionId": "d", "text": {"en": "Five independent coins", "fa": "پنج مستقل", "de": "unabhängig"}},
                    ],
                    "correct_answer": {"option_id": "a"},
                    "explanation": {
                        "en": "Correlation collapses diversification benefits in stress.",
                        "fa": "همبستگی مزیت تنوع را در تنش از بین می‌برد.",
                        "de": "Korrelation frisst Diversifikation.",
                    },
                    "difficulty": 3,
                    "order": 1,
                },
            ],
        },
        {
            "slug": "var-expected-shortfall",
            "title": "VaR and Expected Shortfall for Traders",
            "description": "Tail metrics that size desks actually use.",
            "lesson_type": "theory",
            "order": 6,
            "estimated_minutes": 45,
            "content": {
                "html": """
<h2>VaR</h2>
<p>
Value at Risk at level α (e.g., 95%) is the loss threshold exceeded with
probability 1−α over horizon T:
<code>P(Loss &gt; VaR) = 1 - α</code>.
If 1-day 95% VaR = $2,000, you expect worse than that on ~1 day in 20 —
not "maximum loss".
</p>

<h2>Expected Shortfall (CVaR)</h2>
<p>
ES is the average loss conditional on exceeding VaR:
<code>ES = E[Loss | Loss &gt; VaR]</code>.
ES answers "when it is bad, how bad on average?" — preferred for fat tails.
</p>

<h3>Use in a trading stack</h3>
<ul>
  <li>Portfolio VaR caps notional/leverage.</li>
  <li>ES used to stress leveraged books in crypto.</li>
  <li>Always combine with scenario gaps (VaR models miss discontinuous liquidation cascades).</li>
</ul>

<h3>Worked example</h3>
<p>
PnL distribution: 95% VaR $2k, ES $4.5k. Risk budget says daily stop at
$3k is inside the tail average — meaning on tail days the stop may slip.
Therefore size so stop slippage still keeps ES under policy max.
</p>

<h3>Common mistakes</h3>
<ul>
  <li>Treating VaR as worst case.</li>
  <li>Gaussian assumptions on crypto PnL with liquidation jumps.</li>
</ul>
""",
            },
            "quizzes": [
                {
                    "question_text": {
                        "en": "95% daily VaR = $2,000 means:",
                        "fa": "VaR روزانه ۹۵٪ برابر ۲۰۰۰ یعنی:",
                        "de": "95% VaR = $2.000 bedeutet:",
                    },
                    "question_type": "single_choice",
                    "options": [
                        {"optionId": "a", "text": {"en": "Worse loss than $2k happens about 5% of days", "fa": "ضرر بدتر از ۲k حدود ۵٪ روزها رخ می‌دهد", "de": "Schlimmer als $2k an ~5% der Tage"}},
                        {"optionId": "b", "text": {"en": "Max loss is $2k", "fa": "حداکثر ضرر ۲k", "de": "Maxverlust $2k"}},
                        {"optionId": "c", "text": {"en": "Expected profit is $2k", "fa": "سود مورد انتظار ۲k", "de": "Erwarteter Gewinn"}},
                        {"optionId": "d", "text": {"en": "Fees are $2k", "fa": "کارمزد ۲k", "de": "Gebühren"}},
                    ],
                    "correct_answer": {"option_id": "a"},
                    "explanation": {
                        "en": "VaR is a quantile, not a maximum.",
                        "fa": "VaR چندک است نه ماکزیمم.",
                        "de": "VaR ist ein Quantil.",
                    },
                    "difficulty": 3,
                    "order": 1,
                },
                {
                    "question_text": {
                        "en": "Expected Shortfall is better than VaR for fat tails because it:",
                        "fa": "Expected Shortfall برای دم‌های چاق بهتر از VaR است زیرا:",
                        "de": "Expected Shortfall ist bei Fat Tails besser, weil:",
                    },
                    "question_type": "single_choice",
                    "options": [
                        {"optionId": "a", "text": {"en": "Averages losses beyond the quantile", "fa": "میانگین ضررهای فراتر از چندک را می‌گیرد", "de": "Verluste jenseits des Quantils mittelt"}},
                        {"optionId": "b", "text": {"en": "Is always smaller", "fa": "همیشه کوچک‌تر است", "de": "immer kleiner"}},
                        {"optionId": "c", "text": {"en": "Needs no data", "fa": "داده نمی‌خواهد", "de": "keine Daten"}},
                        {"optionId": "d", "text": {"en": "Predicts direction", "fa": "جهت می‌گوید", "de": "Richtung sagt"}},
                    ],
                    "correct_answer": {"option_id": "a"},
                    "explanation": {
                        "en": "ES conditions on the tail and describes severity.",
                        "fa": "ES روی دم شرطی می‌شود و شدت را توصیف می‌کند.",
                        "de": "ES beschreibt Tail-Schwere.",
                    },
                    "difficulty": 3,
                    "order": 2,
                },
            ],
        },
        {
            "slug": "stops-and-exit-policy",
            "title": "Stops and Exit Policy",
            "description": "Where stops belong, and how exits create payoff edge.",
            "lesson_type": "practice",
            "order": 7,
            "estimated_minutes": 45,
            "content": {
                "html": """
<h2>Stop placement is risk design</h2>
<p>
A stop answers: "what price proves the idea wrong?" Not "what price feels
uncomfortable?" Place it beyond structural invalidation, then size to risk
budget. If the structural stop is too far, skip or size smaller — do not
fake a tighter stop.
</p>

<h3>Exit hierarchy</h3>
<ul>
  <li><strong>Invalidation stop:</strong> hard risk boundary.</li>
  <li><strong>Scale-out:</strong> take partial at 1R/2R to cut variance.</li>
  <li><strong>Trail:</strong> lock profit under higher lows / ATR band.</li>
  <li><strong>Time stop:</strong> exit if thesis stalls (opportunity cost).</li>
</ul>

<h3>Worked example policy</h3>
<p>
Long after breakout retest: stop below retest low (structure). Size 0.6%
risk. At +1.5R sell 40%. Trail rest under 1h higher lows or 2×ATR. Hard
stop never widens after entry. Ever.
</p>

<h3>Common mistakes</h3>
<ul>
  <li>Widening stops under stress.</li>
  <li>No profit-taking plan (all-or-nothing outs).</li>
  <li>Using round-number stops inside liquidity pools.</li>
</ul>
""",
            },
            "quizzes": [
                {
                    "question_text": {
                        "en": "If structural stop distance implies too much risk, correct action is to:",
                        "fa": "اگر فاصله استاپ ساختاری ریسک زیادی دارد، اقدام درست:",
                        "de": "Wenn der Struktur-Stop zu viel Risiko impliziert:",
                    },
                    "question_type": "single_choice",
                    "options": [
                        {"optionId": "a", "text": {"en": "Move stop closer to reduce size pain", "fa": "نزدیک کردن استاپ", "de": "Stop näher setzen"}},
                        {"optionId": "b", "text": {"en": "Reduce size or skip the trade", "fa": "کاهش سایز یا رد معامله", "de": "Size senken oder Skip"}},
                        {"optionId": "c", "text": {"en": "Increase leverage", "fa": "افزایش اهرم", "de": "Hebel erhöhen"}},
                        {"optionId": "d", "text": {"en": "Remove stop", "fa": "حذف استاپ", "de": "Stop entfernen"}},
                    ],
                    "correct_answer": {"option_id": "b"},
                    "explanation": {
                        "en": "Size is the flexible variable; structural invalidation is not.",
                        "fa": "سایز متغیر منعطف است؛ حد باطل ساختاری نه.",
                        "de": "Size ist flexibel, Struktur nicht.",
                    },
                    "difficulty": 3,
                    "order": 1,
                },
                {
                    "question_text": {
                        "en": "After entry, widening a hard stop is:",
                        "fa": "بعد از ورود، باز کردن استاپ سخت:",
                        "de": "Stop nach Entry ausweiten ist:",
                    },
                    "question_type": "single_choice",
                    "options": [
                        {"optionId": "a", "text": {"en": "A plan violation that increases risk", "fa": "نقض طرح و افزایش ریسک", "de": "Planverletzung mit mehr Risiko"}},
                        {"optionId": "b", "text": {"en": "Good risk management", "fa": "مدیریت ریسک خوب", "de": "gutes Risikomanagement"}},
                        {"optionId": "c", "text": {"en": "Tax optimization", "fa": "بهینه مالیات", "de": "Steuer"}},
                        {"optionId": "d", "text": {"en": "A hedge", "fa": "هج", "de": "Hedge"}},
                    ],
                    "correct_answer": {"option_id": "a"},
                    "explanation": {
                        "en": "Risk was defined at entry; widening breaks the unit R.",
                        "fa": "ریسک هنگام ورود تعریف شده؛ باز کردن R را خراب می‌کند.",
                        "de": "Risiko war definiert.",
                    },
                    "difficulty": 2,
                    "order": 2,
                },
            ],
        },
        {
            "slug": "risk-operating-system",
            "title": "Personal Risk Operating System",
            "description": "Daily loss limits, concurrency caps, and kill criteria.",
            "lesson_type": "practice",
            "order": 8,
            "estimated_minutes": 40,
            "content": {
                "html": """
<h2>Risk is an operating system</h2>
<p>
Policies convert intention into defaults under stress. Minimum viable
personal risk OS:
</p>
<ul>
  <li><strong>Per-trade:</strong> 0.25–1% capital at risk example band.</li>
  <li><strong>Concurrent:</strong> max open risk 2–3R.</li>
  <li><strong>Daily stop:</strong> e.g., -3R or -1.5% → done for day.</li>
  <li><strong>Weekly stop:</strong> e.g., -8R → review system, size down.</li>
  <li><strong>Mistake budget:</strong> two rule breaks → mandatory off platform 24h.</li>
</ul>

<h3>Why daily stops matter</h3>
<p>
Tilt is path-dependent. A hard stop on the session caps behavioral
ruin even when statistical ruin is modest.
</p>

<h3>Worked checklist before entry</h3>
<ol>
  <li>What is my R?</li>
  <li>Is total heat within cap?</li>
  <li>Am I within daily/weekly loss budget?</li>
  <li>Does entry match written setup?</li>
  <li>If any answer is no → no trade.</li>
</ol>

<h3>Common mistakes</h3>
<ul>
  <li>Rules that only exist on green days.</li>
  <li>Changing risk OS mid-drawdown to "make it back".</li>
</ul>
""",
            },
            "quizzes": [
                {
                    "question_text": {
                        "en": "A daily loss stop exists mainly to limit:",
                        "fa": "استاپ ضرر روزانه عمدتاً برای محدود کردن چیست؟",
                        "de": "Tagesverlust-Limit begrenzt primär:",
                    },
                    "question_type": "single_choice",
                    "options": [
                        {"optionId": "a", "text": {"en": "Behavioral ruin / tilt spirals", "fa": "ویرانی رفتاری / مارپیچ tilt", "de": "Verhaltensruin"}},
                        {"optionId": "b", "text": {"en": "Exchange fees", "fa": "کارمزد صرافی", "de": "Gebühren"}},
                        {"optionId": "c", "text": {"en": "Tax", "fa": "مالیات", "de": "Steuer"}},
                        {"optionId": "d", "text": {"en": "Latency", "fa": "تأخیر", "de": "Latenz"}},
                    ],
                    "correct_answer": {"option_id": "a"},
                    "explanation": {
                        "en": "Session hard stops cap revenge trading and oversizing.",
                        "fa": "استاپ سخت سشن جلوی revenge trading و oversize را می‌گیرد.",
                        "de": "Harte Tagesstops bremsen Tilt.",
                    },
                    "difficulty": 2,
                    "order": 1,
                },
                {
                    "question_text": {
                        "en": "Two rule breaks in a session should trigger:",
                        "fa": "دو نقض قاعده در یک سشن باید فعال کند:",
                        "de": "Zwei Regelverstöße führen zu:",
                    },
                    "question_type": "single_choice",
                    "options": [
                        {"optionId": "a", "text": {"en": "Larger size to recover", "fa": "سایز بزرگ‌تر برای جبران", "de": "größerer Size"}},
                        {"optionId": "b", "text": {"en": "Mandatory time off platform", "fa": "اجبار به دوری از پلتفرم", "de": "Pflichtpause"}},
                        {"optionId": "c", "text": {"en": "Ignoring journal", "fa": "نادیده گرفتن ژورنال", "de": "Journal ignorieren"}},
                        {"optionId": "d", "text": {"en": "New random system", "fa": "سیستم تصادفی جدید", "de": "Zufallssystem"}},
                    ],
                    "correct_answer": {"option_id": "b"},
                    "explanation": {
                        "en": "Mistake budgets protect process integrity when ego is loud.",
                        "fa": "بودجه خطا وقتی احساسات بلند است از فرایند محافظت می‌کند.",
                        "de": "Fehlerbudget schützt den Prozess.",
                    },
                    "difficulty": 3,
                    "order": 2,
                },
            ],
        },
    ],
}
