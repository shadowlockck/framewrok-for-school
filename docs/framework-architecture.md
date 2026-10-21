# Архітектура School Website Framework

> **Призначення документа:** Посібник для розробників, веброзробників та технічних спеціалістів відділів освіти щодо розробки, кастомізації та розширення сайтів закладів освіти на базі фреймворку.

---

## 1. Архітектурні принципи фреймворку

Фреймворк побудований за принципом **Inversion of Control (Інверсія контролю)** та **Headless / Component-Driven Architecture**:

1. **Нормативна інваріантність (Legal Invariants):**
   - Норми закону (ст. 30 ЗУ «Про освіту», захист персональних даних учнів, 10-денний термін фінансової звітності, вимоги НАССР) закладені в ядро фреймворку.
   - Розробнику не потрібно з нуля вивчати закони та перевіряти, які документи обов'язкові — валідація вбудована в моделі та API.

2. **Розширюваність через абстрактні класи (Extension Points):**
   - Усі ключові сутності реалізовані як абстрактні моделі (`AbstractSchoolProfile`, `AbstractLegalDocument`, `AbstractClassCapacity`, `AbstractFinancialReport`, `AbstractDailyMenu` тощо).
   - Розробник може успадкувати будь-яку модель і додати власні специфічні поля без модифікації ядра.

3. **Динамічний маніфест можливостей (Capabilities & Manifest API):**
   - Бекенд надає системний ендпоінт `/api/v1/core/manifest/`, який автоматично інтроспектує активні додатки (`INSTALLED_APPS`).
   - Якщо школа не надає послуг харчування або не публікує розклад дзвінків — відповідний додаток просто вимикається в конфігурації, а фронтенд автоматично приховує вкладку і картки без помилок.

4. **Повна відсутність хардкоду (Decoupled Frontend):**
   - Увесь UI живиться через `SchoolFrameworkProvider` (React Context).
   - Назва закладу, логотип, кольори фірмового стилю, реквізити та контактні дані беруться виключно з API закладу або конфігурації.

---

## 2. Як розширювати моделі (Backend)

### Приклад: Додавання філії або спеціалізованих ліцейських кафедр

Якщо для конкретного ліцею потрібно розширити кадровий склад або додати кафедри:

```python
# your_school_app/models.py
from apps.legal.models import AbstractStaffMember
from django.db import models

class LyceumStaffMember(AbstractStaffMember):
    department = models.CharField(
        max_length=150,
        verbose_name="Кафедра (наприклад: Кафедра інформатики та робототехніки)"
    )
    scientific_degree = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="Науковий ступінь"
    )

    class Meta(AbstractStaffMember.Meta):
        verbose_name = "Викладач ліцею"
        verbose_name_plural = "Викладацький склад ліцею"
```

### Приклад: Додавання олімпіадних балів до зарахування

```python
# your_school_app/models.py
from apps.admissions.models import AbstractEnrolledStudent
from django.db import models

class LyceumStudent(AbstractEnrolledStudent):
    olympiad_winner = models.BooleanField(
        default=False,
        verbose_name="Переможець міської/всеукраїнської олімпіади"
    )
    points = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name="Вступний рейтинговий бал"
    )
```

---

## 3. Як вибірково підключати модулі

У файлі `config/settings.py` розробник формує склад сайту:

```python
INSTALLED_APPS = [
    # Обов'язкове ядро
    'apps.core',
    'apps.legal',         # Документи і фінанси

    # Опційні плагіни / модулі (вмикайте за потребою)
    'apps.admissions',    # Зарахування та вільні місця
    'apps.safety',        # Протидія булінгу (ст. 30)
    'apps.nutrition',     # Щоденне меню (якщо є їдальня)
    'apps.schedule',      # Розклад занять
    'apps.news',          # Новини та оголошення
    'apps.gallery',       # Фото- та відеогалерея
]
```

Якщо прибрати `'apps.nutrition'`, бекенд припинить обслуговувати ендпоінти їдальні, а фронтенд оновить навігаційне меню. `apps.core` залишається обов'язковим. `apps.schedule` залежить від `apps.admissions`, оскільки урок прив'язаний до класу. Команда `python manage.py check` повідомить про некоректну комбінацію. Після зміни `INSTALLED_APPS` застосуйте міграції та перезапустіть сервер. Вимкнення застосунку не видаляє його таблиць і даних.

### Оновлення раніше створеного сайту

Нові версії пакета не переписують файли `config/urls.py` та `frontend/src/App.tsx` існуючого сайту. Після оновлення пакета замініть безумовні `include('apps.<модуль>.urls')` у `config/urls.py` на:

```python
from apps.core.modules import module_urlpatterns

# Після базових маршрутів ядра:
urlpatterns += module_urlpatterns()
```

У згенерованому раніше фронтенді оновіть завантаження: спочатку запросіть `/api/v1/core/manifest/`, потім виконуйте запити лише до API модулів, для яких `modules.<назва>` дорівнює `true`. Для трьох поточних дизайнів це вже реалізовано в `school-admin create-frontend`. Повторна генерація фронтенду з `--force` перезаписує локальні правки; перед нею збережіть власні зміни. Перевірте `python manage.py check`, головну сторінку, маніфест і відсутність вимкнених URL у `/api/schema/`.

---

## 4. Використання фронтенду як бібліотеки UI-компонентів (@school-framework/ui)

Розробник може не просто використовувати готовий шаблон, а створити абсолютно унікальний дизайн, використовуючи готові юридично-вивірені компоненти:

```tsx
import React from 'react';
import {
  SchoolFrameworkProvider,
  AccessibilityBar,
  LegalRegisterView,
  FinancialTransparencyView,
  useSchool
} from 'school-framework-ui';

export const CustomLyceumSite = () => {
  return (
    <SchoolFrameworkProvider>
      <div className="my-custom-theme">
        {/* Віджет доступності WCAG 2.1 AA працює на будь-якому сайті */}
        <AccessibilityBar />

        {/* Унікальний Hero-блок розробника */}
        <MyUniqueHero />

        {/* Готові нормативні реєстри ст. 30 зі зручним пошуком та фільтрами */}
        <LegalRegisterView />
        <FinancialTransparencyView />
      </div>
    </SchoolFrameworkProvider>
  );
};
```

---

## 5. Система динамічних тем (Theming Engine)

Колірна схема автоматично синхронізується з БД закладу через CSS-змінні:

| CSS Змінна | Призначення | Значення за замовчуванням |
| :--- | :--- | :--- |
| `--color-primary` | Основний брендовий колір закладу | `#1e3a8a` |
| `--color-secondary` | Вторинний колір (акценти, кнопки) | `#059669` |
| `--color-accent` | Колір попереджень, термінових оголошень | `#d97706` |
| `--font-family-base` | Основний шрифт сайту | `Inter, sans-serif` |

Школа змінює кольори в панелі керування Django Admin у меню **«Налаштування теми та брендингу»**, і сайт миттєво змінює вигляд без перезавантаження серверів.

---

## 6. Встановлення як Python-пакету

Бекенд оформлено відповідно до стандарту PEP 621:

```bash
# Встановлення в режимі розробки
pip install -e ./backend

# Або встановлення з Git репозиторію
pip install git+https://github.com/shadowlockck/framework-for-school.git#subdirectory=backend
```
---

## 7. CLI-утиліта `school-admin`

Фреймворк містить консольну утиліту для швидкого створення проєктів, ініціалізації закладів та автоматичного аудиту:

```bash
# 1. Створення каркасу школи одразу з React-макетом
school-admin startproject my_school_site --frontend-template editorial

# Якщо фронтенд поки не потрібен, замість команди вище виконайте:
# school-admin startproject my_school_site

# 2. Ініціалізація або оновлення профілю закладу в БД
school-admin create-school "Ліцей №100 «Поділ»" \
  --edrpou 12345678 \
  --city "Київ" \
  --founder "Київська міська рада" \
  --capacity 1200 \
  --actual 1150

# 3. Перевірка відповідності ст. 30 ЗУ «Про освіту» (термінальний аудит)
school-admin check-compliance

# 4. Вивід аудиту у форматі JSON для CI/CD пайплайнів
school-admin check-compliance --json

# 5. Швидке заповнення реалістичними демо-даними
school-admin seed-data

# Додати фронтенд пізніше: classic (типовий), editorial або portal
school-admin create-frontend --template portal --output-dir frontend
```

---

## 8. Бібліотечна збірка npm (`@school-framework/ui`)

Фронтенд-компоненти та SDK зібрані в автономну бібліотеку для повторного використання:

```bash
# Збірка додатку та бібліотеки
npm run build

# Збірка виключно npm-пакету (@school-framework/ui)
npm run build:lib
```

Пакет генерує:
- `dist/lib/school-framework-ui.js` (ES Modules)
- `dist/lib/school-framework-ui.umd.cjs` (CommonJS / UMD)
- `dist/lib/style.css` (Tailwind стилі та accessibility)
- `dist/lib/types/` (TypeScript `.d.ts` декларації для всіх компонентів, моделей і хуків)
