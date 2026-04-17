# Next Session: Доработка AI Consulting Website — Blog Citations + Final Polish

## Контекст

Сайт `d:/ai-consulting-website/` — Astro + Tailwind, AI consulting для contractors. За 2 сессии:

### Что уже сделано:
1. **Главная страница** — готова, не трогаем
2. **Services Index** — переделан: 3 карточки с highlight, путь клиента, decision tree, guarantee
3. **AI Audit page** — pain-driven hero, "Is This For You?" квалификация, value stack, guarantee badge, scoring bars, stats
4. **Strategy Roadmap** — hero, визуальный 30/60/90 timeline, Before vs After
5. **Monthly Advisory** — hero, "A Typical Month" по неделям, Month 1 vs Month 6, pricing comparison
6. **About page** — personal story от 1-го лица, photo placeholder, 3-Step Analysis, credentials, Tools bar
7. **Contact page** — убран Cal.com placeholder, full-width form, "What Happens Next", FAQ
8. **Blog Index** — featured post, tags, quiz CTA
9. **Blog Post Layout** — убран CTA перед контентом, author box, related posts
10. **AI Readiness Quiz** — fade анимации, bar chart результатов, per-category рекомендации
11. **ROI Calculator** — НОВАЯ страница `/resources/roi-calculator/` (4 inputs, breakdown)
12. **Micro-copy** под inline CTA + stage-matched CTAs на всех service heroes
13. **Navigation** — добавлен "Free Quiz" в nav, ROI Calculator в footer
14. **SEO** — robots.txt исправлен, OG image сделан optional, meta descriptions улучшены
15. **Bugs fixed** — unused imports, dead code, blog meta

### Config (всё ещё placeholders — НЕ ТРОГАТЬ без спроса у юзера):
- `config.ts`: name='[YOUR BRAND]', url='example.com', email='hello@example.com', calUrl='YOUR_LINK', formApiKey='YOUR_WEB3FORMS_KEY'
- `astro.config.mjs`: site='https://example.com'

---

## Что делать в этой сессии

### Задача 1: Исправить статистики в блоге (ГЛАВНОЕ)

Research показал что 6 из 10 ключевых статистик в 5 blog posts не имеют подтверждённых источников. Нужно:

1. **Обновить неверные цифры** на подтверждённые
2. **Добавить source attribution** к каждой значимой статистике (ссылка или footnote)
3. **Убрать или переформулировать** непроверяемые claims

#### Конкретные исправления по файлам:

**`src/content/blog/ai-answering-service-hvac.md`:**
- "22% of calls go unanswered" → **27%** (Source: [Invoca/Housecall Pro](https://www.housecallpro.com/resources/missed-calls/))
- "62% of calls come outside business hours" → переформулировать как "majority of calls" или найти конкретный source. Текущий source (ACHR News) не подтверждён
- "78% of emergency jobs go to first responder" → это MIT/Lead Connect study о speed-to-lead, НЕ специфично для HVAC emergencies. Переформулировать: "78% of customers buy from the first company that responds" ([Lead Connect/MIT study](https://caseyresponse.com/blog/lead-response-time-statistics))
- "$91K/year" → это расчётная цифра, добавить пояснение что это estimate based on industry averages

**`src/content/blog/ai-construction-estimating.md`:**
- "77% of contractors can't fill estimator positions" → **78%** ([AGC 2024 Workforce Survey](https://www.agc.org/sites/default/files/Files/Communications/2024_Workforce_Survey_Analysis.pdf))
- "40% use spreadsheets for estimating" → **85%** ([LetsBuild 2020 survey](https://www.letsbuild.com/blog/construction-estimating-spreadsheet))
- "928% ROI on AI estimating" → УДАЛИТЬ или заменить на: "Coastal Construction saved $1M/year" или "76% faster than manual takeoff" ([Togal.AI case studies](https://www.togal.ai/case-studies), University of Kansas study)
- "30% blow budgets" → переформулировать: "fewer than 31% of projects finish within 10% of budget" ([KPMG Global Construction Survey](https://www.propelleraero.com/blog/10-construction-project-cost-overrun-statistics-you-need-to-hear/))

**`src/content/blog/chatgpt-hvac-contractors.md`:**
- "41.3% reduction in admin time" — source NOT FOUND. Заменить на: "contractors save 4.5 hours per week per manager" ([Procore 2021 Canadian survey](https://www.procore.com/press/canadian-construction-managers-are-estimated-to-save-4-5-hours-a-week))
- "40% of small business staff spend 25%+ on admin" → для contractors конкретно: "85% of contractors spend 25%+ of time on tracking and reporting" ([Levelset 2020 survey](https://www.levelset.com/blog/2020-report-construction-wasted-time-slow-payment/))

**`src/content/blog/ai-readiness-checklist-hvac.md`** и **`src/content/blog/best-hvac-software-2026.md`:**
- Проверить все цитируемые цифры по этому же списку
- Добавить source links где они отсутствуют

#### Формат source attribution в markdown:
```markdown
According to [Housecall Pro research](https://www.housecallpro.com/resources/missed-calls/), **27% of inbound calls** to home service businesses go unanswered.
```

### Задача 2: Проверить homepage stats consistency

Главную страницу не трогаем в структуре, НО статистики на ней тоже используют те же цифры ($91K, 41.3%, 928%). Проверить и обновить ТОЛЬКО цифры если они расходятся с blog posts после исправлений. Hero и структуру не менять.

Файлы: `src/pages/index.astro` (секция "What AI Actually Finds", строки ~124-194) и секция "Cost of Waiting" (строки ~101-122).

### Задача 3 (если останется время): Visual polish

- Проверить все страницы в браузере (`npm run dev`)
- Проверить mobile view
- Убедиться что `npm run build` проходит чисто

---

## Правила

- НЕ менять структуру/layout главной страницы — только цифры если нужно
- НЕ менять config.ts placeholders — это отдельная задача при деплое
- Все source links должны быть рабочими (проверять через WebFetch если сомневаешься)
- Blog posts ~2,000+ слов — при замене цифр сохранять контекст и flow текста
- После всех изменений — `npm run build` для проверки
