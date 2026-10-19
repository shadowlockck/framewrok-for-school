# School Website Framework (Фреймворк для сайтів шкіл)

> Повнофункціональний, безпечний та розширюваний інженерний веб-фреймворк для створення офіційних сайтів закладів загальної середньої освіти України з неухильним дотриманням вимог чинного законодавства.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.11%2B-blue.svg)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-5.2%20LTS-green.svg)](https://www.djangoproject.com/)
[![PyPI](https://img.shields.io/badge/PyPI-django--school--framework-blue.svg)](https://pypi.org/)
[![npm](https://img.shields.io/badge/npm-%40school--framework%2Fui-red.svg)](https://www.npmjs.com/)
[![React](https://img.shields.io/badge/React-19.0-61dafb.svg)](https://react.dev/)
[![TailwindCSS](https://img.shields.io/badge/Tailwind-3.4-38b2ac.svg)](https://tailwindcss.com/)
[![WCAG 2.1](https://img.shields.io/badge/Accessibility-WCAG%202.1%20AA-purple.svg)](https://www.w3.org/WAI/standards-guidelines/wcag/)

---

## 🏛️ Відповідність нормативно-правовим актам

Фреймворк спроектований так, щоб заклад освіти «з коробки» виконував усі законні вимоги щодо публічності та інформаційної відкритості:

1. **Стаття 30 Закону України «Про освіту»**:
   - Статут закладу освіти;
   - Ліцензії на провадження освітньої діяльності;
   - Сертифікати про акредитацію освітніх програм;
   - Структура та органи управління закладу;
   - Кадровий склад згідно з ліцензійними умовами;
   - Освітні програми, перелік навчальних компонентів;
   - Територія обслуговування, закріплена засновником;
   - Ліцензований обсяг та фактична кількість осіб;
   - Мова (мови) освітнього процесу;
   - Вакантні посади та порядок проведення конкурсу;
   - Матеріально-технічне забезпечення;
   - Результати моніторингу якості освіти та річний звіт;
   - Правила прийому та форми здобуття освіти (очна, дистанційна, екстернат, сімейна, педпатронаж);
   - Умови доступності для навчання осіб з особливими освітніми потребами (ООП);
   - Кошторис та фінансові звіти (контроль строку оприлюднення не пізніше **10 робочих днів**);
   - Благодійна допомога (перелік товарів, робіт і послуг із зазначенням вартості).
2. **Стаття 39 Закону України «Про повну загальну середню освіту»**:
   - Оприлюднення умов конкурсу на посаду керівника закладу наступного робочого дня після ухвалення рішення.
3. **Закон України «Про захист персональних даних»**:
   - Списки зарахованих учнів оприлюднюються **виключно із зазначенням їхніх прізвищ** (без імен, адрес та персональної інформації).
4. **Харчування (Постанова КМУ № 305 / НАССР)**:
   - Щоденне меню відповідно до вікових груп (1-4, 5-9, 10-11 класи);
   - Інформація про оператора, що надає послуги харчування.
5. **Протидія булінгу (Закон № 2657-VIII)**:
   - План заходів щодо запобігання та протидії булінгу;
   - Порядок подання та конфіденційного розгляду заяв;
   - Захищена форма онлайн-подання конфіденційних звернень.
6. **Цифрова доступність (WCAG 2.1 AA)**:
   - Спеціальна версія для людей з порушенням зору (налаштування розміру шрифту та висококонтрастні колірні схеми: чорно-біла, жовтий на чорному).

---

## 🛠️ Стек технологій та архітектура

- **Бекенд-бібліотека (`django-school-framework`):** Python 3.11+, Django 5.2 LTS, Django REST Framework, drf-spectacular (Swagger OpenAPI / Redoc). Абстрактні базові класи для легкого успадкування.
- **CLI-утиліта (`school-admin`):** Швидке скаффолдинг-створення сайтів шкіл, ініціалізація профілів та аудит закону прямо з терміналу.
- **Фронтенд-бібліотека (`@school-framework/ui`):** React 19, TypeScript, Tailwind CSS, Lucide Icons. Підтримка ES Modules, UMD, TypeScript `.d.ts` типів та стилів.
- **Compliance Dashboard:** Вбудований у Django Admin монітор відповідності закону з відсотковою шкалою та нагадуванням про строки.
- **Розгортання:** Docker Compose з конфігурованими портами без конфліктів.

Детальний посібник для розробників: **[docs/framework-architecture.md](docs/framework-architecture.md)**. Перед публікацією сайту перевірте [налаштування HTTPS і безпечного розгортання](docs/deployment-guide.md).

---

## 💻 Швидкий старт через CLI `school-admin`

Встановіть пакет фреймворку:

```bash
pip install django-school-framework
```

### 1. Створити каркас нового сайту школи

```bash
school-admin startproject my_school
cd my_school
```

### 2. Застосувати міграції та створити профіль закладу

```bash
python manage.py migrate

school-admin create-school "Ліцей №100 «Поділ»" \
  --edrpou 12345678 \
  --city "Київ" \
  --founder "Київська міська рада" \
  --capacity 1200 \
  --actual 1150
```

### 3. Перевірити рівень виконання ст. 30 ЗУ «Про освіту»

```bash
# Термінальний монітор з прогрес-баром та чек-листом
school-admin check-compliance

# Або вивід у форматі JSON для CI/CD перевірок
school-admin check-compliance --json
```

### 4. Наповнити базу демонстраційними даними (за потреби)

```bash
school-admin seed-data
```

---

## 🎨 Використання бібліотеки компонентів `@school-framework/ui`

Встановіть React UI-kit у вашому фронтенд-проєкті:

```bash
npm install @school-framework/ui
```

```tsx
import React from 'react';
import '@school-framework/ui/style.css';
import {
  SchoolFrameworkProvider,
  Header,
  LegalRegisterView,
  FinancialTransparencyView,
  useSchool,
  useModules
} from '@school-framework/ui';

export function App() {
  return (
    <SchoolFrameworkProvider apiBase="https://myschool.edu.ua/api/v1">
      <MainContent />
    </SchoolFrameworkProvider>
  );
}

function MainContent() {
  const { school, loading } = useSchool();
  const { modules } = useModules();

  if (loading) return <div>Завантаження...</div>;

  return (
    <div className="min-h-screen bg-slate-50">
      <Header />
      <main className="max-w-7xl mx-auto py-8 px-4">
        <h1 className="text-3xl font-bold">{school.name}</h1>
        {modules.legal && <LegalRegisterView />}
        {modules.legal && <FinancialTransparencyView />}
      </main>
    </div>
  );
}
```

---

## 🐳 Запуск монорепозиторію через Docker Compose

Для локальної розробки та демонстрації повного стеку:

```bash
# 1. Налаштувати змінні оточення
cp .env.example .env

# 2. Запустити сервіси (MySQL, Backend, Frontend)
docker compose up -d --build
```

Доступні адреси:
- 🌐 **Frontend (Сайт школи):** [http://localhost:5173](http://localhost:5173)
- ⚙️ **Backend API:** [http://localhost:8000/api/v1/](http://localhost:8000/api/v1/)
- 📖 **Документація API (Swagger):** [http://localhost:8000/api/docs/](http://localhost:8000/api/docs/)
- 📑 **Документація API (Redoc):** [http://localhost:8000/api/redoc/](http://localhost:8000/api/redoc/)
- 🔐 **Панель керування з Compliance Dashboard:** [http://localhost:8000/admin/](http://localhost:8000/admin/)

---

## 📦 Модулі фреймворку

| Модуль | Призначення | Відповідність закону |
| :--- | :--- | :--- |
| `apps.core` | Профіль школи, ЄДРПОУ, брендинг (CSS-змінні), Manifest API, Compliance Auditor. | ст. 30 ч. 2 ЗУ «Про освіту» |
| `apps.legal` | Обов'язкові документи (статут, ліцензії), фінансові звіти (строк 10 днів), кадри, вакансії. | ст. 30 ч. 2 п. 1–5, 12, ч. 3 |
| `apps.admissions` | Закріплена територія, вільні місця, списки зарахованих (виключно прізвища). | ст. 30 ч. 2 п. 7, ЗУ про захист даних |
| `apps.nutrition` | Щоденне меню за віковими категоріями, оператор харчування. | Постанова КМУ № 305 / НАССР |
| `apps.safety` | План заходів протидії булінгу, конфіденційна подача онлайн-заяв. | ст. 30 ч. 2 п. 14, ЗУ № 2657-VIII |
| `apps.news` | Новини, термінові сповіщення безпеки для батьків та учнів. | Інформаційна відкритість |
| `apps.schedule` | Розклад дзвінків та уроків за днями тижня для паралелей. | Організація освітнього процесу |
| `apps.gallery` | Фото- та відеоальбоми шкільних заходів. | Популяризація діяльності закладу |

---

## 🧪 Тестування та перевірка якості

```bash
# Запуск 22 автоматичних тестів бекенду
docker compose exec backend python manage.py test apps.core apps.legal apps.admissions apps.nutrition apps.safety apps.news apps.schedule apps.gallery

# Або локально через віртуальне оточення
PYTHONPATH=backend ./venv/bin/python backend/manage.py test apps.core apps.legal apps.admissions apps.nutrition apps.safety apps.news apps.schedule apps.gallery

# Збірка фронтенд додатку та бібліотеки UI
cd frontend && npm run build
```

Для перевірки саме встановленого пакета, генератора сайту та згенерованого фронтенду
запустіть `python scripts/smoke_installed_package.py`. Скрипт потребує Python із
`setuptools` і `wheel`, Node.js/npm та доступу до інтернету для встановлення
залежностей у тимчасове віртуальне оточення. CI додатково запускає його на Windows.

---

## 📄 Ліцензія

Проект поширюється під відкритою ліцензією [MIT](LICENSE).
Розроблено для вільного використання всіма закладами загальної середньої освіти України.
