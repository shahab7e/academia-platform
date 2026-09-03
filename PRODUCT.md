# Product

<!-- impeccable:product-schema 1 -->

## Platform

web

## Users

Two audiences share the same platform:

- **Individual students** preparing for Iran's Konkur (national university entrance exam) and school exams in mathematics, probability & statistics, and discrete mathematics. They register directly, buy courses/tests/collections from the shop, take timed practice tests, attend live classes, and get AI-assisted support via tickets.
- **Partner schools/institutions** (e.g. Alpha School, Baharestan High School, Hanan school complex, Hadaf publications/کنکور هدف, Salam Schools complex, Neshane Rasa, Roshangaran High School, Shafie Scientific-Educational Foundation, Olame Tabatabaei) — institutional customers whose students use the platform under their own arrangement, distinct from individual retail sign-ups.

## Product Purpose

Deliver Arian Tafazolizadeh's personal mathematics instruction — course delivery, live classes, VOD recordings, a test-maker/practice-test engine, an e-commerce shop for courses and materials, and AI-assisted student support — to both individual Konkur/exam-prep students and partner-school cohorts. Success is students actually improving exam performance and partner schools trusting the platform enough to route their own students through it.

## Positioning

The product **is** Arian Tafazolizadeh's own teaching, not an anonymous content mill. Unlike broad Iranian Konkur-prep publishers (e.g. Kanoon, Gaj-style catalogs), the differentiator is the direct teacher-student relationship and his specific teaching method for math, probability & statistics, and discrete mathematics — a neighboring platform could replicate the feature set but not the instructor.

## Operating Context

- Persian-language, RTL-first UI with Jalali (Saturday-first) calendar throughout.
- Konkur exam cycle and school academic calendar shape scheduling, live-class timing, and test-collection release.
- Timed, topic-based practice tests with device fingerprinting (`@fingerprintjs`) to prevent multiple-login cheating during exams; students expect these sessions to feel secure and fair.
- Live classes (RTMP / live iframe) plus chunked VOD uploads (Tus-protocol) for recorded sessions; secure video delivery via SpotPlayer DRM.
- SMS OTP auth via sms.ir alongside standard username/email login; JWT in HTTP-only cookies with cross-tab sync.
- Iranian payment gateway (Zibal, formerly/also Zarinpal) for the shop and course purchases.
- A Capacitor-wrapped Android app packages the same web app for mobile distribution — this is a packaging convenience, not a separate native design language; the product's design system stays web-first.

## Capabilities and Constraints

- **Course delivery**: class schedules, live sessions, session files (slides/handouts/code), chunked VOD uploads.
- **Test Maker suite**: question bank, test collections (public/private, folder-organized), topic-based and custom test generation, device-fingerprinted student test sessions, detailed answer sheets with PDF export, automated scoring and progress tracking.
- **Knowledge tree**: legacy Subject → Chapter → Section → Topic hierarchy alongside a newer self-referencing Folder structure; tracks student topic mastery and recommends practice.
- **Shop / e-commerce**: digital (courses, tests, collections) and physical products, cart, coupons/discounts, Zibal payment and order/transaction records.
- **AI support**: Gemini-backed ticket categorization and AI chat threads for student questions.
- **Content**: blog, gallery, knowledge base articles.
- **Auth & security**: username/email or SMS-verified phone login, JWT cookies, device fingerprinting, per-app-based access control (student/teacher/admin/support/content-creator/finance roles).
- **Constraint**: Persian typography correctness (glyph boundary handling, math expression rendering) is load-bearing, not cosmetic — regressions there directly hurt the core teaching content.
- **Constraint**: platform is `web`; do not introduce iOS/Android-native design idioms on the strength of the Capacitor wrapper alone.

## Brand Commitments

- Personal instructor brand: **Arian Tafazolizadeh** (آرین تفضلی‌زاده), with an "AT" chevron/X monogram mark used as the site's brand identity (`AT.svg`, PWA icon).
- Persian-first, RTL-native presentation is a binding identity constraint, not a locale toggle.

## Evidence on Hand

- Partner-school/institution logos already in the codebase (`vite-project/public/*.png|webp|svg`) are real institutional trust signals — Alpha School, Baharestan, Hanan, Hadaf, Salam Schools, Neshane Rasa, Roshangaran, Shafie Foundation — not to be treated as fabricated testimonials, and not to be extended with invented partners.
- No documented pricing figures, growth metrics, or case-study numbers exist yet — do not invent specific prices, student counts, or performance claims; state these as open/undocumented if a surface needs them.

## Product Principles

1. **The teacher-student relationship is the product.** Every surface should reinforce that this is Arian Tafazolizadeh's own teaching, not anonymous or outsourced content.
2. **Persian-first, RTL-native.** Never design in an English/LTR-first mental model and translate afterward; Persian typography and RTL layout are the default, not an accommodation.
3. **Exam integrity and trust.** Test-taking surfaces must feel secure and fair to students and credible to partner-school administrators evaluating the platform.
4. **Serve two audiences without splitting the product.** Individual students and partner-school cohorts run on the same platform; features should not silently assume one audience over the other.
5. **Respect the real academic calendar.** Content, scheduling, and messaging follow the Jalali calendar and the actual Konkur exam cycle, not a generic school-year assumption.
