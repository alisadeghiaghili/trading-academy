"""
اسکریپت داده‌های اولیه - ایجاد ماژول‌ها، دروس و آزمون‌ها
Initial seed data for Trading Academy curriculum
"""

import asyncio
import sys
from pathlib import Path
from uuid import uuid4
from datetime import datetime, timezone

sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlalchemy import select
from app.db.session import get_db_context
from app.db.models import Module, Lesson, LessonType, QuizQuestion, UserRole


CURRICULUM = [
    {
        "slug": "crypto-basics",
        "title": "مبانی ارزهای دیجیتال",
        "description": "آشنایی کامل با دنیای ارزهای دیجیتال، بلاکچین، کیف پول‌ها و صرافی‌ها",
        "order": 1,
        "required_tier": "free",
        "lessons": [
            {
                "slug": "what-is-crypto",
                "title": "ارز دیجیتال چیست؟",
                "description": "تعریف ارز دیجیتال، تاریخچه بیت‌کوین و تفاوت با پول سنتی",
                "lesson_type": "theory",
                "order": 1,
                "estimated_minutes": 25,
                "content": {
                    "html": """
                    <h2>ارز دیجیتال چیست؟</h2>
                    <p>ارز دیجیتال (Cryptocurrency) نوعی پول دیجیتال یا مجازی است که از فناوری رمزنگاری برای امنیت استفاده می‌کند و توسط هیچ مرجع مرکزی کنترل نمی‌شود.</p>
                    <h3>ویژگی‌های کلیدی:</h3>
                    <ul>
                        <li><strong>غیرمتمرکز:</strong> بدون نیاز به بانک مرکزی</li>
                        <li><strong>شفاف:</strong> تمام تراکنش‌ها روی بلاکچین قابل مشاهده است</li>
                        <li><strong>امن:</strong> رمزنگاری قوی برای محافظت از تراکنش‌ها</li>
                        <li><strong>جهانی:</strong> بدون محدودیت جغرافیایی</li>
                    </ul>
                    <h3>تاریخچه بیت‌کوین</h3>
                    <p>بیت‌کوین در سال ۲۰۰۹ توسط شخص یا گروهی با نام مستعار «ساتوشی ناکاموتو» ایجاد شد. وایت‌پیپر بیت‌کوین در اکتبر ۲۰۰۸ منتشر شد.</p>
                    <h3>تفاوت با پول سنتی</h3>
                    <table>
                        <tr><th>ویژگی</th><th>پول سنتی</th><th>ارز دیجیتال</th></tr>
                        <tr><td>کنترل</td><td>متمرکز (بانک)</td><td>غیرمتمرکز</td></tr>
                        <tr><td>عرضه</td><td>نامحدود</td><td>محدود (مثلاً BTC: 21M)</td></tr>
                        <tr><td>شفافیت</td><td>محدود</td><td>کامل</td></tr>
                        <tr><td>انتقال</td><td>کند و پرهزینه</td><td>سریع و کم‌هزینه</td></tr>
                    </table>
                    """
                },
                "quizzes": [
                    {
                        "question_text": {"en": "Who created Bitcoin?", "fa": "بیت‌کوین توسط چه کسی ایجاد شد؟", "de": "Wer hat Bitcoin erstellt?"},
                        "question_type": "single_choice",
                        "options": [
                            {"optionId": "a", "text": {"en": "Satoshi Nakamoto", "fa": "ساتوشی ناکاموتو", "de": "Satoshi Nakamoto"}},
                            {"optionId": "b", "text": {"en": "Vitalik Buterin", "fa": "ویتالیک بوترین", "de": "Vitalik Buterin"}},
                            {"optionId": "c", "text": {"en": "Elon Musk", "fa": "ایلان ماسک", "de": "Elon Musk"}},
                            {"optionId": "d", "text": {"en": "Mark Zuckerberg", "fa": "مارک زاکربرگ", "de": "Mark Zuckerberg"}},
                        ],
                        "correct_answer": {"option_id": "a"},
                        "explanation": {"en": "Bitcoin was created by Satoshi Nakamoto in 2009.", "fa": "بیت‌کوین در سال ۲۰۰۹ توسط ساتوشی ناکاموتو ایجاد شد.", "de": "Bitcoin wurde 2009 von Satoshi Nakamoto erstellt."},
                        "difficulty": 1,
                        "order": 1,
                    },
                    {
                        "question_text": {"en": "What is the maximum supply of Bitcoin?", "fa": "حداکثر عرضه بیت‌کوین چقدر است؟", "de": "Was ist das maximale Angebot an Bitcoin?"},
                        "question_type": "single_choice",
                        "options": [
                            {"optionId": "a", "text": {"en": "21 million", "fa": "۲۱ میلیون", "de": "21 Millionen"}},
                            {"optionId": "b", "text": {"en": "100 million", "fa": "۱۰۰ میلیون", "de": "100 Millionen"}},
                            {"optionId": "c", "text": {"en": "Unlimited", "fa": "نامحدود", "de": "Unbegrenzt"}},
                            {"optionId": "d", "text": {"en": "1 billion", "fa": "۱ میلیارد", "de": "1 Milliarde"}},
                        ],
                        "correct_answer": {"option_id": "a"},
                        "explanation": {"en": "Bitcoin has a fixed supply of 21 million coins.", "fa": "بیت‌کوین عرضه ثابت ۲۱ میلیون سکه دارد.", "de": "Bitcoin hat ein festes Angebot von 21 Millionen Münzen."},
                        "difficulty": 1,
                        "order": 2,
                    },
                ],
            },
            {
                "slug": "blockchain-explained",
                "title": "بلاکچین چگونه کار می‌کند؟",
                "description": "ساختار بلاکچین، ماینینگ، اجماع و انواع شبکه‌ها",
                "lesson_type": "theory",
                "order": 2,
                "estimated_minutes": 30,
                "content": {
                    "html": """
                    <h2>بلاکچین چیست؟</h2>
                    <p>بلاکچین یک دفتر کل توزیع‌شده است که تراکنش‌ها را به صورت امن و غیرقابل تغییر ثبت می‌کند. هر «بلوک» شامل مجموعه‌ای از تراکنش‌هاست و به بلوک قبلی زنجیر شده است.</p>
                    <h3>مراحل تأیید تراکنش:</h3>
                    <ol>
                        <li>کاربر تراکنش را ارسال می‌کند</li>
                        <li>تراکنش در شبکه پخش می‌شود (Mempool)</li>
                        <li>ماینرها/والیدیتورها تراکنش را تأیید می‌کنند</li>
                        <li>تراکنش در بلوک جدید قرار می‌گیرد</li>
                        <li>بلوک به زنجیره اضافه می‌شود</li>
                        <li>تراکنش نهایی و غیرقابل تغییر است</li>
                    </ol>
                    <h3>روش‌های اجماع:</h3>
                    <table>
                        <tr><th>روش</th><th>نمونه</th><th>مزایا</th><th>معایب</th></tr>
                        <tr><td>PoW (اثبات کار)</td><td>بیت‌کوین</td><td>امنیت بالا</td><td>مصرف انرژی</td></tr>
                        <tr><td>PoS (اثبات سهام)</td><td>اتریوم ۲</td><td>کم‌مصرف</td><td>تمرکز ثروت</td></tr>
                        <tr><td>DPoS</td><td>EOS, TRON</td><td>سریع</td><td>تمرکز بیشتر</td></tr>
                    </table>
                    """
                },
                "quizzes": [
                    {
                        "question_text": {"en": "What does PoW stand for?", "fa": "PoW مخفف چیست؟", "de": "Wofür steht PoW?"},
                        "question_type": "single_choice",
                        "options": [
                            {"optionId": "a", "text": {"en": "Proof of Work", "fa": "اثبات کار", "de": "Proof of Work"}},
                            {"optionId": "b", "text": {"en": "Proof of Wealth", "fa": "اثبات ثروت", "de": "Proof of Wealth"}},
                            {"optionId": "c", "text": {"en": "Proof of Wallet", "fa": "اثبات کیف پول", "de": "Proof of Wallet"}},
                            {"optionId": "d", "text": {"en": "Proof of Stake", "fa": "اثبات سهام", "de": "Proof of Stake"}},
                        ],
                        "correct_answer": {"option_id": "a"},
                        "explanation": {"en": "PoW stands for Proof of Work - used by Bitcoin.", "fa": "PoW مخفف Proof of Work (اثبات کار) است که بیت‌کوین از آن استفاده می‌کند.", "de": "PoW steht für Proof of Work - wird von Bitcoin verwendet."},
                        "difficulty": 1,
                        "order": 1,
                    },
                ],
            },
            {
                "slug": "wallets-and-security",
                "title": "کیف پول‌ها و امنیت",
                "description": "انواع کیف پول، کلیدهای خصوصی و عمومی، و نحوه محافظت از دارایی",
                "lesson_type": "theory",
                "order": 3,
                "estimated_minutes": 35,
                "content": {
                    "html": """
                    <h2>کیف پول ارز دیجیتال</h2>
                    <p>کیف پول ارز دیجیتال ابزاری برای ذخیره، ارسال و دریافت ارزهای دیجیتال است. کیف پول‌ها کلیدهای خصوصی شما را مدیریت می‌کنند.</p>
                    <h3>انواع کیف پول:</h3>
                    <table>
                        <tr><th>نوع</th><th>نمونه</th><th>امنیت</th><th>کاربرد</th></tr>
                        <tr><td>سخت‌افزاری (Hardware)</td><td>Ledger, Trezor</td><td>بالاترین</td><td>نگهداری بلندمدت</td></tr>
                        <tr><td>نرم‌افزاری دسکتاپ</td><td>Electrum, Exodus</td><td>بالا</td><td>معامله‌گری</td></tr>
                        <tr><td>موبایل</td><td>Trust Wallet, MetaMask</td><td>متوسط</td><td>روزانه</td></tr>
                        <tr><td>تحت وب</td><td>Binance, Coinbase</td><td>متوسط</td><td>معامله در صرافی</td></tr>
                        <tr><td>کاغذی (Paper)</td><td>QR Code چاپی</td><td>بالا</td><td>ذخیره سرد</td></tr>
                    </table>
                    <h3>کلید خصوصی vs کلید عمومی:</h3>
                    <ul>
                        <li><strong>کلید عمومی:</strong> مانند شماره حساب بانکی - برای دریافت ارز استفاده می‌شود</li>
                        <li><strong>کلید خصوصی:</strong> مانند رمز کارت بانکی - برای ارسال ارز ضروری است و نباید با کسی به اشتراک گذاشته شود</li>
                    </ul>
                    <h3>نکات امنیتی حیاتی:</h3>
                    <ol>
                        <li>هرگز کلید خصوصی خود را با کسی به اشتراک نگذارید</li>
                        <li>از کیف پول سخت‌افزاری برای مبالغ زیاد استفاده کنید</li>
                        <li>Backup (بکاپ) از Seed Phrase تهیه کنید</li>
                        <li>از احراز هویت دومرحله‌ای (2FA) استفاده کنید</li>
                        <li>از WiFi عمومی برای معاملات استفاده نکنید</li>
                    </ol>
                    """
                },
                "quizzes": [
                    {
                        "question_text": {"en": "Which wallet type has the highest security?", "fa": "کدام نوع کیف پول بیشترین امنیت را دارد؟", "de": "Welche Wallet-Typ hat die höchste Sicherheit?"},
                        "question_type": "single_choice",
                        "options": [
                            {"optionId": "a", "text": {"en": "Hardware wallet", "fa": "کیف پول سخت‌افزاری", "de": "Hardware Wallet"}},
                            {"optionId": "b", "text": {"en": "Web wallet", "fa": "کیف پول تحت وب", "de": "Web Wallet"}},
                            {"optionId": "c", "text": {"en": "Mobile wallet", "fa": "کیف پول موبایل", "de": "Mobile Wallet"}},
                            {"optionId": "d", "text": {"en": "Exchange wallet", "fa": "کیف پول صرافی", "de": "Exchange Wallet"}},
                        ],
                        "correct_answer": {"option_id": "a"},
                        "explanation": {"en": "Hardware wallets store private keys offline, making them the most secure option.", "fa": "کیف پول‌های سخت‌افزاری کلیدهای خصوصی را آفلاین نگهداری می‌کنند و امن‌ترین گزینه هستند.", "de": "Hardware Wallets speichern Private Keys offline und sind daher die sicherste Option."},
                        "difficulty": 1,
                        "order": 1,
                    },
                    {
                        "question_text": {"en": "What should you NEVER share with anyone?", "fa": "چه چیزی را نباید هرگز با کسی به اشتراک بگذارید؟", "de": "Was sollten Sie niemals mit jemandem teilen?"},
                        "question_type": "single_choice",
                        "options": [
                            {"optionId": "a", "text": {"en": "Private key", "fa": "کلید خصوصی", "de": "Private Key"}},
                            {"optionId": "b", "text": {"en": "Public address", "fa": "آدرس عمومی", "de": "Öffentliche Adresse"}},
                            {"optionId": "c", "text": {"en": "Portfolio balance", "fa": "موجودی پرتفوی", "de": "Portfolio-Guthaben"}},
                            {"optionId": "d", "text": {"en": "Trading strategy", "fa": "استراتژی معاملاتی", "de": "Handelsstrategie"}},
                        ],
                        "correct_answer": {"option_id": "a"},
                        "explanation": {"en": "Your private key gives full control over your funds. Never share it.", "fa": "کلید خصوصی کنترل کامل بر دارایی‌های شما را فراهم می‌کند. هرگز آن را به اشتراک نگذارید.", "de": "Der Private Key gibt vollständige Kontrolle über Ihre Mittel. Teilen Sie ihn niemals."},
                        "difficulty": 1,
                        "order": 2,
                    },
                ],
            },
            {
                "slug": "exchanges-guide",
                "title": "صرافی‌های ارز دیجیتال",
                "description": "نحوه انتخاب صرافی، KYC، انواع سفارشات و مقایسه صرافی‌ها",
                "lesson_type": "theory",
                "order": 4,
                "estimated_minutes": 30,
                "content": {
                    "html": """
                    <h2>صرافی ارز دیجیتال چیست؟</h2>
                    <p>صرافی ارز دیجیتال پلتفرمی است که در آن می‌توانید ارزهای دیجیتال را بخرید، بفروشید یا مبادله کنید.</p>
                    <h3>انواع صرافی:</h3>
                    <ul>
                        <li><strong>متمرکز (CEX):</strong> بایننس، کوین‌بیس، کراکن - نیاز به KYC، نقدشوندگی بالا</li>
                        <li><strong>غیرمتمرکز (DEX):</strong> یونی‌سواپ، سوشی‌سواپ - بدون KYC، نقدشوندگی متغیر</li>
                    </ul>
                    <h3>انواع سفارشات:</h3>
                    <table>
                        <tr><th>نوع سفارش</th><th>توضیح</th><th>کاربرد</th></tr>
                        <tr><td>Market (بازار)</td><td>خرید/فروش فوری با قیمت فعلی</td><td>سرعت بالا</td></tr>
                        <tr><td>Limit (محدود)</td><td>خرید/فروش در قیمت مشخص</td><td>کنترل قیمت</td></tr>
                        <tr><td>Stop-Loss (حد ضرر)</td><td>فروش خودکار در قیمت مشخص</td><td>مدیریت ریسک</td></tr>
                        <tr><td>Stop-Limit</td><td>ترکیب Stop و Limit</td><td>کنترل دقیق‌تر</td></tr>
                    </table>
                    <h3>معیارهای انتخاب صرافی:</h3>
                    <ol>
                        <li>امنیت و سابقه هک</li>
                        <li>نقدشوندگی (حجم معاملات)</li>
                        <li>کارمزدها</li>
                        <li>تنوع جفت‌ارزها</li>
                        <li>پشتیبانی از فیات</li>
                        <li>رابط کاربری</li>
                    </ol>
                    """
                },
                "quizzes": [
                    {
                        "question_text": {"en": "What type of order fills immediately at the current price?", "fa": "کدام نوع سفارش فوراً با قیمت فعلی اجرا می‌شود؟", "de": "Welche Ordertyp wird sofort zum aktuellen Preis ausgeführt?"},
                        "question_type": "single_choice",
                        "options": [
                            {"optionId": "a", "text": {"en": "Market order", "fa": "سفارش بازار", "de": "Marktorder"}},
                            {"optionId": "b", "text": {"en": "Limit order", "fa": "سفارش محدود", "de": "Limit-Order"}},
                            {"optionId": "c", "text": {"en": "Stop-loss order", "fa": "سفارش حد ضرر", "de": "Stop-Loss-Order"}},
                            {"optionId": "d", "text": {"en": "Stop-limit order", "fa": "سفارش حد ضرر محدود", "de": "Stop-Limit-Order"}},
                        ],
                        "correct_answer": {"option_id": "a"},
                        "explanation": {"en": "A market order executes immediately at the best available price.", "fa": "سفارش بازار فوراً با بهترین قیمت موجود اجرا می‌شود.", "de": "Eine Marktorder wird sofort zum besten verfügbaren Preis ausgeführt."},
                        "difficulty": 1,
                        "order": 1,
                    },
                ],
            },
        ],
    },
    {
        "slug": "technical-analysis",
        "title": "تحلیل تکنیکال",
        "description": "یادگیری اندیکاتورها، الگوهای نموداری و استراتژی‌های معاملاتی",
        "order": 2,
        "required_tier": "free",
        "lessons": [
            {
                "slug": "candlestick-patterns",
                "title": "الگوهای کندل‌استیک",
                "description": "آشنایی با کندل‌های ژاپنی و الگوهای مهم قیمتی",
                "lesson_type": "theory",
                "order": 1,
                "estimated_minutes": 40,
                "content": {
                    "html": """
                    <h2>کندل‌استیک ژاپنی</h2>
                    <p>کندل‌استیک‌ها اطلاعات چهار قیمت (باز، بالا، پایین، بسته) را در یک بازه زمانی نشان می‌دهند.</p>
                    <h3>اجزای کندل:</h3>
                    <ul>
                        <li><strong>بدنه (Body):</strong> فاصله بین قیمت باز و بسته</li>
                        <li><strong>سایه بالا (Upper Wick):</strong> بالاترین قیمت</li>
                        <li><strong>سایه پایین (Lower Wick):</strong> پایین‌ترین قیمت</li>
                    </ul>
                    <h3>الگوهای مهم:</h3>
                    <table>
                        <tr><th>الگو</th><th>نوع</th><th>سیگنال</th></tr>
                        <tr><td>چکش (Hammer)</td><td>برگشتی</td><td>صعودی</td></tr>
                        <tr><td>ستاره تیرانداز (Shooting Star)</td><td>برگشتی</td><td>نزولی</td></tr>
                        <tr><td>صعودی (Bullish Engulfing)</td><td>برگشتی</td><td>صعودی</td></tr>
                        <tr><td>نزولی (Bearish Engulfing)</td><td>برگشتی</td><td>نزولی</td></tr>
                        <tr><td>دوجی (Doji)</td><td>بی‌تصمیمی</td><td>خنثی</td></tr>
                    </table>
                    """
                },
                "quizzes": [
                    {
                        "question_text": {"en": "A Hammer candlestick pattern is typically:", "fa": "الگوی کندل چکش معمولاً:", "de": "Ein Hammer-Kerzenmuster ist typischerweise:"},
                        "question_type": "single_choice",
                        "options": [
                            {"optionId": "a", "text": {"en": "Bullish reversal", "fa": "برگشت صعودی", "de": "Bullische Umkehr"}},
                            {"optionId": "b", "text": {"en": "Bearish reversal", "fa": "برگشت نزولی", "de": "Bärische Umkehr"}},
                            {"optionId": "c", "text": {"en": "Neutral", "fa": "خنثی", "de": "Neutral"}},
                            {"optionId": "d", "text": {"en": "Continuation", "fa": "ادامه روند", "de": "Fortsetzung"}},
                        ],
                        "correct_answer": {"option_id": "a"},
                        "explanation": {"en": "A Hammer at the bottom of a downtrend signals potential bullish reversal.", "fa": "چکش در انتهای روند نزولی نشان‌دهنده برگشت احتمالی صعودی است.", "de": "Ein Hammer am Ende eines Abwärtstrends signalisiert eine potenzielle bullische Umkehr."},
                        "difficulty": 2,
                        "order": 1,
                    },
                ],
            },
            {
                "slug": "indicators-rsi-macd",
                "title": "اندیکاتورهای RSI و MACD",
                "description": "نحوه استفاده از اسیلاتورها برای تشخیص نقاط ورود و خروج",
                "lesson_type": "theory",
                "order": 2,
                "estimated_minutes": 35,
                "content": {
                    "html": """
                    <h2>اندیکاتور RSI (شاخص قدرت نسبی)</h2>
                    <p>RSI بین ۰ تا ۱۰۰ نوسان می‌کند و شرایط اشباع خرید/فروش را نشان می‌دهد.</p>
                    <ul>
                        <li>RSI بالای ۷۰: اشباع خرید (سیگنال فروش احتمالی)</li>
                        <li>RSI زیر ۳۰: اشباع فروش (سیگنال خرید احتمالی)</li>
                        <li>RSI بالای ۵۰: روند صعودی</li>
                        <li>RSI زیر ۵۰: روند نزولی</td></tr>
                    </ul>
                    <h2>اندیکاتور MACD</h2>
                    <p>MACD از سه خط تشکیل شده:</p>
                    <ul>
                        <li><strong>MACD Line:</strong> تفاوت EMA ۱۲ و EMA ۲۶</li>
                        <li><strong>Signal Line:</strong> EMA ۹ خط MACD</li>
                        <li><strong>Histogram:</strong> تفاوت MACD و Signal</li>
                    </ul>
                    <h3>سیگنال‌ها:</h3>
                    <ul>
                        <li>عبور MACD از Signal به بالا: سیگنال خرید</li>
                        <li>عبور MACD از Signal به پایین: سیگنال فروش</li>
                    </ul>
                    """
                },
                "quizzes": [
                    {
                        "question_text": {"en": "RSI above 70 typically indicates:", "fa": "RSI بالای ۷۰ معمولاً نشان‌دهنده:", "de": "RSI über 70 zeigt typischerweise:"},
                        "question_type": "single_choice",
                        "options": [
                            {"optionId": "a", "text": {"en": "Overbought conditions", "fa": "شرایط اشباع خرید", "de": "Überkaufte Bedingungen"}},
                            {"optionId": "b", "text": {"en": "Oversold conditions", "fa": "شرایط اشباع فروش", "de": "Überverkaufte Bedingungen"}},
                            {"optionId": "c", "text": {"en": "Strong uptrend", "fa": "روند صعودی قوی", "de": "Starker Aufwärtstrend"}},
                            {"optionId": "d", "text": {"en": "No signal", "fa": "بدون سیگنال", "de": "Kein Signal"}},
                        ],
                        "correct_answer": {"option_id": "a"},
                        "explanation": {"en": "RSI above 70 suggests the asset may be overbought and due for a pullback.", "fa": "RSI بالای ۷۰ نشان می‌دهد دارایی ممکن است بیش از حد خریداری شده باشد.", "de": "RSI über 70 deutet darauf hin, dass der Vermögenswert überkauft sein könnte."},
                        "difficulty": 2,
                        "order": 1,
                    },
                ],
            },
        ],
    },
    {
        "slug": "risk-management",
        "title": "مدیریت ریسک و سرمایه",
        "description": "استراتژی‌های مدیریت ریسک، سایزبندی موقعیت و حفظ سرمایه",
        "order": 3,
        "required_tier": "free",
        "lessons": [
            {
                "slug": "position-sizing",
                "title": "سایزبندی موقعیت",
                "description": "روش‌های تعیین حجم معامله و محدود کردن ریسک هر معامله",
                "lesson_type": "theory",
                "order": 1,
                "estimated_minutes": 30,
                "content": {
                    "html": """
                    <h2>سایزبندی موقعیت چیست؟</h2>
                    <p>سایزبندی موقعیت تعیین می‌کند که چه مقدار از سرمایه خود را در هر معامله ریسک کنید.</p>
                    <h3>روش کسر ثابت (Fixed Fractional):</h3>
                    <p>در این روش، درصد ثابتی از سرمایه را در هر معامله ریسک می‌کنید (معمولاً ۱-۲٪).</p>
                    <h3>فرمول محاسبه:</h3>
                    <p><code>حجم موقعیت = (سرمایه × درصد ریسک) / فاصله حد ضرر</code></p>
                    <h3>مثال عملی:</h3>
                    <ul>
                        <li>سرمایه: $۱۰,۰۰۰</li>
                        <li>ریسک هر معامله: ۲٪ = $۲۰۰</li>
                        <li>قیمت ورود: $۵۰,۰۰۰ (بیت‌کوین)</li>
                        <li>حد ضرر: $۴۹,۰۰۰ (فاصله: $۱,۰۰۰)</li>
                        <li>حجم = $۲۰۰ / $۱,۰۰۰ = ۰.۲ BTC</li>
                    </ul>
                    <h3>قانون ۲٪:</h3>
                    <p>هرگز بیش از ۲٪ از کل سرمایه را در یک معامله واحد ریسک نکنید. این قانون از شما در برابر ضررهای بزرگ محافظت می‌کند.</p>
                    """
                },
                "quizzes": [
                    {
                        "question_text": {"en": "If your capital is $10,000 and you risk 2% per trade, what is your max risk per trade?", "fa": "اگر سرمایه شما ۱۰,۰۰۰ دلار باشد و ۲٪ در هر معامله ریسک کنید، حداکثر ریسک هر معامله چقدر است؟", "de": "Wenn Ihr Kapital 10.000 $ beträgt und Sie 2% pro Trade riskieren, was ist Ihr maximales Risiko pro Trade?"},
                        "question_type": "single_choice",
                        "options": [
                            {"optionId": "a", "text": {"en": "$200", "fa": "۲۰۰ دلار", "de": "200 $"}},
                            {"optionId": "b", "text": {"en": "$2,000", "fa": "۲,۰۰۰ دلار", "de": "2.000 $"}},
                            {"optionId": "c", "text": {"en": "$500", "fa": "۵۰۰ دلار", "de": "500 $"}},
                            {"optionId": "d", "text": {"en": "$100", "fa": "۱۰۰ دلار", "de": "100 $"}},
                        ],
                        "correct_answer": {"option_id": "a"},
                        "explanation": {"en": "$10,000 × 2% = $200 maximum risk per trade.", "fa": "۱۰,۰۰۰ × ۲٪ = ۲۰۰ دلار حداکثر ریسک هر معامله.", "de": "10.000 $ × 2% = 200 $ maximales Risiko pro Trade."},
                        "difficulty": 2,
                        "order": 1,
                    },
                ],
            },
            {
                "slug": "risk-reward-ratio",
                "title": "نسبت ریسک به ریوارد",
                "description": "چگونه با نسبت R:R سودآوری معاملات خود را افزایش دهید",
                "lesson_type": "theory",
                "order": 2,
                "estimated_minutes": 25,
                "content": {
                    "html": """
                    <h2>نسبت ریسک به ریوارد (R:R)</h2>
                    <p>این نسبت نشان می‌دهد در برابر هر واحد ریسک، چند واحد سود انتظار دارید.</p>
                    <h3>فرمول:</h3>
                    <p><code>R:R = (قیمت هدف - قیمت ورود) / (قیمت ورود - حد ضرر)</code></p>
                    <h3>مثال:</h3>
                    <ul>
                        <li>قیمت ورود: $۵۰,۰۰۰</li>
                        <li>حد ضرر: $۴۹,۰۰۰ (ریسک: $۱,۰۰۰)</li>
                        <li>هدف سود: $۵۳,۰۰۰ (ریوارد: $۳,۰۰۰)</li>
                        <li>نسبت R:R = ۳,۰۰۰/۱,۰۰۰ = ۱:۳</li>
                    </ul>
                    <h3>چرا R:R مهم است؟</h3>
                    <p>با نسبت ۱:۳ حتی با نرخ برد ۴۰٪ هم سودآور هستید:</p>
                    <ul>
                        <li>۴۰ معامله برد × $۳,۰۰۰ = $۱۲۰,۰۰۰</li>
                        <li>۶۰ معامله باخت × $۱,۰۰۰ = $۶۰,۰۰۰</li>
                        <li>سود خالص = $۶۰,۰۰۰</li>
                    </ul>
                    """
                },
                "quizzes": [
                    {
                        "question_text": {"en": "What is the minimum recommended R:R ratio for most strategies?", "fa": "حداقل نسبت R:R توصیه‌شده برای اکثر استراتژی‌ها چقدر است؟", "de": "Was ist das empfohlene minimale R:R-Verhältnis für die meisten Strategien?"},
                        "question_type": "single_choice",
                        "options": [
                            {"optionId": "a", "text": {"en": "1:2", "fa": "۱:۲", "de": "1:2"}},
                            {"optionId": "b", "text": {"en": "1:1", "fa": "۱:۱", "de": "1:1"}},
                            {"optionId": "c", "text": {"en": "1:5", "fa": "۱:۵", "de": "1:5"}},
                            {"optionId": "d", "text": {"en": "2:1", "fa": "۲:۱", "de": "2:1"}},
                        ],
                        "correct_answer": {"option_id": "a"},
                        "explanation": {"en": "A minimum 1:2 R:R ratio ensures profitability even with a moderate win rate.", "fa": "نسبت حداقل ۱:۲ سودآوری را حتی با نرخ برد متوسط تضمین می‌کند.", "de": "Ein minimales R:R-Verhältnis von 1:2 stellt selbst bei moderater Trefferquote Rentabilität sicher."},
                        "difficulty": 2,
                        "order": 1,
                    },
                ],
            },
        ],
    },
    {
        "slug": "fundamental-analysis",
        "title": "تحلیل بنیادی",
        "description": "بررسی وایت‌پیپر، تیم، توکنومیکس و ارزش‌گذاری پروژه‌ها",
        "order": 4,
        "required_tier": "pro",
        "lessons": [
            {
                "slug": "whitepaper-analysis",
                "title": "تحلیل وایت‌پیپر",
                "description": "نحوه خواندن و تحلیل وایت‌پیپر پروژه‌های ارز دیجیتال",
                "lesson_type": "theory",
                "order": 1,
                "estimated_minutes": 40,
                "content": {
                    "html": """
                    <h2>وایت‌پیپر چیست؟</h2>
                    <p>وایت‌پیپر سندی است که فناوری، اهداف و نقشه راه یک پروژه ارز دیجیتال را توضیح می‌دهد.</p>
                    <h3>منابع معتبر برای دریافت وایت‌پیپر:</h3>
                    <ul>
                        <li><strong>وبسایت رسمی پروژه:</strong> معمولاً در بخش Docs یا Whitepaper</li>
                        <li><strong>CoinGecko / CoinMarketCap:</strong> لینک وایت‌پیپر هر توکن</li>
                        <li><strong>GitHub:</strong> برای پروژه‌های متن‌باز</li>
                        <li><strong>Bitcointalk:</strong> برای پروژه‌های قدیمی</li>
                    </ul>
                    <h3>آنچه باید در وایت‌پیپر بررسی کنید:</h3>
                    <ol>
                        <li><strong>مشکل و راه‌حل:</strong> پروژه چه مشکلی را حل می‌کند؟</li>
                        <li><strong>فناوری:</strong> آیا فناوری نوآورانه‌ای دارد؟</li>
                        <li><strong>تیم:</strong> چه کسانی پشت پروژه هستند؟</li>
                        <li><strong>توکنومیکس:</strong> عرضه، تقاضا و مکانیزم توکن</li>
                        <li><strong>نقشه راه:</strong> اهداف و زمان‌بندی توسعه</li>
                        <li><strong>رقبا:</strong> رقبای اصلی و مزیت رقابتی</li>
                    </ol>
                    """
                },
                "quizzes": [
                    {
                        "question_text": {"en": "Where can you typically find a project's whitepaper?", "fa": "وایت‌پیپر یک پروژه معمولاً کجا یافت می‌شود؟", "de": "Wo finden Sie typischerweise das Whitepaper eines Projekts?"},
                        "question_type": "single_choice",
                        "options": [
                            {"optionId": "a", "text": {"en": "Project's official website", "fa": "وبسایت رسمی پروژه", "de": "Offizielle Website des Projekts"}},
                            {"optionId": "b", "text": {"en": "Twitter", "fa": "توییتر", "de": "Twitter"}},
                            {"optionId": "c", "text": {"en": "Reddit", "fa": "ردیت", "de": "Reddit"}},
                            {"optionId": "d", "text": {"en": "Discord", "fa": "دیسکورد", "de": "Discord"}},
                        ],
                        "correct_answer": {"option_id": "a"},
                        "explanation": {"en": "The official website is the primary source for whitepapers. CoinGecko and CoinMarketCap also link to them.", "fa": "وبسایت رسمی منبع اصلی وایت‌پیپرهاست. CoinGecko و CoinMarketCap نیز لینک آن را ارائه می‌دهند.", "de": "Die offizielle Website ist die primäre Quelle für Whitepaper. CoinGecko und CoinMarketCap verlinken ebenfalls darauf."},
                        "difficulty": 2,
                        "order": 1,
                    },
                ],
            },
        ],
    },
    {
        "slug": "portfolio-management",
        "title": "مدیریت پرتفوی",
        "description": "تنوع‌بخشی، تخصیص دارایی و بهینه‌سازی پرتفوی",
        "order": 5,
        "required_tier": "pro",
        "lessons": [
            {
                "slug": "diversification",
                "title": "تنوع‌بخشی دارایی‌ها",
                "description": "چگونه پرتفوی متنوع بسازید تا ریسک را کاهش دهید",
                "lesson_type": "theory",
                "order": 1,
                "estimated_minutes": 30,
                "content": {
                    "html": """
                    <h2>تنوع‌بخشی چیست؟</h2>
                    <p>تنوع‌بخشی یعنی سرمایه خود را بین دارایی‌های مختلف تقسیم کنید تا ریسک کلی پرتفوی کاهش یابد.</p>
                    <h3>اصول تنوع‌بخشی در کریپتو:</h3>
                    <ol>
                        <li><strong>تنوع در دسته‌بندی‌ها:</strong> L1 (بیت‌کوین، اتریوم)، DeFi، Gaming، Layer2</li>
                        <li><strong>تنوع در اندازه:</strong> Large-cap (BTC, ETH)، Mid-cap، Small-cap</li>
                        <li><strong>تنوع زمانی:</strong> DCA (میانگین‌گیری هزینه دلاری)</li>
                        <li><strong>تنوع جغرافیایی:</strong> پروژه‌های مختلف از مناطق مختلف</li>
                    </ol>
                    <h3>نمونه پرتفوی متنوع:</h3>
                    <table>
                        <tr><th>دسته</th><th>درصد</th><th>نمونه</th></tr>
                        <tr><td>Bitcoin</td><td>۴۰٪</td><td>BTC</td></tr>
                        <tr><td>Ethereum</td><td>۲۵٪</td><td>ETH</td></tr>
                        <tr><td>Layer 2 / Alt L1</td><td>۲۰٪</td><td>SOL, MATIC, AVAX</td></tr>
                        <tr><td>DeFi</td><td>۱۰٪</td><td>UNI, AAVE, COMP</td></tr>
                        <tr><td>Cash / Stablecoins</td><td>۵٪</td><td>USDT, USDC</td></tr>
                    </table>
                    """
                },
                "quizzes": [
                    {
                        "question_text": {"en": "What is the main benefit of portfolio diversification?", "fa": "مزیت اصلی تنوع‌بخشی پرتفوی چیست؟", "de": "Was ist der Hauptvorteil der Portfolio-Diversifikation?"},
                        "question_type": "single_choice",
                        "options": [
                            {"optionId": "a", "text": {"en": "Reduces overall risk", "fa": "کاهش ریسک کلی", "de": "Reduziert das Gesamtrisiko"}},
                            {"optionId": "b", "text": {"en": "Guarantees profits", "fa": "تضمین سود", "de": "Garantiert Gewinne"}},
                            {"optionId": "c", "text": {"en": "Increases maximum returns", "fa": "افزایش حداکثر بازده", "de": "Erhöht die maximalen Renditen"}},
                            {"optionId": "d", "text": {"en": "Eliminates all losses", "fa": "حذف تمام ضررها", "de": "Beseitigt alle Verluste"}},
                        ],
                        "correct_answer": {"option_id": "a"},
                        "explanation": {"en": "Diversification reduces risk by spreading investments across different assets.", "fa": "تنوع‌بخشی ریسک را با تقسیم سرمایه‌گذاری بین دارایی‌های مختلف کاهش می‌دهد.", "de": "Diversifikation reduziert das Risiko durch die Streuung von Investitionen über verschiedene Anlagen."},
                        "difficulty": 2,
                        "order": 1,
                    },
                ],
            },
        ],
    },
]


async def seed_data():
    """Populate database with curriculum content."""
    print("🌱 Starting database seed...")

    async with get_db_context() as db:
        # Check if data already exists
        result = await db.execute(select(Module).limit(1))
        if result.scalar_one_or_none():
            print("⚠️  Modules already exist. Skipping seed.")
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
            print(f"📚 Created module: {module_data['title']}")

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
                print(f"  📖 Created lesson: {lesson_data['title']}")

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
                    print(f"    ❓ Added quiz question")

        await db.commit()
        print("\n✅ Database seeded successfully!")
        print(f"   Modules: {len(CURRICULUM)}")
        total_lessons = sum(len(m["lessons"]) for m in CURRICULUM)
        total_quizzes = sum(
            len(l.get("quizzes", []))
            for m in CURRICULUM
            for l in m["lessons"]
        )
        print(f"   Lessons: {total_lessons}")
        print(f"   Quiz questions: {total_quizzes}")


if __name__ == "__main__":
    asyncio.run(seed_data())
    # Also seed gamification data
    from app.seed_gamification import seed_gamification
    asyncio.run(seed_gamification())
