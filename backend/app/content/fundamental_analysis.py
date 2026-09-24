"""Fundamental Analysis module.

Benchmark depth: CFA equity research process adapted to crypto tokenomics +
Messari-style on-chain/valuation hygiene. Target: 6 deep lessons.
"""

from __future__ import annotations

from typing import Any


FUNDAMENTAL_ANALYSIS: dict[str, Any] = {
    "slug": "fundamental-analysis",
    "title": "Fundamental Analysis",
    "description": (
        "Research process, tokenomics and unlocks, on-chain and network "
        "metrics, valuation frameworks, team/vesting diligence, and risk memos."
    ),
    "order": 4,
    "required_tier": "pro",
    "lessons": [
        {
            "slug": "research-process",
            "title": "Research Process and Thesis Discipline",
            "description": "How professional research avoids narrative capture.",
            "lesson_type": "theory",
            "order": 1,
            "estimated_minutes": 45,
            "content": {
                "html": """
<h2>Research is a pipeline</h2>
<p>
Fundamental work without a pipeline becomes story collection. A usable
process:
</p>
<ol>
  <li><strong>Question:</strong> what claim are we underwriting (adoption, fees, store of value)?</li>
  <li><strong>Evidence map:</strong> on-chain, financials/fees, competitive set, supply schedule.</li>
  <li><strong>Falsifiers:</strong> what would kill the thesis in 3–6 months?</li>
  <li><strong>Position link:</strong> how does thesis map to entry/invalidation/size?</li>
</ol>

<h3>Primary vs secondary sources</h3>
<ul>
  <li>Primary: protocol docs, unlock schedules on-chain, audited contracts, fee dashboards with methodology.</li>
  <li>Secondary: threads, rankings sites, influencer models (use as leads only).</li>
</ul>

<h3>Worked example thesis card</h3>
<p>
Claim: "Fee capture will grow with L2 activity and burn supports real
yield." Evidence needed: fee accrual mechanics, burn vs issuance, growth in
paid calls (not just TVL), competitor fee share. Falsifier: fees up 3x but
token sinks hollowed by insider unlocks.
</p>

<h3>Common mistakes</h3>
<ul>
  <li>Falling in love with narrative before supply math.</li>
  <li>Using TVL alone as adoption proof.</li>
  <li>Never writing falsifiers.</li>
</ul>
""",
            },
            "quizzes": [
                {
                    "question_text": {
                        "en": "A research thesis is incomplete without:",
                        "fa": "پایان‌نامه تحقیق بدون چه ناقص است؟",
                        "de": "Eine These ist unvollständig ohne:",
                    },
                    "question_type": "single_choice",
                    "options": [
                        {"optionId": "a", "text": {"en": "Falsifiers and evidence map", "fa": "falsifier و نقشه شواهد", "de": "Falsifizierer und Evidenz"}},
                        {"optionId": "b", "text": {"en": "Price target screenshot", "fa": "اسکرین‌شات تارگت", "de": "Zielpreis-Screenshot"}},
                        {"optionId": "c", "text": {"en": "Celebrity endorsement", "fa": "تایید سلبریتی", "de": "Promi"}},
                        {"optionId": "d", "text": {"en": "Complex roadmap PDF", "fa": "PDF نقشه راه پیچیده", "de": "Roadmap-PDF"}},
                    ],
                    "correct_answer": {"option_id": "a"},
                    "explanation": {
                        "en": "Falsifiers make a thesis testable instead of religious.",
                        "fa": "falsifier پایان‌نامه را آزمودنی می‌کند نه مسلکی.",
                        "de": "Falsifizierer machen Thesen testbar.",
                    },
                    "difficulty": 3,
                    "order": 1,
                },
            ],
        },
        {
            "slug": "tokenomics-unlocks",
            "title": "Tokenomics: Unlocks, Emissions, Value Accrual",
            "description": "The supply side that destroys most 'fundamental' stories.",
            "lesson_type": "theory",
            "order": 2,
            "estimated_minutes": 55,
            "content": {
                "html": """
<h2>Supply is a cash-flow story</h2>
<p>
Token price is claim on future scarce units + services. If unit supply
grows faster than demand for services/stores, price pressure is mechanical.
Never stop at "max supply". Always build a float schedule.
</p>

<h3>Float schedule template</h3>
<ul>
  <li>TGE float %.</li>
  <li>Cliff dates and linear unlocks (team, investors, ecosystem, foundation).</li>
  <li>Emissions (inflation) and sinks (burns, locks).</li>
  <li>Vote-escrow or staking that temporarily restrains float.</li>
</ul>

<h3>Value accrual mechanisms</h3>
<table>
  <tr><th>Mechanism</th><th>What holders receive</th><th>Risk</th></tr>
  <tr><td>Fee switch / buyback</td><td>Cash-flow-like</td><td>Governance can turn off</td></tr>
  <tr><td>Burn on usage</td><td>Scarcity if usage real</td><td>Wash usage, hollow burns</td></tr>
  <tr><td>Work token / staking</td><td>Right to serve + rewards</td><td>Dilution if rewards &gt; real fees</td></tr>
  <tr><td>Governance only</td><td>Control premium</td><td>Often weak claim on value</td></tr>
</table>

<h3>Worked example</h3>
<p>
Circulating 20M / max 100M. Next 12 months: +15M unlocks, +10M emissions,
staking removes 5M temporarily. Net tradable supply +20M (+100% float)
even if max supply story is "fixed". Price support requires demand growth
absorbing that.
</p>

<h3>Common mistakes</h3>
<ul>
  <li>FDV optimism without unlock math.</li>
  <li>Counting burn without verifying organic usage.</li>
  <li>Ignoring insider cost basis vs your entry.</li>
</ul>
""",
            },
            "quizzes": [
                {
                    "question_text": {
                        "en": "Best first step in tokenomics diligence:",
                        "fa": "بهترین قدم اول در diligence توکنومیکس:",
                        "de": "Erster Schritt Tokenomics:",
                    },
                    "question_type": "single_choice",
                    "options": [
                        {"optionId": "a", "text": {"en": "Build a circulating float unlock schedule", "fa": "ساخت زمان‌بندی unlock عرضه در گردش", "de": "Float-Unlock-Plan"}},
                        {"optionId": "b", "text": {"en": "Read the logo design", "fa": "طراحی لوگو", "de": "Logo"}},
                        {"optionId": "c", "text": {"en": "Check Discord emoji count", "fa": "تعداد ایموجی دیسکورد", "de": "Discord"}},
                        {"optionId": "d", "text": {"en": "Max supply only", "fa": "فقط سقف عرضه", "de": "nur Max Supply"}},
                    ],
                    "correct_answer": {"option_id": "a"},
                    "explanation": {
                        "en": "Tradable scarcity is governed by float path, not slogans.",
                        "fa": "کمیابی قابل‌معامله با مسیر float تعیین می‌شود.",
                        "de": "Maßgeblich ist der Float-Pfad.",
                    },
                    "difficulty": 3,
                    "order": 1,
                },
                {
                    "question_text": {
                        "en": "A 'buyback and burn' is weak if:",
                        "fa": "«بای‌بک و سوزاندن» ضعیف است اگر:",
                        "de": "Buyback/Burn ist schwach, wenn:",
                    },
                    "question_type": "single_choice",
                    "options": [
                        {"optionId": "a", "text": {"en": "Usage is fake and unlocks dominate supply", "fa": "کاربرد جعلی و unlock بر عرضه مسلط است", "de": "Nutzung fake und Unlocks dominieren"}},
                        {"optionId": "b", "text": {"en": "Logo is blue", "fa": "لوگو آبی است", "de": "Logo blau"}},
                        {"optionId": "c", "text": {"en": "Fees are low", "fa": "کارمزد کم است", "de": "Fees gering"}},
                        {"optionId": "d", "text": {"en": "It is on a new chain", "fa": "روی زنجیره جدید است", "de": "neue Chain"}},
                    ],
                    "correct_answer": {"option_id": "a"},
                    "explanation": {
                        "en": "Sinks cannot outrun inorganic supply and hollow volume.",
                        "fa": "sink نمی‌تواند بر عرضه غیرارگانیک و حجم توخالی غلبه کند.",
                        "de": "Sink verliert gegen hohles Angebot.",
                    },
                    "difficulty": 3,
                    "order": 2,
                },
            ],
        },
        {
            "slug": "onchain-metrics",
            "title": "On-chain and Network Metrics",
            "description": "Activity quality beyond vanity charts.",
            "lesson_type": "theory",
            "order": 3,
            "estimated_minutes": 50,
            "content": {
                "html": """
<h2>Measure usage quality</h2>
<ul>
  <li><strong>Active addresses / entities:</strong> demand proxies (watch Sybil noise).</li>
  <li><strong>Fees paid:</strong> willingness to pay for blockspace/services.</li>
  <li><strong>Revenue vs token incentives:</strong> real yield vs subsidy.</li>
  <li><strong>NVT-style ratios:</strong> <code>NVT ≈ Network Value / Transaction Volume</code> (use with care).</li>
  <li><strong>Supply metrics:</strong> long-term holder supply, exchange net flows.</li>
</ul>

<h3>Quality filters</h3>
<p>
Prefer entity-adjusted metrics, methodology notes, and long windows.
A spike in addresses from airdrop farming is not product-market fit.
</p>

<h3>Worked example</h3>
<p>
Protocol TVL +80% QoQ, but incentive emissions +300%, fees flat. Verdict:
mercenary capital likely. Thesis should not treat TVL as organic demand.
</p>

<h3>Common mistakes</h3>
<ul>
  <li>Equating wallet count with users.</li>
  <li>Ignoring wash volume on low-fee chains.</li>
</ul>
""",
            },
            "quizzes": [
                {
                    "question_text": {
                        "en": "TVL up 80% while fees flat and incentives up 300% suggests:",
                        "fa": "رشد ۸۰٪ TVL با کارمزد ثابت و اینسنتیو +۳۰۰٪ نشان می‌دهد:",
                        "de": "TVL +80%, Fees flat, Incentives +300% deutet auf:",
                    },
                    "question_type": "single_choice",
                    "options": [
                        {"optionId": "a", "text": {"en": "Likely mercenary/subsidized capital", "fa": "سرمایه مزدور/یارانه‌ای", "de": "Söldnerkapital"}},
                        {"optionId": "b", "text": {"en": "Guaranteed product-market fit", "fa": "PMF تضمینی", "de": "garantiertes PMF"}},
                        {"optionId": "c", "text": {"en": "Undervaluation by definition", "fa": "ارزانی ذاتی", "de": "Unterbewertung"}},
                        {"optionId": "d", "text": {"en": "Quantum security", "fa": "امنیت کوانتومی", "de": "Quantensicherheit"}},
                    ],
                    "correct_answer": {"option_id": "a"},
                    "explanation": {
                        "en": "Subsidized TVL without fee demand is weak evidence.",
                        "fa": "TVL یارانه‌ای بدون تقاضای کارمزد شاهد ضعیفی است.",
                        "de": "Subventioniertes TVL ist schwache Evidenz.",
                    },
                    "difficulty": 3,
                    "order": 1,
                },
            ],
        },
        {
            "slug": "valuation-frameworks",
            "title": "Valuation Frameworks That Stay Honest",
            "description": "Multiples, fee-based anchors, and why price targets fail.",
            "lesson_type": "theory",
            "order": 4,
            "estimated_minutes": 50,
            "content": {
                "html": """
<h2>Relative and cash-flow-ish anchors</h2>
<p>
Crypto rarely has clean equity cash flows, but relative valuation still
helps discipline narratives.
</p>
<ul>
  <li><strong>FDV / Fees or Revenue:</strong> how many years of current network fees are priced in.</li>
  <li><strong>P/E analogs:</strong> Market cap / annualized real yield to stakers (if claim is genuine).</li>
  <li><strong>Comparable set:</strong> same category L1/L2/DEX with usage-normalized metrics.</li>
  <li><strong>Optionality ladder:</strong> separate cash-flow claims from pure optionality bets.</li>
</ul>

<h3>Why single-point price targets fail</h3>
<p>
A target price hides parameter uncertainty (adoption path, fee switch,
unlock drag). Prefer scenario bands: bear/base/bull with explicit
assumptions on fee growth and net issuance.
</p>

<h3>Worked example</h3>
<p>
Token A: FDV $2B, annualized fees $40M → 50× FDV/fees.
Token B: FDV $400M, fees $20M → 20×. Cheaper is not automatically better —
compare growth, margins to holders, and unlock drag. If A has +80% float
dilution next year and B has none, multiple gap compresses in practice.
</p>

<h3>Common mistakes</h3>
<ul>
  <li>Applying equity P/E blindly to governance tokens with no cash-flow claim.</li>
  <li>Comparing FDV of one token to market cap of another.</li>
</ul>
""",
            },
            "quizzes": [
                {
                    "question_text": {
                        "en": "Comparing Token A (FDV) to Token B (market cap) is invalid because:",
                        "fa": "مقایسه FDV توکن A با market cap توکن B نامعتبر است زیرا:",
                        "de": "FDV vs. Market Cap vergleichen ist ungültig, weil:",
                    },
                    "question_type": "single_choice",
                    "options": [
                        {"optionId": "a", "text": {"en": "Different supply bases are being priced", "fa": "پایه عرضه متفاوت قیمت‌گذاری می‌شود", "de": "andere Angebotsbasis"}},
                        {"optionId": "b", "text": {"en": "Names differ", "fa": "نام‌ها فرق دارد", "de": "Namen"}},
                        {"optionId": "c", "text": {"en": "One is on Ethereum", "fa": "یکی روی اتریوم است", "de": "Chain"}},
                        {"optionId": "d", "text": {"en": "Charts look different", "fa": "چارت فرق دارد", "de": "Chart"}},
                    ],
                    "correct_answer": {"option_id": "a"},
                    "explanation": {
                        "en": "Normalize to the same supply concept before multiples.",
                        "fa": "قبل از مضرب، مفهوم عرضه را یکسان کنید.",
                        "de": "Angebot normalisieren.",
                    },
                    "difficulty": 3,
                    "order": 1,
                },
            ],
        },
        {
            "slug": "team-vesting-diligence",
            "title": "Team, Vesting, and Insider Economics",
            "description": "Incentive alignment and exit pressure.",
            "lesson_type": "theory",
            "order": 4,
            "estimated_minutes": 40,
            "content": {
                "html": """
<h2>Who gets paid when you hold</h2>
<p>
Fundamental quality includes governance and insider incentives. Ask:
</p>
<ul>
  <li>Team/investor % and vesting cliffs (on-chain if possible).</li>
  <li>Historical transfers from foundation/team wallets.</li>
  <li>Control of upgrade keys, pause switches, mint rights.</li>
  <li>Legal entity opacity vs claims of decentralization.</li>
</ul>

<h3>Red flags</h3>
<ul>
  <li>Upgradeable contracts controlled by 2-of-3 anonymous keys.</li>
  <li>Unlock cliffs within your planned holding horizon with large % float.</li>
  <li>Marketing "community-owned" while insiders hold 40%+.</li>
</ul>

<h3>Worked example</h3>
<p>
Vesting: 18-month cliff for 22% investor allocation unlocking linearly over
12 months. If your horizon is 6 months, you are underwriting that supply
wave. Either shorten horizon, hedge beta, or demand a valuation cushion.
</p>
""",
            },
            "quizzes": [
                {
                    "question_text": {
                        "en": "A large investor unlock inside your holding horizon is:",
                        "fa": "آزادسازی بزرگ سرمایه‌گذار در افق نگهداری شما:",
                        "de": "Investor-Unlock im Haltehorizont ist:",
                    },
                    "question_type": "single_choice",
                    "options": [
                        {"optionId": "a", "text": {"en": "A supply risk you must price or avoid", "fa": "ریسک عرضه که باید قیمت بخورید یا اجتناب کنید", "de": "Angebotsrisiko"}},
                        {"optionId": "b", "text": {"en": "Always bullish", "fa": "همیشه صعودی", "de": "bullish"}},
                        {"optionId": "c", "text": {"en": "Irrelevant", "fa": "بی‌ربط", "de": "egal"}},
                        {"optionId": "d", "text": {"en": "Proof of decentralization", "fa": "اثبات تمرکززدایی", "de": "Dezentralität"}},
                    ],
                    "correct_answer": {"option_id": "a"},
                    "explanation": {
                        "en": "Scheduled sellable supply is first-order risk.",
                        "fa": "عرضه قابل‌فروش زمان‌بندی‌شده ریسک درجه اول است.",
                        "de": "Geplantes Angebot ist Kernrisiko.",
                    },
                    "difficulty": 2,
                    "order": 1,
                },
            ],
        },
        {
            "slug": "risk-memo",
            "title": "Writing a Risk Memo Before Size",
            "description": "Convert research into a tradeable risk document.",
            "lesson_type": "practice",
            "order": 6,
            "estimated_minutes": 40,
            "content": {
                "html": """
<h2>From idea to underwriting document</h2>
<p>
One page, mandatory sections:
</p>
<ol>
  <li><strong>Thesis:</strong> 3 sentences max.</li>
  <li><strong>Time horizon:</strong> weeks / months / years.</li>
  <li><strong>Catalysts:</strong> unlock, upgrade, fee switch, listing.</li>
  <li><strong>Risks:</strong> market, protocol, regulatory, custody, liquidity.</li>
  <li><strong>Falsifiers:</strong> observable kill switches.</li>
  <li><strong>Size &amp; invalidation:</strong> R defined, max heat, exit policy.</li>
</ol>

<h3>Worked mini-memo</h3>
<p>
Thesis: fee growth + declining net issuance. Horizon: 2 quarters.
Catalyst: fee switch vote. Risks: unlock wave month 4, competitor chain
fee share gain. Falsifier: fees flat while net issuance positive for 8
weeks. Size 0.75R at entry zone, invalidation weekly close below structural
low.
</p>
<p>
If you cannot write this page, you are not ready to size.
</p>
""",
            },
            "quizzes": [
                {
                    "question_text": {
                        "en": "A risk memo must include:",
                        "fa": "memo ریسک باید شامل باشد:",
                        "de": "Ein Risiko-Memo enthält:",
                    },
                    "question_type": "single_choice",
                    "options": [
                        {"optionId": "a", "text": {"en": "Thesis, risks, falsifiers, size/invalidation", "fa": "پایان‌نامه، ریسک‌ها، falsifier، سایز/حد باطل", "de": "These, Risiken, Falsifizierer, Size"}},
                        {"optionId": "b", "text": {"en": "Only entry price", "fa": "فقط قیمت ورود", "de": "nur Entry"}},
                        {"optionId": "c", "text": {"en": "Meme chart only", "fa": "فقط چارت میم", "de": "nur Meme"}},
                        {"optionId": "d", "text": {"en": "Leverage max", "fa": "حداکثر اهرم", "de": "max Hebel"}},
                    ],
                    "correct_answer": {"option_id": "a"},
                    "explanation": {
                        "en": "The memo is the bridge from research to risk.",
                        "fa": "memo پل تحقیق به ریسک است.",
                        "de": "Memo verbindet Research und Risiko.",
                    },
                    "difficulty": 2,
                    "order": 1,
                },
            ],
        },
    ],
}
