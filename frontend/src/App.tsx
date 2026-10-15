import React, { useState } from 'react';
import { AccessibilityBar } from './components/AccessibilityBar';
import { Header } from './components/Header';
import { LegalRegisterView } from './pages/LegalRegisterView';
import { AdmissionsView } from './pages/AdmissionsView';
import { FinancialTransparencyView } from './pages/FinancialTransparencyView';
import { NewsView } from './pages/NewsView';
import { ScheduleView } from './pages/ScheduleView';
import { GalleryView } from './pages/GalleryView';
import { BookOpen, ShieldCheck, HeartHandshake, PhoneCall, ArrowRight, ShieldAlert, Utensils, Calendar, Newspaper, Image } from 'lucide-react';

export const App: React.FC = () => {
  const [currentTab, setCurrentTab] = useState<string>('home');
  const [lang, setLang] = useState<'uk' | 'en'>('uk');

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
                  Простір знань, інновацій та безпечного зростання
                </h1>
                <p className="text-blue-200 text-base md:text-lg max-w-2xl mx-auto mb-8">
                  Офіційна веб-платформа закладу загальної середньої освіти з повною інформаційною відкритістю та дотриманням законодавства.
                </p>

                <div className="flex flex-wrap justify-center gap-4">
                  <button
                    onClick={() => setCurrentTab('legal')}
                    className="bg-amber-500 hover:bg-amber-400 text-slate-950 font-bold px-6 py-3 rounded-xl transition shadow-lg flex items-center gap-2"
                  >
                    <span>Відкритість закладу (ст. 30)</span>
                    <ArrowRight className="w-4 h-4" />
                  </button>

                  <button
                    onClick={() => setCurrentTab('admissions')}
                    className="bg-white/10 hover:bg-white/20 text-white font-semibold px-6 py-3 rounded-xl backdrop-blur transition border border-white/20"
                  >
                    Зарахування дітей та вільні місця
                  </button>
                </div>
              </div>
            </section>

            {/* Quick Cards Grid */}
            <section className="py-12 max-w-7xl mx-auto px-4 -mt-8">
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
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
              </div>
            </section>
          </div>
        )}

        {currentTab === 'legal' && <LegalRegisterView />}
        {currentTab === 'admissions' && <AdmissionsView />}
        {currentTab === 'finance' && <FinancialTransparencyView />}
        {currentTab === 'schedule' && <ScheduleView />}
        {currentTab === 'news' && <NewsView />}
        {currentTab === 'gallery' && <GalleryView />}
        {currentTab === 'nutrition' && (
          <div className="py-12 max-w-7xl mx-auto px-4">
            <div className="bg-white rounded-2xl p-8 border border-slate-200 shadow-sm">
              <h2 className="text-2xl font-bold text-slate-900 mb-4 flex items-center gap-2">
                <Utensils className="w-6 h-6 text-emerald-600" />
                <span>Організація харчування та щоденне меню</span>
              </h2>
              <p className="text-sm text-slate-600 mb-6">
                Відповідно до законодавства, на сайті закладу щоденно оприлюднюється фактичне меню за віковими групами,
                а також інформація про оператора харчування.
              </p>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div className="p-4 bg-emerald-50 rounded-xl border border-emerald-200">
                  <h4 className="font-bold text-emerald-950 text-sm mb-1">Початкова школа (1-4 класи)</h4>
                  <p className="text-xs text-slate-600">Сніданок: каша вівсяна з яблуком, чай з лимоном, сир твердий.</p>
                </div>
                <div className="p-4 bg-blue-50 rounded-xl border border-blue-200">
                  <h4 className="font-bold text-blue-950 text-sm mb-1">Базова школа (5-9 класи)</h4>
                  <p className="text-xs text-slate-600">Обід: суп овочевий, пюре картопляне з котлетою паровою, компот.</p>
                </div>
                <div className="p-4 bg-amber-50 rounded-xl border border-amber-200">
                  <h4 className="font-bold text-amber-950 text-sm mb-1">Старша школа (10-11 класи)</h4>
                  <p className="text-xs text-slate-600">Обід: борщ український, рагу овочеве з індичкою, салат із капусти.</p>
                </div>
              </div>
            </div>
          </div>
        )}
        {currentTab === 'safety' && (
          <div className="py-12 max-w-7xl mx-auto px-4">
            <div className="bg-white rounded-2xl p-8 border border-slate-200 shadow-sm">
              <h2 className="text-2xl font-bold text-slate-900 mb-4 flex items-center gap-2">
                <ShieldAlert className="w-6 h-6 text-rose-600" />
                <span>Запобігання та протидія булінгу (цькуванню)</span>
              </h2>
              <p className="text-sm text-slate-600 mb-6">
                Заклад освіти забезпечує неухильне дотримання порядку реагування на доведені випадки булінгу та захист конфіденційності заявника.
              </p>
              <div className="bg-slate-50 p-6 rounded-xl border border-slate-200 max-w-2xl">
                <h4 className="font-bold text-slate-900 text-sm mb-3">Подати конфіденційне звернення</h4>
                <div className="space-y-3">
                  <div>
                    <label className="block text-xs font-medium text-slate-700 mb-1">Ваш статус</label>
                    <select className="w-full border border-slate-300 rounded-lg p-2 text-xs">
                      <option>Учень / учениця</option>
                      <option>Батьки / законні представники</option>
                      <option>Педагогічний працівник</option>
                      <option>Анонімно</option>
                    </select>
                  </div>
                  <div>
                    <label className="block text-xs font-medium text-slate-700 mb-1">Опис ситуації</label>
                    <textarea rows={3} className="w-full border border-slate-300 rounded-lg p-2 text-xs" placeholder="Вкажіть факти та обставини..."></textarea>
                  </div>
                  <button className="bg-rose-600 hover:bg-rose-700 text-white font-bold text-xs px-4 py-2 rounded-lg transition">
                    Надіслати конфіденційно
                  </button>
                </div>
              </div>
            </div>
          </div>
        )}
      </main>

      {/* Footer */}
      <footer className="bg-slate-900 text-slate-400 text-xs py-8 border-t border-slate-800">
        <div className="max-w-7xl mx-auto px-4 flex flex-wrap items-center justify-between gap-4">
          <div>
            <p className="font-semibold text-white">Ліцей «Інтелект та Інновації»</p>
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
