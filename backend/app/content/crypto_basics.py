"""Crypto Basics module.

Benchmark depth: Binance Academy topic clusters + Princeton Bitcoin textbook
chapters on consensus/UTXO + professional custody/threat-model guidance.
Target: 8 lessons, application-level quizzes, worked examples.
"""

from __future__ import annotations

from typing import Any


CRYPTO_BASICS: dict[str, Any] = {
    "slug": "crypto-basics",
    "title": "Crypto Fundamentals",
    "description": (
        "Monetary properties, cryptography, ledger models, consensus, fee markets, "
        "custody threat models, exchange microstructure, and scaling trade-offs."
    ),
    "order": 1,
    "required_tier": "free",
    "lessons": [
        {
            "slug": "monetary-properties",
            "title": "Digital Money and Monetary Properties",
            "description": (
                "What makes a monetary asset credible: scarcity, settlement, "
                "censorship resistance, and the crypto value proposition."
            ),
            "lesson_type": "theory",
            "order": 1,
            "estimated_minutes": 35,
            "content": {
                "html": """
<h2>Why money needs properties, not just a brand</h2>
<p>
Money is a coordination technology. Any asset used as money is judged on
portability, divisibility, durability, fungibility, verifiability, and
scarcity. Fiat scores high on portability and divisibility but is
politically elastic. Commodity money (gold) is scarce but hard to settle
digitally. Cryptocurrency attempts programmable scarcity with global
settlement.
</p>

<h3>Monetary premium vs utility premium</h3>
<p>
An asset price can be decomposed conceptually as
<code>price = utility_value + monetary_premium</code>.
Utility value is cash-flow or consumption value. Monetary premium is what
holders pay for use as store of value / medium of exchange. Bitcoin's
thesis is almost entirely monetary premium. Utility tokens (gas tokens,
governance claims) have a different risk model — if the utility demand
fails, the monetary premium collapses with it.
</p>

<h3>Hardness and credible supply</h3>
<p>
Supply hardness is not a marketing claim; it is an enforcement property.
For Bitcoin, the 21M cap and halving schedule are consensus rules. Breaking
them requires a fork that economic nodes reject. Ask always:
<strong>who can change the supply rule, and at what cost?</strong>
If a foundation can mint without social consensus, scarcity is soft.
</p>

<table>
  <tr><th>Asset</th><th>Issuance</th><th>Settlement</th><th>Censorship resistance</th></tr>
  <tr><td>USD (cash)</td><td>Policy elastic</td><td>Fast (digital rails)</td><td>Low (accounts freezable)</td></tr>
  <tr><td>Gold</td><td>Mining growth ~1.5%/yr</td><td>Slow / costly</td><td>Medium (physical seizure risk)</td></tr>
  <tr><td>BTC</td><td>Fixed schedule, cap 21M</td><td>Probabilistic, then final</td><td>High (self-custody + PoW)</td></tr>
  <tr><td>Many L1 gas tokens</td><td>Variable / inflationary</td><td>Fast, fee-dependent</td><td>Medium (validator set dependent)</td></tr>
</table>

<h3>Settlement finality: a spectrum</h3>
<p>
Cash finality is legal. Gold finality is physical. Blockchain finality is
probabilistic (PoW confirmations) or economic (PoS reorg cost). A trader
must map this to operations: how many confirmations for $100? for $10M?
The answer is not ideology; it is expected cost of reorg vs cost of delay.
</p>

<h3>Worked example: evaluating a "scarce" token</h3>
<ul>
  <li>Max supply 100M stated in docs.</li>
  <li>Team + foundation allocation 35% unlocks over 4 years.</li>
  <li>Emissions continue at 8% annually to "ecosystem fund".</li>
  <li>Governance can raise emissions with 51% of staked token.</li>
</ul>
<p>
Conclusion: effective scarcity is low. Near-term float will grow faster
than headline max supply suggests. A monetary premium is hard to justify
unless governance is constrained on-chain and unlock schedule is enforced
by code, not promise.
</p>

<h3>Common mistakes</h3>
<ul>
  <li>Equating "crypto" with Bitcoin's monetary properties.</li>
  <li>Ignoring unlock cliffs when reasoning about scarcity.</li>
  <li>Treating settlement finality as binary (0/1) instead of probabilistic.</li>
  <li>Confusing decentralization of users with decentralization of consensus.</li>
</ul>
""",
            },
            "quizzes": [
                {
                    "question_text": {
                        "en": "A token has a hard 21M cap, but 40% unlocks to insiders over 12 months. Near-term scarcity is best described as:",
                        "fa": "توکنی سقف ۲۱ میلیونی دارد اما ۴۰٪ آن طی ۱۲ ماه به اینسایدرها آزاد می‌شود. کمیابی کوتاه‌مدت بهتر است توصیف شود به:",
                        "de": "Ein Token hat eine feste Obergrenze von 21 Mio., 40% werden jedoch über 12 Monate an Insider freigeschaltet. Die kurzfristige Knappheit ist:",
                    },
                    "question_type": "single_choice",
                    "options": [
                        {"optionId": "a", "text": {"en": "High, because max supply is fixed", "fa": "بالا، چون سقف عرضه ثابت است", "de": "Hoch, da das Angebot fix ist"}},
                        {"optionId": "b", "text": {"en": "Low, because circulating supply rises quickly", "fa": "پایین، چون عرضه در گردش سریع رشد می‌کند", "de": "Gering, da das zirkulierende Angebot schnell steigt"}},
                        {"optionId": "c", "text": {"en": "Equal to gold's scarcity", "fa": "برابر با کمیابی طلا", "de": "Wie bei Gold"}},
                        {"optionId": "d", "text": {"en": "Determined only by daily volume", "fa": "فقط با حجم روزانه مشخص می‌شود", "de": "Nur vom Tagesvolumen bestimmt"}},
                    ],
                    "correct_answer": {"option_id": "b"},
                    "explanation": {
                        "en": "Near-term float and unlock schedules dominate tradable scarcity. Max supply is a long-horizon constraint only if issuance rules cannot be changed.",
                        "fa": "عرضه در گردش و برنامه آزادسازی، کمیابی قابل‌معامله را تعیین می‌کنند. سقف عرضه فقط بلندمدت معتبر است اگر قابل تغییر نباشد.",
                        "de": "Kurzfristiges Float und Unlock-Schedules bestimmen die handelbare Knappheit.",
                    },
                    "difficulty": 3,
                    "order": 1,
                },
                {
                    "question_text": {
                        "en": "Bitcoin confirmation depth exists because:",
                        "fa": "عمق تأیید بیت‌کوین وجود دارد زیرا:",
                        "de": "Bitcoin-Bestätigungen existieren, weil:",
                    },
                    "question_type": "single_choice",
                    "options": [
                        {"optionId": "a", "text": {"en": "Nodes are slow", "fa": "نودها کند هستند", "de": "Nodes langsam sind"}},
                        {"optionId": "b", "text": {"en": "Finality is probabilistic against reorgs", "fa": "نهایی‌شدن در برابر reorg احتمالی است", "de": "Finalität gegen Reorgs probabilistisch ist"}},
                        {"optionId": "c", "text": {"en": "Miners delay on purpose", "fa": "ماینرها عمداً تأخیر می‌کنند", "de": "Miner absichtlich verzögern"}},
                        {"optionId": "d", "text": {"en": "Exchanges require it by law", "fa": "صرافی‌ها قانوناً می‌خواهند", "de": "Börsen es gesetzlich verlangen"}},
                    ],
                    "correct_answer": {"option_id": "b"},
                    "explanation": {
                        "en": "Each additional block makes rewriting history exponentially more expensive. Depth is a risk parameter, not a rule of nature.",
                        "fa": "هر بلوک اضافه بازنویسی تاریخچه را به‌صورت نمایی گران‌تر می‌کند. عمق پارامتر ریسک است، نه قانون طبیعت.",
                        "de": "Jeder Block macht eine Historien-Rewrite teurer.",
                    },
                    "difficulty": 2,
                    "order": 2,
                },
                {
                    "question_text": {
                        "en": "Which question best tests whether a chain has credible scarcity?",
                        "fa": "کدام پرسش بهترین آزمون کمیابی معتبر یک زنجیره است؟",
                        "de": "Welche Frage testet glaubwürdige Knappheit am besten?",
                    },
                    "question_type": "single_choice",
                    "options": [
                        {"optionId": "a", "text": {"en": "What is the current price?", "fa": "قیمت فعلی چیست؟", "de": "Wie ist der Preis?"}},
                        {"optionId": "b", "text": {"en": "Who can change issuance, and at what cost?", "fa": "چه کسی می‌تواند انتشار را تغییر دهد و با چه هزینه‌ای؟", "de": "Wer kann Emission ändern und zu welchem Preis?"}},
                        {"optionId": "c", "text": {"en": "How many influencers cover it?", "fa": "چند اینفلوئنسر آن را پوشش می‌دهند؟", "de": "Wie viele Influencer es covern"}},
                        {"optionId": "d", "text": {"en": "How high is 24h volume?", "fa": "حجم ۲۴ ساعته چقدر است؟", "de": "Wie hoch ist das 24h-Volumen?"}},
                    ],
                    "correct_answer": {"option_id": "b"},
                    "explanation": {
                        "en": "Scarcity is credible only when change cost is high and visible. Marketing max-supply numbers are not enforcement.",
                        "fa": "کمیابی فقط وقتی معتبر است که هزینه تغییر بالا و شفاف باشد. عدد «سقف عرضه» در تبلیغات الزام اجرا نیست.",
                        "de": "Knappheit ist nur glaubwürdig, wenn Änderungskosten hoch und sichtbar sind.",
                    },
                    "difficulty": 3,
                    "order": 3,
                },
            ],
        },
        {
            "slug": "cryptographic-primitives",
            "title": "Keys, Hashes, and Signatures",
            "description": (
                "The minimum cryptography a trader must own: hashes, asymmetric "
                "keys, digital signatures, and address derivation intuition."
            ),
            "lesson_type": "theory",
            "order": 2,
            "estimated_minutes": 40,
            "content": {
                "html": """
<h2>Hash functions: fingerprints with commitments</h2>
<p>
A cryptographic hash <code>H(x)</code> maps arbitrary input to a fixed-length
digest with three practical properties:
</p>
<ul>
  <li><strong>Pre-image resistance:</strong> given <code>y</code>, hard to find <code>x</code> with <code>H(x)=y</code>.</li>
  <li><strong>Second pre-image resistance:</strong> given <code>x1</code>, hard to find <code>x2≠x1</code> with the same hash.</li>
  <li><strong>Collision resistance:</strong> hard to find any pair with equal hashes.</li>
</ul>
<p>
Blockchains use hashes to link blocks, commit to transaction sets (Merkle
roots), and derive addresses. If collision resistance breaks, the security
model collapses regardless of token price.
</p>

<h3>Public keys, private keys, signatures</h3>
<p>
A private key <code>k</code> is a large random integer. The public key
<code>pk = k·G</code> is derived on an elliptic curve. A digital signature
<code>Sign(k, msg)</code> proves control of <code>k</code> without revealing
<code>k</code>. Verification <code>Verify(pk, msg, sig)</code> is cheap.
</p>
<p>
Operationally: <strong>losing <code>k</code> means losing funds</strong>.
There is no bank to reverse a signature. Seed phrases (BIP39) are human
encodings of <code>k</code> (or a master key that derives many keys). Anyone
who sees the seed can spend.
</p>

<h3>Addresses and derivation (intuition only)</h3>
<ul>
  <li>BTC-style: hash of pubkey → address; locking/unlocking scripts enforce spend rules.</li>
  <li>Account chains (Ethereum-style): address from pubkey hash; account balances are global state.</li>
  <li>Hierarchical deterministic (HD) wallets: one seed → infinite keys with backup once.</li>
</ul>
<p>
You do not need to implement secp256k1. You do need to know which object is
secret, how backups work, and what an address commitment does and does not
hide (addresses are pseudonymous, not anonymous).
</p>

<h3>Worked example: signing a transfer</h3>
<ol>
  <li>Wallet builds message <code>msg</code> = {from, to, amount, nonce, chain_id}.</li>
  <li>User authorizes (password / biometrics) to unlock <code>k</code>.</li>
  <li><code>sig = Sign(k, hash(msg))</code> is attached to the transaction.</li>
  <li>Network verifies <code>Verify(pk, hash(msg), sig)</code> and state transition.</li>
</ol>
<p>
If <code>chain_id</code> is omitted or mixed up (replay protection failure),
the same signature can be replayed on another network. This is why
transaction structure is security-critical.
</p>

<h3>Common mistakes</h3>
<ul>
  <li>Treating "password" as the private key. The password usually encrypts local keystore; the key is still the secret.</li>
  <li>Storing seeds in cloud notes/screenshots.</li>
  <li>Believing "not your keys, not your coins" is about ideology rather than counterparty math.</li>
  <li>Ignoring phishing for approvals (permit signatures, unlimited allowances).</li>
</ul>
""",
            },
            "quizzes": [
                {
                    "question_text": {
                        "en": "A digital signature primarily proves:",
                        "fa": "امضای دیجیتال در درجه اول چه چیزی را اثبات می‌کند؟",
                        "de": "Eine digitale Signatur beweist primär:",
                    },
                    "question_type": "single_choice",
                    "options": [
                        {"optionId": "a", "text": {"en": "That the message is confidential", "fa": "پیام محرمانه است", "de": "Dass die Nachricht vertraulich ist"}},
                        {"optionId": "b", "text": {"en": "Control of a private key over that message", "fa": "کنترل کلید خصوصی روی آن پیام", "de": "Kontrolle eines privaten Schlüssels über die Nachricht"}},
                        {"optionId": "c", "text": {"en": "That the sender has enough balance", "fa": "فرستنده موجودی کافی دارد", "de": "Dass der Sender Guthaben hat"}},
                        {"optionId": "d", "text": {"en": "That the transaction is profitable", "fa": "تراکنش سودآور است", "de": "Dass die Transaktion profitabel ist"}},
                    ],
                    "correct_answer": {"option_id": "b"},
                    "explanation": {
                        "en": "Signatures prove authorization, not funds or confidentiality. Balance checks are separate consensus rules.",
                        "fa": "امضا مجوز را ثابت می‌کند، نه موجودی یا محرمانگی. کنترل موجودی قاعده جداگانه consensus است.",
                        "de": "Signaturen beweisen Autorisierung, nicht Guthaben.",
                    },
                    "difficulty": 2,
                    "order": 1,
                },
                {
                    "question_text": {
                        "en": "Your 12-word seed phrase is best understood as:",
                        "fa": "عبارت seed دوازده‌کلمه‌ای شما بهتر است درک شود به‌عنوان:",
                        "de": "Eine 12-Wort-Seed-Phrase ist am besten verstanden als:",
                    },
                    "question_type": "single_choice",
                    "options": [
                        {"optionId": "a", "text": {"en": "A username for your wallet", "fa": "نام کاربری کیف پول", "de": "Benutzername"}},
                        {"optionId": "b", "text": {"en": "Human-readable encoding of master key material", "fa": "کدگذاری خوانا از ماده کلید اصلی", "de": "Lesbare Kodierung des Master-Schlüssels"}},
                        {"optionId": "c", "text": {"en": "A public backup of balances", "fa": "پشتیبان عمومی موجودی‌ها", "de": "Öffentliches Backup"}},
                        {"optionId": "d", "text": {"en": "Encrypted by the exchange automatically", "fa": "صرافی خودکار رمزگذاری می‌کند", "de": "Automatisch von der Börse verschlüsselt"}},
                    ],
                    "correct_answer": {"option_id": "b"},
                    "explanation": {
                        "en": "The seed derives the key tree. Exposure is equivalent to losing custody of all derived accounts.",
                        "fa": "seed درخت کلیدها را می‌سازد. افشای آن معادل از دست دادن حضانت همه حساب‌هاست.",
                        "de": "Der Seed leitet den Schlüsselbaum ab.",
                    },
                    "difficulty": 2,
                    "order": 2,
                },
                {
                    "question_text": {
                        "en": "Missing replay protection (e.g., no chain_id in a signed payload) enables:",
                        "fa": "نبود محافظت replay (مثلاً نبود chain_id در payload امضاشده) چه چیزی را ممکن می‌کند؟",
                        "de": "Fehlender Replay-Schutz ermöglicht:",
                    },
                    "question_type": "single_choice",
                    "options": [
                        {"optionId": "a", "text": {"en": "Faster block times", "fa": "بلوک‌های سریع‌تر", "de": "Schnellere Blöcke"}},
                        {"optionId": "b", "text": {"en": "Reusing the same signature on another chain", "fa": "استفاده مجدد از همان امضا روی زنجیره دیگر", "de": "Wiederverwendung der Signatur auf einer anderen Chain"}},
                        {"optionId": "c", "text": {"en": "Lower fees automatically", "fa": "کاهش خودکار کارمزد", "de": "Automatisch niedrigere Gebühren"}},
                        {"optionId": "d", "text": {"en": "Quantum resistance", "fa": "مقاومت کوانتومی", "de": "Quantenresistenz"}},
                    ],
                    "correct_answer": {"option_id": "b"},
                    "explanation": {
                        "en": "If the signed message is chain-agnostic, the same authorization can be valid elsewhere.",
                        "fa": "اگر پیام امضاشده به زنجیره وابسته نباشد، همان مجوز جای دیگری هم معتبر است.",
                        "de": "Ohne Chain-Bindung ist die Autorisierung portierbar.",
                    },
                    "difficulty": 3,
                    "order": 3,
                },
            ],
        },
        {
            "slug": "ledger-models",
            "title": "UTXO vs Account Models and Merkle Commitments",
            "description": (
                "How balances are represented and why ledger model changes wallet, "
                "privacy, and smart-contract design."
            ),
            "lesson_type": "theory",
            "order": 3,
            "estimated_minutes": 45,
            "content": {
                "html": """
<h2>Two ways to answer "who owns what"</h2>
<p>
A blockchain state machine must define ownership. Two dominant designs
exist. They are not cosmetic; they change fee behavior, parallelization,
privacy, and contract complexity.
</p>

<h3>UTXO model (Bitcoin-like)</h3>
<p>
State is a set of unspent transaction outputs. A transaction consumes
inputs (references to UTXOs, unlocking them with signatures/scripts) and
creates new outputs. Your wallet balance is
<code>sum(UTXOs controlled by your keys)</code>, not a single integer.
</p>
<ul>
  <li><strong>Pros:</strong> parallel validation, clear double-spend check (spent set), fine-grained privacy (many addresses).</li>
  <li><strong>Cons:</strong> change outputs complexity, harder account-style contracts, wallet UX mistakes (change address handling).</li>
</ul>

<h3>Account model (Ethereum-like)</h3>
<p>
State maps <code>address → balance/code/storage</code>. Transactions mutate
accounts with nonces to prevent replay. Contracts share a global state
model, which makes composability natural and fee logic account-based.
</p>
<ul>
  <li><strong>Pros:</strong> intuitive balances, contract composability, simpler payment UX.</li>
  <li><strong>Cons:</strong> state growth pressure, account abstraction complexity, MEV surface in mempool ordering.</li>
</ul>

<table>
  <tr><th>Dimension</th><th>UTXO</th><th>Account</th></tr>
  <tr><td>Balance representation</td><td>Set of coins</td><td>Account map</td></tr>
  <tr><td>Replay defense</td><td>Spent outpoints</td><td>Nonces</td></tr>
  <tr><td>Contract composability</td><td>Harder</td><td>Natural</td></tr>
  <tr><td>Privacy potential</td><td>Higher (many UTXOs)</td><td>Lower (address graph)</td></tr>
  <tr><td>Parallelism</td><td>Easier</td><td>Harder (state contention)</td></tr>
</table>

<h3>Merkle trees and SPV-style verification</h3>
<p>
Transactions in a block are hashed into a Merkle tree; the root is in the
header. A light client can verify inclusion of a transaction with an
authentication path of <code>O(log n)</code> hashes instead of the full
block. This is why "proof of payment" can be compact.
</p>
<p>
Caveat: inclusion proof is not proof of economic finality. A block can be
reorged. Always combine Merkle inclusion with confirmation depth policy.
</p>

<h3>Worked example: change in a UTXO spend</h3>
<p>
You control a UTXO of 0.50 BTC and pay 0.12 BTC. Wallet constructs:
</p>
<ul>
  <li>Input: UTXO 0.50 BTC</li>
  <li>Output1: 0.12 BTC to merchant</li>
  <li>Output2: 0.37 BTC to your change address (minus fee)</li>
</ul>
<p>
If fee is 0.01 BTC, change is 0.37. Forgetting change or reusing addresses
is a privacy leak; sending change to an address you do not control is
catastrophic.
</p>

<h3>Common mistakes</h3>
<ul>
  <li>Assuring "wallet balance" exists as a row in a database like a bank ledger.</li>
  <li>Ignoring change addresses when auditing self-custody.</li>
  <li>Calling Merkle inclusion "final settlement".</li>
</ul>
""",
            },
            "quizzes": [
                {
                    "question_text": {
                        "en": "In a UTXO model, a wallet balance is:",
                        "fa": "در مدل UTXO، موجودی کیف پول چیست؟",
                        "de": "Im UTXO-Modell ist ein Wallet-Guthaben:",
                    },
                    "question_type": "single_choice",
                    "options": [
                        {"optionId": "a", "text": {"en": "A single integer in global state", "fa": "یک عدد در state سراسری", "de": "Eine Zahl im globalen State"}},
                        {"optionId": "b", "text": {"en": "The sum of spendable outputs controlled by keys", "fa": "مجموع خروجی‌های خرج‌نشده تحت کنترل کلیدها", "de": "Summe kontrollierbarer unspent Outputs"}},
                        {"optionId": "c", "text": {"en": "Whatever the exchange UI shows", "fa": "آنچه UI صرافی نشان می‌دهد", "de": "Was die Börsen-UI zeigt"}},
                        {"optionId": "d", "text": {"en": "Always one address only", "fa": "همیشه فقط یک آدرس", "de": "Immer nur eine Adresse"}},
                    ],
                    "correct_answer": {"option_id": "b"},
                    "explanation": {
                        "en": "UTXO wallets aggregate many coins. Balance is derived, not stored as one field.",
                        "fa": "کیف پول UTXO مجموعه‌ای از سکه‌ها را جمع می‌زند. موجودی استخراج می‌شود، نه ذخیره.",
                        "de": "Guthaben wird abgeleitet, nicht als Feld gespeichert.",
                    },
                    "difficulty": 2,
                    "order": 1,
                },
                {
                    "question_text": {
                        "en": "A Merkle inclusion proof lets a light client verify:",
                        "fa": "اثبات شامل بودن Merkle به کلاینت سبک اجازه می‌دهد چه چیزی را تأیید کند؟",
                        "de": "Ein Merkle-Inklusionsbeweis erlaubt die Prüfung von:",
                    },
                    "question_type": "single_choice",
                    "options": [
                        {"optionId": "a", "text": {"en": "That the tx is economically final forever", "fa": "تراکنش برای همیشه از نظر اقتصادی نهایی است", "de": "Endgültiger wirtschaftlicher Finalität"}},
                        {"optionId": "b", "text": {"en": "That the tx is in that block's committed set", "fa": "تراکنش در مجموعه commitشده آن بلوک است", "de": "Zugehörigkeit zur committeten Menge des Blocks"}},
                        {"optionId": "c", "text": {"en": "That fees were fair", "fa": "کارمزد منصفانه بود", "de": "Faire Gebühren"}},
                        {"optionId": "d", "text": {"en": "That the sender is KYC'd", "fa": "فرستنده KYC دارد", "de": "KYC des Senders"}},
                    ],
                    "correct_answer": {"option_id": "b"},
                    "explanation": {
                        "en": "Inclusion is a data commitment fact. Finality depends on consensus/reorg risk.",
                        "fa": "شامل بودن یک واقعیت commit داده‌ای است. نهایی‌بودن به consensus وابسته است.",
                        "de": "Inklusion ist ein Commitment-Fakt.",
                    },
                    "difficulty": 3,
                    "order": 2,
                },
                {
                    "question_text": {
                        "en": "Why do account chains use nonces?",
                        "fa": "چرا زنجیره‌های account از nonce استفاده می‌کنند؟",
                        "de": "Warum nutzen Account-Chains Nonces?",
                    },
                    "question_type": "single_choice",
                    "options": [
                        {"optionId": "a", "text": {"en": "To make signatures longer", "fa": "برای بلندتر کردن امضا", "de": "Längere Signaturen"}},
                        {"optionId": "b", "text": {"en": "To order txs and prevent replay of the same authorization", "fa": "برای ترتیب تراکنش‌ها و جلوگیری از replay مجوز مشابه", "de": "Zur Ordnung und Replay-Verhinderung"}},
                        {"optionId": "c", "text": {"en": "To compress state automatically", "fa": "برای فشرده‌سازی خودکار state", "de": "State-Kompression"}},
                        {"optionId": "d", "text": {"en": "To hide the receiver", "fa": "برای مخفی کردن گیرنده", "de": "Empfänger verbergen"}},
                    ],
                    "correct_answer": {"option_id": "b"},
                    "explanation": {
                        "en": "Nonces enforce per-account ordering and make an old signed tx invalid after inclusion.",
                        "fa": "nonce ترتیب حساب را اجباری می‌کند و تراکنش امضاشده قدیمی را بعد از اجرا نامعتبر می‌کند.",
                        "de": "Nonces erzwingen Ordnung und verhindern Replay.",
                    },
                    "difficulty": 2,
                    "order": 3,
                },
            ],
        },
        {
            "slug": "consensus-and-attacks",
            "title": "Consensus: PoW, PoS, Finality, and Attacks",
            "description": (
                "How networks agree under adversarial conditions, and which "
                "attacks matter for holders and traders."
            ),
            "lesson_type": "theory",
            "order": 4,
            "estimated_minutes": 50,
            "content": {
                "html": """
<h2>Consensus is a security budget</h2>
<p>
Consensus protocols decide which history is canonical when parties are
rational or malicious. The question is never "is it decentralized?" in the
abstract. The question is:
<em>what is the cost to rewrite or censor, and who pays that cost?</em>
</p>

<h3>Proof of Work (PoW)</h3>
<p>
Miners spend energy to find a nonce such that
<code>H(header) &lt; target</code>. Longest/heaviest chain wins. Security is
the price of rewriting k blocks: an attacker must outpace honest
accumulated work for the reorg window.
</p>
<ul>
  <li><strong>Strength:</strong> objective verification of cost; expensive external attack.</li>
  <li><strong>Weakness:</strong> energy cost, mining centralization tendencies, reorg risk near deep confirmations is low but non-zero.</li>
</ul>

<h3>Proof of Stake (PoS)</h3>
<p>
Validators stake capital and sign attestations. Misbehavior can be
slashed. Finality is often economic (checkpoint finality) rather than
purely probabilistic. Security rests on stake distribution, slashing
rules, client diversity, and social recovery assumptions.
</p>
<ul>
  <li><strong>Strength:</strong> capital-at-risk, energy efficiency, fast finality designs.</li>
  <li><strong>Weakness:</strong> stake centralization, long-range/weak subjectivity, governance capture via staking derivatives.</li>
</ul>

<h3>Attack catalog for traders</h3>
<table>
  <tr><th>Attack</th><th>Mechanism</th><th>Trader impact</th></tr>
  <tr><td>Double spend / reorg</td><td>Replace a confirmed history</td><td>Deposits reverse; settlement lies</td></tr>
  <tr><td>51% / majority attack</td><td>Control block production</td><td>Censorship, double spends</td></tr>
  <tr><td>Censorship</td><td>Exclude txs selectively</td><td>Exits blocked at L1</td></tr>
  <tr><td>Validator collusion</td><td>Coordinate majority stake</td><td>Finality theater</td></tr>
  <tr><td>Client monoculture bug</td><td>One client dominates</td><td>Consensus split / halt</td></tr>
</table>

<h3>Worked example: exchange deposit policy</h3>
<p>
Exchange credits a coin deposit after <code>n</code> confirmations. For a
low-hashrate PoW coin, 6 confirmations may still be cheap to reorg during
low difficulty. Policy should be:
</p>
<ul>
  <li>Estimate attacker cost per confirmation (hashrate × time × price).</li>
  <li>Compare to deposit size at risk.</li>
  <li>Set <code>n</code> such that expected fraud loss &lt; operational cost of delay.</li>
</ul>
<p>
A professional desk does not copy "6 confirmations" blindly across chains.
</p>

<h3>Finality language hygiene</h3>
<ul>
  <li><strong>Probabilistic finality:</strong> confidence increases with depth (PoW).</li>
  <li><strong>Economic finality:</strong> revert cost exceeds potential gain (many PoS).</li>
  <li><strong>Instant finality marketing:</strong> ask what happens under mass validator exit or client bug.</li>
</ul>

<h3>Common mistakes</h3>
<ul>
  <li>Assuming "decentralized" implies censorship resistance.</li>
  <li>Using the same confirmation count for BTC and a low-security clone.</li>
  <li>Ignoring client diversity in PoS risk assessment.</li>
</ul>
""",
            },
            "quizzes": [
                {
                    "question_text": {
                        "en": "The right way to set exchange confirmations is to compare:",
                        "fa": "راه درست تعیین تعداد تأیید در صرافی مقایسه چیست؟",
                        "de": "Bestätigungen setzt man richtig, indem man vergleicht:",
                    },
                    "question_type": "single_choice",
                    "options": [
                        {"optionId": "a", "text": {"en": "Blog posts from 2017", "fa": "پست‌های وبلاگ ۲۰۱۷", "de": "Blogposts von 2017"}},
                        {"optionId": "b", "text": {"en": "Attacker reorg cost vs deposit size at risk", "fa": "هزینه حمله reorg در برابر میزان واریز در معرض خطر", "de": "Reorg-Kosten vs. Einlagenrisiko"}},
                        {"optionId": "c", "text": {"en": "UI animation speed", "fa": "سرعت انیمیشن UI", "de": "UI-Animationsgeschwindigkeit"}},
                        {"optionId": "d", "text": {"en": "Number of Twitter followers of the chain", "fa": "تعداد فالوئرهای توییتر زنجیره", "de": "Twitter-Follower"}},
                    ],
                    "correct_answer": {"option_id": "b"},
                    "explanation": {
                        "en": "Confirmation depth is an economic security parameter and should be set per chain.",
                        "fa": "عمق تأیید پارامتر امنیت اقتصادی است و باید per chain تنظیم شود.",
                        "de": "Bestätigungstiefe ist ein ökonomischer Parameter pro Chain.",
                    },
                    "difficulty": 3,
                    "order": 1,
                },
                {
                    "question_text": {
                        "en": "PoS 'instant finality' claims should be stress-tested against:",
                        "fa": "ادعای «نهایی‌شدن فوری» PoS باید در برابر چه چیزی آزموده شود؟",
                        "de": "PoS-Finalitätsclaims sollten getestet werden gegen:",
                    },
                    "question_type": "single_choice",
                    "options": [
                        {"optionId": "a", "text": {"en": "Mass exits and client bugs", "fa": "خروج گسترده و باگ کلاینت", "de": "Massenausstiege und Client-Bugs"}},
                        {"optionId": "b", "text": {"en": "Coin logo aesthetics", "fa": "زیبایی لوگوی کوین", "de": "Logo-Design"}},
                        {"optionId": "c", "text": {"en": "Number of wallets on a dashboard", "fa": "تعداد کیف پول‌ها در داشبورد", "de": "Wallet-Anzahl"}},
                        {"optionId": "d", "text": {"en": "Whether the whitepaper is long", "fa": "بلند بودن وایت‌پیپر", "de": "Länge des Whitepapers"}},
                    ],
                    "correct_answer": {"option_id": "a"},
                    "explanation": {
                        "en": "Weak subjectivity and client monoculture are first-order PoS operational risks.",
                        "fa": "weak subjectivity و یکنواختی کلاینت ریسک‌های عملیاتی درجه اول PoS هستند.",
                        "de": "Weak Subjectivity und Client-Monokultur sind Kernrisiken.",
                    },
                    "difficulty": 3,
                    "order": 2,
                },
                {
                    "question_text": {
                        "en": "A double-spend attack means:",
                        "fa": "حمله double-spend یعنی:",
                        "de": "Ein Double-Spend bedeutet:",
                    },
                    "question_type": "single_choice",
                    "options": [
                        {"optionId": "a", "text": {"en": "Spending the same funds in two conflicting histories", "fa": "خرج همان وجوه در دو تاریخچه متضاد", "de": "Dieselben Mittel in zwei widersprüchlichen Historien"}},
                        {"optionId": "b", "text": {"en": "Paying two different merchants legally", "fa": "پرداخت قانونی به دو تاجر", "de": "Zwei Händler legal bezahlen"}},
                        {"optionId": "c", "text": {"en": "High fee bidding", "fa": "پیشنهاد کارمزد بالا", "de": "Hohe Gebotsgebühren"}},
                        {"optionId": "d", "text": {"en": "Running two wallets", "fa": "اجرای دو کیف پول", "de": "Zwei Wallets nutzen"}},
                    ],
                    "correct_answer": {"option_id": "a"},
                    "explanation": {
                        "en": "Conflicting spends are resolved by consensus; the loser is orphaned if depth rules are honest.",
                        "fa": "خرجهای متضاد با consensus حل می‌شوند؛ بازنده orphan می‌شود.",
                        "de": "Widersprüche löst der Konsens auf.",
                    },
                    "difficulty": 2,
                    "order": 3,
                },
            ],
        },
        {
            "slug": "mempool-fees-mev",
            "title": "Mempool, Fee Markets, and MEV",
            "description": (
                "Why your transaction can stall, how fees clear, and how order "
                "flow can be extracted — core market microstructure for on-chain trading."
            ),
            "lesson_type": "theory",
            "order": 5,
            "estimated_minutes": 45,
            "content": {
                "html": """
<h2>The mempool is a waiting room with priority rules</h2>
<p>
Unconfirmed transactions sit in nodes' mempools. Block space is scarce, so
inclusion is an auction (explicit fees, or gas/fee markets). Underpricing
fees in a burst leads to stalls and replacement anxiety (RBF policies).
</p>

<h3>Fee market mechanics</h3>
<ul>
  <li><strong>BTC-style:</strong> sat/vByte bids for limited block weight.</li>
  <li><strong>EVM-style:</strong> base fee (burned) + priority tip; base fee adjusts to block utilization targets.</li>
</ul>
<p>
A trader sending during volatility should use a fee estimator based on
short-horizon inclusion probability, not yesterday's average.
</p>

<h3>Replacement and stuck transactions</h3>
<p>
If a tx is underpriced, you may replace it (where policy allows) with a
higher fee. Without replacement support, funds can look "stuck" until
dropped. Operational checklist: fee floor, RBF flag, child-pays-for-parent
options, and patience policy.
</p>

<h3>MEV in plain terms</h3>
<p>
Maximal Extractable Value is value captured by controlling transaction
ordering / inclusion. Forms include:
</p>
<ul>
  <li><strong>Arbitrage:</strong> price gaps across pools/venues, winner takes order.</li>
  <li><strong>Sandwich:</strong> place txs around a victim swap to move price against them.</li>
  <li><strong>Liquidation:</strong> race to liquidate undercollateralized positions.</li>
</ul>
<p>
If you market-swap large size on a transparent mempool, you can be
adversarially priced. Mitigations: slippage limits, private relays / batch
auctions, TWAP, or RFQ venues.
</p>

<h3>Worked example: sandwich exposure</h3>
<ol>
  <li>You submit a market buy of size <code>X</code> with high slippage tolerance.</li>
  <li>Searcher observes it in mempool.</li>
  <li>Searcher buys before you (price up), lets your tx execute higher, sells after.</li>
  <li>Your effective execution worsens by the price impact they created.</li>
</ol>
<p>
Defense is not "use another wallet". Defense is order-flow privacy and
execution discipline.
</p>

<h3>Common mistakes</h3>
<ul>
  <li>Using unlimited slippage "to make sure it fills".</li>
  <li>Ignoring private transaction submission options.</li>
  <li>Treating gas spikes as noise instead of a real-time scarcity market.</li>
</ul>
""",
            },
            "quizzes": [
                {
                    "question_text": {
                        "en": "A sandwich attack typically harms you because:",
                        "fa": "حمله sandwich معمولاً به شما آسیب می‌زند زیرا:",
                        "de": "Ein Sandwich-Angriff schadet typischerweise, weil:",
                    },
                    "question_type": "single_choice",
                    "options": [
                        {"optionId": "a", "text": {"en": "The chain halts", "fa": "زنجیره متوقف می‌شود", "de": "Chain anhält"}},
                        {"optionId": "b", "text": {"en": "Your swap executes against a moved price", "fa": "سوآپ شما مقابل قیمت جابه‌جا شده اجرا می‌شود", "de": "Der Swap gegen bewegten Preis läuft"}},
                        {"optionId": "c", "text": {"en": "Your private key leaks", "fa": "کلید خصوصی لو می‌رود", "de": "Privater Schlüssel leakt"}},
                        {"optionId": "d", "text": {"en": "You pay tax twice", "fa": "دو بار مالیات می‌دهید", "de": "Doppelte Steuer"}},
                    ],
                    "correct_answer": {"option_id": "b"},
                    "explanation": {
                        "en": "Searchers bracket your order flow to capture the impact you pay.",
                        "fa": "سرچ‌ها order flow شما را بسته‌بندی می‌کنند تا impact پرداختی شما را بگیرند.",
                        "de": "Searcher klemmen Ihre Order ein.",
                    },
                    "difficulty": 3,
                    "order": 1,
                },
                {
                    "question_text": {
                        "en": "Best first-line defense against public mempool execution loss:",
                        "fa": "بهترین خط اول دفاع در برابر زیان اجرا در mempool عمومی:",
                        "de": "Beste erste Verteidigung gegen Mempool-Verluste:",
                    },
                    "question_type": "single_choice",
                    "options": [
                        {"optionId": "a", "text": {"en": "Raise slippage tolerance to 50%", "fa": "افزایش تحمل slippage به ۵۰٪", "de": "Slippage auf 50% erhöhen"}},
                        {"optionId": "b", "text": {"en": "Private submission / tighter slippage / slicing", "fa": "ارسال خصوصی / slippage تنگ / خردکردن سفارش", "de": "Private Submission / enge Slippage / Slicing"}},
                        {"optionId": "c", "text": {"en": "Trade only at night", "fa": "فقط شب معامله کنید", "de": "Nur nachts handeln"}},
                        {"optionId": "d", "text": {"en": "Use a new seed phrase per trade", "fa": "هر معامله seed جدید", "de": "Neuer Seed pro Trade"}},
                    ],
                    "correct_answer": {"option_id": "b"},
                    "explanation": {
                        "en": "Limit information leakage and price impact; higher slippage increases attack surface.",
                        "fa": "نشت اطلاعات و price impact را محدود کنید؛ slippage بالا سطح حمله را زیاد می‌کند.",
                        "de": "Informationsleck und Impact begrenzen.",
                    },
                    "difficulty": 3,
                    "order": 2,
                },
                {
                    "question_text": {
                        "en": "A stuck underpriced transaction is primarily a problem of:",
                        "fa": "تراکنش گیرکرده با کارمزد کم در درجه اول مشکل چیست؟",
                        "de": "Eine feststeckende Transaktion ist primär ein Problem von:",
                    },
                    "question_type": "single_choice",
                    "options": [
                        {"optionId": "a", "text": {"en": "Block space scarcity and fee bidding", "fa": "کمیابی فضای بلوک و پیشنهاد کارمزد", "de": "Blockspace-Knappheit und Gebotsverfahren"}},
                        {"optionId": "b", "text": {"en": "Wrong language UI", "fa": "UI با زبان اشتباه", "de": "Falsche UI-Sprache"}},
                        {"optionId": "c", "text": {"en": "Low token market cap", "fa": "مارکت‌کپ پایین توکن", "de": "Niedrige Marktkapitalisierung"}},
                        {"optionId": "d", "text": {"en": "Wallet theme settings", "fa": "تنظیمات تم کیف پول", "de": "Wallet-Theme"}},
                    ],
                    "correct_answer": {"option_id": "a"},
                    "explanation": {
                        "en": "Mempool inclusion is an auction on scarce block space.",
                        "fa": "شامل شدن در mempool حراج فضای بلوک کمیاب است.",
                        "de": "Inklusion ist eine Auktion über Blockspace.",
                    },
                    "difficulty": 2,
                    "order": 3,
                },
            ],
        },
        {
            "slug": "wallets-custody-threat-model",
            "title": "Wallets, Custody, and Threat Models",
            "description": (
                "Hot vs cold, multisig, MPC, hardware devices, approvals, and "
                "operational security for real money."
            ),
            "lesson_type": "practice",
            "order": 6,
            "estimated_minutes": 50,
            "content": {
                "html": """
<h2>Custody is a threat model, not a product category</h2>
<p>
Ask: what can go wrong, who can cause it, and what is the blast radius?
Then choose tools. Labels like "secure wallet" are untestable without a
threat model.
</p>

<h3>Custody architectures</h3>
<table>
  <tr><th>Architecture</th><th>Trust assumption</th><th>Failure mode</th></tr>
  <tr><td>Exchange custody</td><td>Exchange solvency + security</td><td>Hack, freeze, insolvency</td></tr>
  <tr><td>Hot wallet (seed in app)</td><td>Device + user opsec</td><td>Malware, phishing, seed leak</td></tr>
  <tr><td>Hardware wallet</td><td>Device + supply chain + user</td><td>Evil maid, malicious firmware, bad approvals</td></tr>
  <tr><td>Multisig (2-of-3)</td><td>No single key suffices</td><td>Key loss without recovery quorum</td></tr>
  <tr><td>MPC / institutional vault</td><td>Policy engine + share holders</td><td>Policy bugs, collusion of parties</td></tr>
</table>

<h3>Approvals and unlimited allowances</h3>
<p>
On many chains, interacting with a contract can grant spending rights over
your tokens. Unlimited approvals are convenient and dangerous: a later
contract exploit can drain approved tokens without a new signature.
Treat allowances as live risk; revoke when finished.
</p>

<h3>Phishing taxonomy (what actually works)</h3>
<ul>
  <li><strong>Fake support:</strong> DMs asking to "verify seed".</li>
  <li><strong>Fake sites:</strong> typosquats with identical UI requesting approvals.</li>
  <li><strong>Malicious signatures:</strong> human-unreadable permit/order payloads.</li>
  <li><strong>Address poisoning:</strong> dust txs with lookalike addresses in history.</li>
</ul>

<h3>Practice: write your personal custody policy</h3>
<ol>
  <li>Define tiers: spending hot wallet / savings cold / trading venue float.</li>
  <li>Set max per-tiers (e.g., hot ≤ 5% liquid net worth).</li>
  <li>Define recovery: seed backup locations, multisig geographic split.</li>
  <li>Define approval hygiene: revoke weekly; no unlimited where avoidable.</li>
  <li>Define incident runbook: if device suspected compromised → move funds via new seed first, investigate second.</li>
</ol>
<p>
If you cannot answer those five items, you do not have custody — you have
hope.
</p>

<h3>Common mistakes</h3>
<ul>
  <li>Keeping trading capital and life savings in one hot wallet.</li>
  <li>Signing blind payloads because "the dApp asked".</li>
  <li>Reusing the same seed across hot browser extension and "cold" practices.</li>
</ul>
""",
            },
            "quizzes": [
                {
                    "question_text": {
                        "en": "Unlimited token approvals are dangerous mainly because:",
                        "fa": "approvals نامحدود خطرناک‌اند عمدتاً زیرا:",
                        "de": "Unbegrenzte Token-Freigaben sind gefährlich, weil:",
                    },
                    "question_type": "single_choice",
                    "options": [
                        {"optionId": "a", "text": {"en": "They increase gas forever", "fa": "gas را برای همیشه زیاد می‌کنند", "de": "Gas dauerhaft steigt"}},
                        {"optionId": "b", "text": {"en": "A later exploit can spend without a new signature", "fa": "اکسپلویت بعدی بدون امضای جدید می‌تواند خرج کند", "de": "Spätere Exploits ohne neue Signatur ausgeben können"}},
                        {"optionId": "c", "text": {"en": "They change token supply", "fa": "عرضه توکن را عوض می‌کنند", "de": "Angebot ändern"}},
                        {"optionId": "d", "text": {"en": "They hide your address", "fa": "آدرس را مخفی می‌کنند", "de": "Adresse verbergen"}},
                    ],
                    "correct_answer": {"option_id": "b"},
                    "explanation": {
                        "en": "Allowances are standing authorizations; minimize and revoke them.",
                        "fa": "approval مجوز دائمی است؛ کم و باطلشان کنید.",
                        "de": "Freigaben sind Dauerautorisierungen.",
                    },
                    "difficulty": 3,
                    "order": 1,
                },
                {
                    "question_text": {
                        "en": "A 2-of-3 multisig mainly reduces which risk?",
                        "fa": "مالتی‌سیگ ۲-از-۳ عمدتاً کدام ریسک را کم می‌کند؟",
                        "de": "2-of-3 Multisig reduziert primär welches Risiko?",
                    },
                    "question_type": "single_choice",
                    "options": [
                        {"optionId": "a", "text": {"en": "Market volatility", "fa": "نوسان بازار", "de": "Marktvolatilität"}},
                        {"optionId": "b", "text": {"en": "Single key compromise or loss", "fa": "به‌خطر افتادن یا گم‌شدن یک کلید", "de": "Kompromittierung/Verlust eines Schlüssels"}},
                        {"optionId": "c", "text": {"en": "Smart contract price oracles", "fa": "اوراکل قیمت قرارداد هوشمند", "de": "Oracles"}},
                        {"optionId": "d", "text": {"en": "Tax reporting", "fa": "گزارش مالیاتی", "de": "Steuer"}},
                    ],
                    "correct_answer": {"option_id": "b"},
                    "explanation": {
                        "en": "No single key can spend; you must also design recovery or you create a new loss mode.",
                        "fa": "یک کلید به‌تنهایی نمی‌تواند خرج کند؛ بازیابی هم باید طراحی شود.",
                        "de": "Ein Schlüssel genügt nicht; Recovery-Design nötig.",
                    },
                    "difficulty": 2,
                    "order": 2,
                },
                {
                    "question_text": {
                        "en": "If you suspect your device is compromised while holding funds in a hot wallet, first action:",
                        "fa": "اگر مشکوکید دستگاه آلوده است و در کیف پول گرم وجوه دارید، اولین اقدام:",
                        "de": "Bei Verdacht auf kompromittiertes Gerät zuerst:",
                    },
                    "question_type": "single_choice",
                    "options": [
                        {"optionId": "a", "text": {"en": "Post on social media", "fa": "پست در شبکه اجتماعی", "de": "Social Media Post"}},
                        {"optionId": "b", "text": {"en": "Move funds using a clean seed/device before forensics", "fa": "انتقال وجوه با seed/دستگاه تمیز قبل از پزشکی قانونی", "de": "Funds mit sauberem Seed/Device umziehen"}},
                        {"optionId": "c", "text": {"en": "Sign a message to test the key", "fa": "امضای پیام برای تست کلید", "de": "Testnachricht signieren"}},
                        {"optionId": "d", "text": {"en": "Change wallet color theme", "fa": "تغییر تم رنگ کیف پول", "de": "Theme wechseln"}},
                    ],
                    "correct_answer": {"option_id": "b"},
                    "explanation": {
                        "en": "Preserve capital first; investigation can follow after funds are safe.",
                        "fa": "اول سرمایه حفظ شود؛ بررسی بعد از ایمن‌سازی.",
                        "de": "Zuerst Kapital sichern.",
                    },
                    "difficulty": 3,
                    "order": 3,
                },
            ],
        },
        {
            "slug": "exchanges-orderbooks",
            "title": "Exchanges, Order Books, and Execution Basics",
            "description": (
                "Spot vs derivatives venue mechanics, order types, fees, and "
                "counterparty risk for on-ramp and trading."
            ),
            "lesson_type": "theory",
            "order": 7,
            "estimated_minutes": 45,
            "content": {
                "html": """
<h2>Venues are not interchangeable</h2>
<p>
Centralized exchanges (CEX) offer deep books and fiat rails but add
custody and operational counterparty risk. Decentralized venues (DEX)
minimize custody trust but expose you to smart-contract and MEV risk.
Choose venue as a risk decision.
</p>

<h3>Order types that matter</h3>
<ul>
  <li><strong>Market:</strong> immediacy; you pay the spread + impact.</li>
  <li><strong>Limit:</strong> price ceiling/floor; fill is not guaranteed.</li>
  <li><strong>Stop / stop-limit:</strong> conditional triggers; slippage in gaps is real.</li>
  <li><strong>Post-only:</strong> maker-only; avoids taker fees when adding liquidity.</li>
</ul>

<h3>Fee stack</h3>
<p>
Effective cost is not the published maker/taker alone:
<code>cost = fees + spread + impact + funding (if perps) + withdrawal</code>.
A 2 bps fee with 20 bps of impact is not cheap execution.
</p>

<h3>Counterparty checklist (CEX)</h3>
<ul>
  <li>Proof-of-reserves quality (not theater) and liabilities visibility.</li>
  <li>Withdrawal history and halt risk.</li>
  <li>Jurisdiction / legal claim structure.</li>
  <li>Security controls: 2FA type (app/hardware vs SMS), allowlists.</li>
</ul>

<h3>Worked example: splitting an order</h3>
<p>
Buy $250k notional on a book where 2% depth absorbs ~$80k within 15 bps.
A single market order crosses multiple levels. Alternatives: slice into
time buckets, use limit post-only ladders, or RFQ/OTC block if available.
</p>

<h3>Common mistakes</h3>
<ul>
  <li>Comparing CEX/DEX by fee table only.</li>
  <li>Using SMS 2FA on email-linked accounts.</li>
  <li>Holding large idle balances on venues "to be ready".</li>
</ul>
""",
            },
            "quizzes": [
                {
                    "question_text": {
                        "en": "True cost of execution includes:",
                        "fa": "هزینه واقعی اجرا شامل چیست؟",
                        "de": "Wahre Ausführungskosten enthalten:",
                    },
                    "question_type": "single_choice",
                    "options": [
                        {"optionId": "a", "text": {"en": "Only maker/taker fee", "fa": "فقط کارمزد maker/taker", "de": "Nur Maker/Taker"}},
                        {"optionId": "b", "text": {"en": "Fees + spread + impact (+ funding if perps)", "fa": "کارمزد + اسپرد + impact (+ funding در perps)", "de": "Fees + Spread + Impact"}},
                        {"optionId": "c", "text": {"en": "Only network gas", "fa": "فقط gas شبکه", "de": "Nur Gas"}},
                        {"optionId": "d", "text": {"en": "Spread only in bull markets", "fa": "فقط اسپرد در بازار گاوی", "de": "Nur Spread im Bullenmarkt"}},
                    ],
                    "correct_answer": {"option_id": "b"},
                    "explanation": {
                        "en": "Published fees understate real cost when size is material.",
                        "fa": "کارمزد اعلام‌شده با سایز بزرگ هزینه واقعی را دست‌کم می‌گیرد.",
                        "de": "Publizierte Fees unterschätzen echte Kosten.",
                    },
                    "difficulty": 2,
                    "order": 1,
                },
                {
                    "question_text": {
                        "en": "A limit order's key trade-off is:",
                        "fa": "مصالحه اصلی سفارش limit چیست؟",
                        "de": "Der Kerntrade-off einer Limit-Order:",
                    },
                    "question_type": "single_choice",
                    "options": [
                        {"optionId": "a", "text": {"en": "Guaranteed fill at any price", "fa": "تضمین اجرا در هر قیمت", "de": "Garantierte Ausführung"}},
                        {"optionId": "b", "text": {"en": "Price control vs fill certainty", "fa": "کنترل قیمت در برابر قطعیت اجرا", "de": "Preiskontrolle vs. Ausführungssicherheit"}},
                        {"optionId": "c", "text": {"en": "Zero fees always", "fa": "همیشه بدون کارمزد", "de": "Immer null Fees"}},
                        {"optionId": "d", "text": {"en": "No counterparty risk", "fa": "بدون ریسک طرف مقابل", "de": "Kein Gegenparteirisiko"}},
                    ],
                    "correct_answer": {"option_id": "b"},
                    "explanation": {
                        "en": "You set price, but you may miss the move.",
                        "fa": "قیمت را تعیین می‌کنید اما ممکن است حرکت را از دست بدهید.",
                        "de": "Preis ja, Fill nicht garantiert.",
                    },
                    "difficulty": 1,
                    "order": 2,
                },
            ],
        },
        {
            "slug": "scaling-l2-bridges",
            "title": "Scaling, L2s, and Bridge Risk",
            "description": (
                "Why L1s scale poorly, how rollups change the trust model, and "
                "where bridge losses actually come from."
            ),
            "lesson_type": "theory",
            "order": 8,
            "estimated_minutes": 45,
            "content": {
                "html": """
<h2>The scalability trilemma in practice</h2>
<p>
Systems trade off decentralization, security, and throughput. Raising
block size or validator hardware requirements increases throughput and
often reduces the cost of capture. L2 designs try to outsource execution
while inheriting L1 settlement.
</p>

<h3>Rollup intuition</h3>
<ul>
  <li><strong>Optimistic rollups:</strong> post data/state claims; fraud proofs can punish bad state within a challenge window.</li>
  <li><strong>ZK rollups:</strong> post data plus validity proofs; state correctness proven cryptographically.</li>
</ul>
<p>
For a trader, the practical questions are: where is data posted, who can
censor ordering, what is the escape hatch to L1, and how long are exits?
</p>

<h3>Bridge risk anatomy</h3>
<table>
  <tr><th>Risk</th><th>What breaks</th></tr>
  <tr><td>Smart-contract bug</td><td>Locked collateral minted illegally</td></tr>
  <tr><td>Validator/key compromise</td><td>Unauthorized attestation of transfers</td></tr>
  <tr><td>Canonical token confusion</td><td>UI accepts fake wrapped asset</td></tr>
  <tr><td>Upgrade key takeover</td><td>Logic replaced to drain pools</td></tr>
</table>
<p>
Many largest losses in crypto history are bridge failures. Treat bridged
assets as derivative claims with their own credit stack, not "the same
coin".
</p>

<h3>Worked example: reading a bridged asset</h3>
<ul>
  <li>Asset label "USDC" on chain X.</li>
  <li>Actually a bridge wrapper backed by canonical USDC on another chain.</li>
  <li>Trust: bridge contract + signers + message verification + liquidity for exit.</li>
</ul>
<p>
If any layer fails, "USDC" on X can trade away from par. Price it like
paper risk.
</p>

<h3>Common mistakes</h3>
<ul>
  <li>Assuming wrapped assets are as good as native.</li>
  <li>Ignoring exit latency during volatility.</li>
  <li>Using first-time bridges with large size.</li>
</ul>
""",
            },
            "quizzes": [
                {
                    "question_text": {
                        "en": "A bridged 'USDC' on a new chain is best viewed as:",
                        "fa": "«USDC» پل‌زده روی یک زنجیره جدید بهتر دیده می‌شود به‌عنوان:",
                        "de": "Gebridgtes „USDC“ auf neuer Chain ist am besten verstanden als:",
                    },
                    "question_type": "single_choice",
                    "options": [
                        {"optionId": "a", "text": {"en": "Identical to native USDC with zero extra risk", "fa": "کاملاً معادل USDC بومی بدون ریسک اضافه", "de": "Identisch mit nativem USDC"}},
                        {"optionId": "b", "text": {"en": "A claim on canonical USDC via bridge trust assumptions", "fa": "ادعایی بر USDC بومی با فرض‌های اعتماد پل", "de": "Anspruch auf kanonisches USDC mit Bridge-Annahmen"}},
                        {"optionId": "c", "text": {"en": "A new fiat currency", "fa": "ارز فیات جدید", "de": "Neue Fiatwährung"}},
                        {"optionId": "d", "text": {"en": "Always redeemable instantly", "fa": "همیشه فوراً قابل بازخرید", "de": "Immer sofort einlösbar"}},
                    ],
                    "correct_answer": {"option_id": "b"},
                    "explanation": {
                        "en": "Bridged assets carry contract, signer, and liquidity risks of the bridge.",
                        "fa": "دارایی پل‌زده ریسک قرارداد، signers و نقدشوندگی پل را دارد.",
                        "de": "Bridged Assets tragen Bridge-Risiken.",
                    },
                    "difficulty": 3,
                    "order": 1,
                },
                {
                    "question_text": {
                        "en": "Optimistic rollups secure state primarily via:",
                        "fa": "rollup های Optimistic امنیت state را عمدتاً از چه می‌گیرند؟",
                        "de": "Optimistic Rollups sichern State primär durch:",
                    },
                    "question_type": "single_choice",
                    "options": [
                        {"optionId": "a", "text": {"en": "Fraud proofs and a challenge window", "fa": "اثبات تقلب و پنجره اعتراض", "de": "Fraud Proofs und Challenge-Fenster"}},
                        {"optionId": "b", "text": {"en": "Social media consensus", "fa": "consensus شبکه اجتماعی", "de": "Social-Media-Konsens"}},
                        {"optionId": "c", "text": {"en": "Hardware enclaves only", "fa": "فقط enclave سخت‌افزاری", "de": "Nur Enclaves"}},
                        {"optionId": "d", "text": {"en": "Backing by a CEX treasury", "fa": "پشتوانه خزانه صرافی", "de": "CEX-Treasury"}},
                    ],
                    "correct_answer": {"option_id": "a"},
                    "explanation": {
                        "en": "Validity is assumed until challenged; watchers must be able to prove fraud.",
                        "fa": "درستی تا زمان اعتراض فرض می‌شود؛ باید امکان اثبات تقلب باشد.",
                        "de": "Annahme von Validität bis zum Fraud Proof.",
                    },
                    "difficulty": 3,
                    "order": 2,
                },
            ],
        },
    ],
}
