import React, { useState } from 'react';
import { AccessibilityBar } from './components/AccessibilityBar';
import { Header } from './components/Header';
import { LegalRegisterView } from './pages/LegalRegisterView';
import { AdmissionsView } from './pages/AdmissionsView';
import { FinancialTransparencyView } from './pages/FinancialTransparencyView';
import { NewsView } from './pages/NewsView';
import { ScheduleView } from './pages/ScheduleView';
import { GalleryView } from './pages/GalleryView';
import { NutritionView } from './pages/NutritionView';
import { SafetyView } from './pages/SafetyView';
import { SchoolFrameworkProvider, useSchool, useModules } from './context/SchoolContext';
import {
  BookOpen, ShieldCheck, HeartHandshake, ArrowRight, ShieldAlert,
  Utensils, Calendar, Newspaper, Image
} from 'lucide-react';

const AppContent: React.FC = () => {
  const [currentTab, setCurrentTab] = useState<string>('home');
  const [lang, setLang] = useState<'uk' | 'en'>('uk');
  const school = useSchool();
  const modules = useModules();

  return (
    <div className="min-h-screen flex flex-col bg-slate-50">
      <AccessibilityBar />
      <Header
        currentTab={currentTab}
        setCurrentTab={setCurrentTab}
        lang={lang}
        setLang={setLang}
      />

      <main className="flex-1">
        {currentTab === 'home' && (
          <div>
            {/* Hero Section */}
            <section className="bg-gradient-to-b from-blue-900 via-indigo-900 to-slate-900 text-white py-16 px-4">
              <div className="max-w-7xl mx-auto text-center">
                <span className="inline-block bg-amber-400 text-slate-950 font-bold text-xs uppercase px-3 py-1 rounded-full mb-4">
                  Нова Українська Школа (НУШ)
                </span>
                <h1 className="text-3xl md:text-5xl font-black tracking-tight mb-4 max-w-4xl mx-auto">
                  {school.name || 'Офіційний сайт закладу загальної середньої освіти'}
                </h1>
                <p className="text-blue-200 text-base md:text-lg max-w-2xl mx-auto mb-8">
                  {school.founder ? `Засновник: ${school.founder}. ` : ''}
                  Офіційна веб-платформа з повною інформаційною відкритістю та дотриманням законодавства України.
                </p>

                <div className="flex flex-wrap justify-center gap-4">
                  {modules.legal && (
                    <button
                      onClick={() => setCurrentTab('legal')}
                      className="bg-amber-500 hover:bg-amber-400 text-slate-950 font-bold px-6 py-3 rounded-xl transition shadow-lg flex items-center gap-2"
                    >
                      <span>Відкритість закладу (ст. 30)</span>
                      <ArrowRight className="w-4 h-4" />
                    </button>
                  )}

                  {modules.admissions && (
                    <button
                      onClick={() => setCurrentTab('admissions')}
                      className="bg-white/10 hover:bg-white/20 text-white font-semibold px-6 py-3 rounded-xl backdrop-blur transition border border-white/20"
                    >
                      Зарахування дітей та вільні місця
                    </button>
                  )}
                </div>
              </div>
            </section>

            {/* Dynamic Quick Cards Grid based on enabled modules */}
            <section className="py-12 max-w-7xl mx-auto px-4 -mt-8">
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                {modules.legal && (
                  <div
                    onClick={() => setCurrentTab('legal')}
                    className="bg-white p-6 rounded-2xl border border-slate-200 shadow-md hover:shadow-xl transition cursor-pointer group"
                  >
                    <div className="w-12 h-12 bg-blue-100 text-primary rounded-xl flex items-center justify-center mb-4 group-hover:scale-110 transition">
                      <BookOpen className="w-6 h-6" />
                    </div>
                    <h3 className="font-bold text-slate-900 text-lg mb-2">Стаття 30 ЗУ «Про освіту»</h3>
                    <p className="text-xs text-slate-600 leading-relaxed">
                      Статут, ліцензії, кадри, освітні програми та річні звіти у єдиному відкритому реєстрі.
                    </p>
                  </div>
                )}

                {modules.admissions && (
                  <div
                    onClick={() => setCurrentTab('admissions')}
                    className="bg-white p-6 rounded-2xl border border-slate-200 shadow-md hover:shadow-xl transition cursor-pointer group"
                  >
                    <div className="w-12 h-12 bg-emerald-100 text-emerald-700 rounded-xl flex items-center justify-center mb-4 group-hover:scale-110 transition">
                      <ShieldCheck className="w-6 h-6" />
                    </div>
                    <h3 className="font-bold text-slate-900 text-lg mb-2">Прийом та вільні місця</h3>
                    <p className="text-xs text-slate-600 leading-relaxed">
                      Закріплена територія, кількість місць у класах, жеребкування та порядок подання заяв.
                    </p>
                  </div>
                )}

                {modules.legal && (
                  <div
                    onClick={() => setCurrentTab('finance')}
                    className="bg-white p-6 rounded-2xl border border-slate-200 shadow-md hover:shadow-xl transition cursor-pointer group"
                  >
                    <div className="w-12 h-12 bg-amber-100 text-amber-700 rounded-xl flex items-center justify-center mb-4 group-hover:scale-110 transition">
                      <HeartHandshake className="w-6 h-6" />
                    </div>
                    <h3 className="font-bold text-slate-900 text-lg mb-2">Кошторис та благодійність</h3>
                    <p className="text-xs text-slate-600 leading-relaxed">
                      Публічна фінансова звітність про надходження та використання коштів закладу.
                    </p>
                  </div>
                )}

                {modules.safety && (
                  <div
                    onClick={() => setCurrentTab('safety')}
                    className="bg-white p-6 rounded-2xl border border-slate-200 shadow-md hover:shadow-xl transition cursor-pointer group"
                  >
                    <div className="w-12 h-12 bg-rose-100 text-rose-700 rounded-xl flex items-center justify-center mb-4 group-hover:scale-110 transition">
                      <ShieldAlert className="w-6 h-6" />
                    </div>
                    <h3 className="font-bold text-slate-900 text-lg mb-2">Протидія булінгу</h3>
                    <p className="text-xs text-slate-600 leading-relaxed">
                      План заходів, порядок реагування та захищена форма конфіденційного звернення.
                    </p>
                  </div>
                )}

                {modules.nutrition && (
                  <div
                    onClick={() => setCurrentTab('nutrition')}
                    className="bg-white p-6 rounded-2xl border border-slate-200 shadow-md hover:shadow-xl transition cursor-pointer group"
                  >
                    <div className="w-12 h-12 bg-teal-100 text-teal-700 rounded-xl flex items-center justify-center mb-4 group-hover:scale-110 transition">
                      <Utensils className="w-6 h-6" />
                    </div>
                    <h3 className="font-bold text-slate-900 text-lg mb-2">Щоденне меню</h3>
                    <p className="text-xs text-slate-600 leading-relaxed">
                      Фактичне меню за віковими групами, вихід страв та оператор харчування.
                    </p>
                  </div>
                )}

                {modules.schedule && (
                  <div
                    onClick={() => setCurrentTab('schedule')}
                    className="bg-white p-6 rounded-2xl border border-slate-200 shadow-md hover:shadow-xl transition cursor-pointer group"
                  >
                    <div className="w-12 h-12 bg-indigo-100 text-indigo-700 rounded-xl flex items-center justify-center mb-4 group-hover:scale-110 transition">
                      <Calendar className="w-6 h-6" />
                    </div>
                    <h3 className="font-bold text-slate-900 text-lg mb-2">Розклад уроків</h3>
                    <p className="text-xs text-slate-600 leading-relaxed">
                      Розклад занять за класами та днями тижня, графік навчальних дзвінків.
                    </p>
                  </div>
                )}

                {modules.news && (
                  <div
                    onClick={() => setCurrentTab('news')}
                    className="bg-white p-6 rounded-2xl border border-slate-200 shadow-md hover:shadow-xl transition cursor-pointer group"
                  >
                    <div className="w-12 h-12 bg-blue-100 text-blue-700 rounded-xl flex items-center justify-center mb-4 group-hover:scale-110 transition">
                      <Newspaper className="w-6 h-6" />
                    </div>
                    <h3 className="font-bold text-slate-900 text-lg mb-2">Новини та анонси</h3>
                    <p className="text-xs text-slate-600 leading-relaxed">
                      Актуальні події, оголошення для батьків та термінові сповіщення.
                    </p>
                  </div>
                )}

                {modules.gallery && (
                  <div
                    onClick={() => setCurrentTab('gallery')}
                    className="bg-white p-6 rounded-2xl border border-slate-200 shadow-md hover:shadow-xl transition cursor-pointer group"
                  >
                    <div className="w-12 h-12 bg-purple-100 text-purple-700 rounded-xl flex items-center justify-center mb-4 group-hover:scale-110 transition">
                      <Image className="w-6 h-6" />
                    </div>
                    <h3 className="font-bold text-slate-900 text-lg mb-2">Шкільна галерея</h3>
                    <p className="text-xs text-slate-600 leading-relaxed">
                      Фотоальбоми та відеозвіти про життя навчального закладу.
                    </p>
                  </div>
                )}
              </div>
            </section>
          </div>
        )}

        {/* Dynamic page view rendering */}
        {currentTab === 'legal' && modules.legal && <LegalRegisterView />}
        {currentTab === 'admissions' && modules.admissions && <AdmissionsView />}
        {currentTab === 'finance' && modules.legal && <FinancialTransparencyView />}
        {currentTab === 'schedule' && modules.schedule && <ScheduleView />}
        {currentTab === 'news' && modules.news && <NewsView />}
        {currentTab === 'gallery' && modules.gallery && <GalleryView />}
        {currentTab === 'nutrition' && modules.nutrition && <NutritionView />}
        {currentTab === 'safety' && modules.safety && <SafetyView />}
      </main>

      {/* Dynamic Footer with school information */}
      <footer className="bg-slate-900 text-slate-400 text-xs py-8 border-t border-slate-800">
        <div className="max-w-7xl mx-auto px-4 flex flex-wrap items-center justify-between gap-4">
          <div>
            <p className="font-semibold text-white">{school.name}</p>
            <p className="text-[11px] text-slate-500 mt-0.5">
              Сайт створено на базі School Website Framework відповідно до ст. 30 ЗУ «Про освіту»
            </p>
          </div>
          <div className="flex items-center gap-4 text-xs">
            <span className="text-slate-500">Режим доступності WCAG 2.1 AA</span>
            <span className="text-slate-600">•</span>
            <span className="text-slate-500">Захист персональних даних</span>
          </div>
        </div>
      </footer>
    </div>
  );
};

export const App: React.FC = () => {
  return (
    <SchoolFrameworkProvider>
      <AppContent />
    </SchoolFrameworkProvider>
  );
};
