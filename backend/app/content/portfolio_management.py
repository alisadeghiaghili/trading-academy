"""Portfolio Management module.

Benchmark depth: Markowitz/CFA portfolio construction essentials applied to
multi-asset crypto books. Target: 6 deep lessons.
"""

from __future__ import annotations

from typing import Any


PORTFOLIO_MANAGEMENT: dict[str, Any] = {
    "slug": "portfolio-management",
    "title": "Portfolio Management",
    "description": (
        "Diversification math, correlation and risk budgeting, rebalancing, "
        "factor exposure, performance attribution, and IPS-style policy."
    ),
    "order": 5,
    "required_tier": "pro",
    "lessons": [
        {
            "slug": "diversification-math",
            "title": "Diversification Mathematics",
            "description": "Why 8 correlated coins are not diversification.",
            "lesson_type": "theory",
            "order": 1,
            "estimated_minutes": 45,
            "content": {
                "html": """
<h2>Portfolio variance</h2>
<p>
For two assets:
<code>σp² = w1²σ1² + w2²σ2² + 2w1w2ρσ1σ2</code>.
Diversification benefit is the correlation term. If ρ → 1, benefit vanishes.
</p>

<h3>Crypto reality</h3>
<p>
In calm regimes BTC/ETH/high-beta show moderate correlation. In
liquidation cascades ρ jumps toward 1 and beta to BTC rises. Plan for
stress correlation, not average correlation.
</p>

<h3>Worked example</h3>
<p>
Equal weights A,B each σ=60%. If ρ=0.3:
σp ≈ sqrt(0.5²·0.6²·2 + 2·0.5·0.5·0.3·0.6·0.6) ≈ 45%.
If ρ=0.9, σp ≈ 57%. Same assets, different crisis reality.
</p>

<h3>Common mistakes</h3>
<ul>
  <li>Counting many alts as diversification vs BTC beta.</li>
  <li>Using full-sample correlation.</li>
</ul>
""",
            },
            "quizzes": [
                {
                    "question_text": {
                        "en": "If pairwise correlation goes to 1 in stress, diversification benefit:",
                        "fa": "اگر همبستگی در تنش به ۱ برسد، مزیت تنوع:",
                        "de": "Bei ρ→1 im Stress sinkt der Diversifikationsnutzen:",
                    },
                    "question_type": "single_choice",
                    "options": [
                        {"optionId": "a", "text": {"en": "Collapses", "fa": "فرو می‌ریزد", "de": "kollabiert"}},
                        {"optionId": "b", "text": {"en": "Doubles", "fa": "دو برابر می‌شود", "de": "verdoppelt"}},
                        {"optionId": "c", "text": {"en": "Stays constant", "fa": "ثابت می‌ماند", "de": "bleibt"}},
                        {"optionId": "d", "text": {"en": "Becomes risk-free", "fa": "بدون ریسک می‌شود", "de": "risikofrei"}},
                    ],
                    "correct_answer": {"option_id": "a"},
                    "explanation": {
                        "en": "Correlation is the engine of diversification.",
                        "fa": "همبستگی موتور تنوع است.",
                        "de": "Korrelation steuert Diversifikation.",
                    },
                    "difficulty": 2,
                    "order": 1,
                },
            ],
        },
        {
            "slug": "risk-budgeting",
            "title": "Risk Budgeting Across Positions",
            "description": "Allocate risk units, not just dollars.",
            "lesson_type": "practice",
            "order": 2,
            "estimated_minutes": 45,
            "content": {
                "html": """
<h2>Budget in risk units</h2>
<p>
Give the book a total risk budget (e.g., 6R max open). Allocate R to
themes: majors beta, relative-value, event risk. Position size then
follows stop distance and remaining heat.
</p>

<h3>Example budget</h3>
<ul>
  <li>Beta bucket (BTC/ETH): max 3R.</li>
  <li>Alt directional: max 2R.</li>
  <li>Event/unlock plays: max 1R.</li>
</ul>
<p>
If an alt signal appears while beta bucket is full, it does not get
crowbarred in. Skip or shrink.
</p>

<h3>Worked example</h3>
<p>
Equity $100k, policy 0.5% per trade risk = $500 = 1R. Max 3 concurrent →
max open risk $1,500 plus correlation discount. High-beta cluster counts
as 1.5 slots when 30d ρ &gt; 0.8.
</p>
""",
            },
            "quizzes": [
                {
                    "question_text": {
                        "en": "Risk budgeting primarily allocates:",
                        "fa": "ریسک بودجه‌ریزی عمدتاً تخصیص می‌دهد:",
                        "de": "Risikobudgeting allokiert primär:",
                    },
                    "question_type": "single_choice",
                    "options": [
                        {"optionId": "a", "text": {"en": "Units of risk across themes/positions", "fa": "واحدهای ریسک بین تم‌ها/موقعیت‌ها", "de": "Risikoeinheiten"}},
                        {"optionId": "b", "text": {"en": "Only dollars", "fa": "فقط دلار", "de": "nur Dollar"}},
                        {"optionId": "c", "text": {"en": "Screen time", "fa": "زمان نمایشگر", "de": "Screenzeit"}},
                        {"optionId": "d", "text": {"en": "Indicator slots", "fa": "جای اندیکاتور", "de": "Indikatorplätze"}},
                    ],
                    "correct_answer": {"option_id": "a"},
                    "explanation": {
                        "en": "Dollars differ in risk; R-normalized budgets do not.",
                        "fa": "دلارها ریسک متفاوت دارند؛ بودجه R-normalized نه.",
                        "de": "Budget in Risikoeinheiten.",
                    },
                    "difficulty": 3,
                    "order": 1,
                },
            ],
        },
        {
            "slug": "rebalancing-rules",
            "title": "Rebalancing Rules",
            "description": "Calendar, threshold, and hybrid policies.",
            "lesson_type": "theory",
            "order": 3,
            "estimated_minutes": 40,
            "content": {
                "html": """
<h2>Policy beats improvisation</h2>
<ul>
  <li><strong>Calendar:</strong> rebalance weekly/monthly regardless of drift.</li>
  <li><strong>Threshold:</strong> rebalance when weight drifts ±x%.</li>
  <li><strong>Hybrid:</strong> check monthly, act on threshold.</li>
</ul>
<p>
Rebalancing systematically sells winners and buys losers relative to
targets — a mean-reversion tax or a discipline benefit depending on regime.
Write the rule before the bull market.
</p>

<h3>Costs</h3>
<p>
Include fees, spread, tax lots, and slippage. Thresholds too tight bleed
costs; too loose recreate concentration.
</p>

<h3>Worked example</h3>
<p>
Targets 70% BTC / 30% ETH. Drift to 80/20. Threshold ±5% absolute →
rebalance back to 70/30. If only +2% drift, do nothing even if calendar
fires.
</p>
""",
            },
            "quizzes": [
                {
                    "question_text": {
                        "en": "A threshold rebalancing rule acts when:",
                        "fa": "قاعده rebalancing آستانه‌ای عمل می‌کند وقتی:",
                        "de": "Threshold-Rebalancing agiert, wenn:",
                    },
                    "question_type": "single_choice",
                    "options": [
                        {"optionId": "a", "text": {"en": "Weights drift beyond the band", "fa": "وزن‌ها از باند خارج شوند", "de": "Gewichte außerhalb der Bandbreite"}},
                        {"optionId": "b", "text": {"en": "Social sentiment spikes", "fa": "سنتیمنت جهش کند", "de": "Stimmung"}},
                        {"optionId": "c", "text": {"en": "Any red candle appears", "fa": "هر کندل قرمز", "de": "rote Kerze"}},
                        {"optionId": "d", "text": {"en": "Only at year end", "fa": "فقط آخر سال", "de": "nur Jahresende"}},
                    ],
                    "correct_answer": {"option_id": "a"},
                    "explanation": {
                        "en": "Threshold rules are event-driven by drift.",
                        "fa": "قاعده آستانه با drift رویدادمحور است.",
                        "de": "Schwellenregeln folgen Drift.",
                    },
                    "difficulty": 2,
                    "order": 1,
                },
            ],
        },
        {
            "slug": "factor-exposure",
            "title": "Factor Exposure in Crypto Books",
            "description": "Beta, momentum, size, and narrative factors.",
            "lesson_type": "theory",
            "order": 4,
            "estimated_minutes": 45,
            "content": {
                "html": """
<h2>You own factors even if unnamed</h2>
<p>
A long book of alts is typically: BTC beta + size factor (small caps) +
momentum + narrative beta (AI, memes, L2). When factor winds reverse, idio
selection cannot always save the book.
</p>

<h3>Practical map</h3>
<ul>
  <li><strong>Market beta:</strong> BTC/ETH core.</li>
  <li><strong>Size:</strong> high-beta small caps draw down more in risk-off.</li>
  <li><strong>Momentum:</strong> winners continue until crowded unwind.</li>
  <li><strong>Narrative:</strong> theme baskets with high pairwise ρ inside theme.</li>
</ul>

<h3>Worked example</h3>
<p>
Portfolio: 60% BTC, 40% basket of 8 AI tokens. You think you are
diversified (9 names). Factor view: you are ~2 bets (BTC beta + AI
narrative). Size and stop policy should reflect 2 bets, not 9.
</p>
""",
            },
            "quizzes": [
                {
                    "question_text": {
                        "en": "Eight tokens from one narrative theme mainly load on:",
                        "fa": "هشت توکن از یک تم روایی عمدتاً روی چه بارگذاری دارند؟",
                        "de": "Acht Tokens einer Narrative laden primär auf:",
                    },
                    "question_type": "single_choice",
                    "options": [
                        {"optionId": "a", "text": {"en": "A shared narrative factor", "fa": "یک فاکتور روایی مشترک", "de": "einen gemeinsamen Faktor"}},
                        {"optionId": "b", "text": {"en": "Independent risks", "fa": "ریسک مستقل", "de": "unabhängige Risiken"}},
                        {"optionId": "c", "text": {"en": "Risk-free rate", "fa": "نرخ بدون ریسک", "de": "risikofreien Zins"}},
                        {"optionId": "d", "text": {"en": "Only tokenomics", "fa": "فقط توکنومیکس", "de": "nur Tokenomics"}},
                    ],
                    "correct_answer": {"option_id": "a"},
                    "explanation": {
                        "en": "Theme baskets are concentrated factor bets.",
                        "fa": "سبک‌های تم، شرط فاکتور متمرکزند.",
                        "de": "Themen-Portfolios sind Faktorwetten.",
                    },
                    "difficulty": 3,
                    "order": 1,
                },
            ],
        },
        {
            "slug": "performance-attribution",
            "title": "Performance Attribution and Review",
            "description": "Know whether returns came from skill or beta.",
            "lesson_type": "practice",
            "order": 5,
            "estimated_minutes": 45,
            "content": {
                "html": """
<h2>Decompose the curve</h2>
<ul>
  <li><strong>Beta contribution:</strong> exposure × market return.</li>
  <li><strong>Selection:</strong> residual after beta.</li>
  <li><strong>Costs:</strong> fees, funding, slippage as negative alpha line items.</li>
</ul>
<p>
If +40% quarter equals BTC +38% with higher vol and costs, process skill
is not proven. Attribution kills lucky narratives.
</p>

<h3>Review cadence</h3>
<ul>
  <li>Weekly: risk budget adherence, mistake count.</li>
  <li>Monthly: R distribution, factor buckets.</li>
  <li>Quarterly: system E[R], cost drag, rule changes only here.</li>
</ul>

<h3>Worked example</h3>
<p>
Book +12% month. BTC +10%, alts beta +2.5%, selection −0.8%, costs −0.3%.
Truth: mostly beta. Next month's plan should not size up "stock picking"
because of a beta rally.
</p>
""",
            },
            "quizzes": [
                {
                    "question_text": {
                        "en": "If portfolio return ≈ BTC return with higher risk, most performance is:",
                        "fa": "اگر بازده پرتفوی ≈ بازده BTC با ریسک بالاتر باشد، بیشتر عملکرد:",
                        "de": "Wenn Portfolio ≈ BTC mit mehr Risiko, ist die Performance primär:",
                    },
                    "question_type": "single_choice",
                    "options": [
                        {"optionId": "a", "text": {"en": "Beta, not selection skill", "fa": "بتا، نه مهارت انتخاب", "de": "Beta"}},
                        {"optionId": "b", "text": {"en": "Alpha from genius entries", "fa": "آلفای ورود نابغه", "de": "Alpha"}},
                        {"optionId": "c", "text": {"en": "Risk-free excess", "fa": "مازاد بدون ریسک", "de": "risikofrei"}},
                        {"optionId": "d", "text": {"en": "Fee savings", "fa": "صرفه‌جویی کارمزد", "de": "Gebühren"}},
                    ],
                    "correct_answer": {"option_id": "a"},
                    "explanation": {
                        "en": "Attribution separates market tide from selection.",
                        "fa": "attribution جزر و مد بازار را از انتخاب جدا می‌کند.",
                        "de": "Attribution trennt Beta und Selektion.",
                    },
                    "difficulty": 3,
                    "order": 1,
                },
            ],
        },
        {
            "slug": "ips-policy",
            "title": "Investment Policy Statement for a Personal Book",
            "description": "Lock objectives, constraints, and procedures.",
            "lesson_type": "practice",
            "order": 6,
            "estimated_minutes": 40,
            "content": {
                "html": """
<h2>IPS = constitution</h2>
<p>
One page personal IPS:
</p>
<ul>
  <li><strong>Objectives:</strong> target return band, max acceptable drawdown.</li>
  <li><strong>Constraints:</strong> liquidity needs, leverage cap, concentration caps, tax.</li>
  <li><strong>Procedures:</strong> sizing, rebalancing, kill rules, review calendar.</li>
</ul>

<h3>Why it works</h3>
<p>
Under stress, people renegotiate with themselves. An IPS forces renegotiation
to happen on a calm calendar, not at 3am during a flush.
</p>

<h3>Worked example clause</h3>
<p>
"Max leverage 2× on core beta only. No position &gt; 15% notional without
written memo. Weekly rebalance band ±5%. Mandatory 24h lockout after two
rule breaks."
</p>
""",
            },
            "quizzes": [
                {
                    "question_text": {
                        "en": "An IPS is most valuable because it:",
                        "fa": "IPS ارزشمند است زیرا:",
                        "de": "Ein IPS ist wertvoll, weil:",
                    },
                    "question_type": "single_choice",
                    "options": [
                        {"optionId": "a", "text": {"en": "Pre-commits rules before stress", "fa": "قاعده را قبل از تنش قفل می‌کند", "de": "Regeln vor Stress vorab festlegt"}},
                        {"optionId": "b", "text": {"en": "Predicts price", "fa": "قیمت پیش‌بینی می‌کند", "de": "Preis sagt"}},
                        {"optionId": "c", "text": {"en": "Removes fees", "fa": "کارمزد حذف می‌کند", "de": "Fees"}},
                        {"optionId": "d", "text": {"en": "Guarantees alpha", "fa": "آلفا تضمین می‌کند", "de": "Alpha garantiert"}},
                    ],
                    "correct_answer": {"option_id": "a"},
                    "explanation": {
                        "en": "Pre-commitment is the behavioral core of risk management.",
                        "fa": "پیش‌تعهد هسته رفتاری مدیریت ریسک است.",
                        "de": "Vorab-Festlegung ist Kern.",
                    },
                    "difficulty": 2,
                    "order": 1,
                },
            ],
        },
    ],
}
