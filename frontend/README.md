# @school-framework/ui

Офіційний React UI-kit та SDK для вебсайтів закладів загальної середньої освіти України.
Створено відповідно до вимог **статті 30 Закону України «Про освіту»**, стандарту доступності **WCAG 2.1 AA** та Закону про захист персональних даних.

## Встановлення

```bash
npm install @school-framework/ui
# або
pnpm add @school-framework/ui
```

Вимоги: `react >= 18`, `react-dom >= 18`.

## Швидкий старт

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

## Доступні компоненти та хуки

- **Провайдер**: `SchoolFrameworkProvider`
- **Хуки**: `useSchool()`, `useModules()`, `useNavigation()`, `useSchoolFramework()`
- **Навігація та доступність**: `Header`, `AccessibilityBar` (шрифти, контрастність WCAG 2.1 AA)
- **Нормативні сторінки (ст. 30)**: `LegalRegisterView`, `FinancialTransparencyView`, `AdmissionsView`, `SafetyView`
- **Шкільне життя**: `NutritionView`, `ScheduleView`, `NewsView`, `GalleryView`
- **API клієнт**: `fetchFromAPI()`, `submitConfidentialReport()`
