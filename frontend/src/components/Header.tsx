import React from 'react';
import { BookOpen, Phone, Mail, MapPin, Globe, ShieldAlert, FileText, Users, DollarSign, Utensils, Calendar, Newspaper, Image } from 'lucide-react';

interface HeaderProps {
  currentTab: string;
  setCurrentTab: (tab: string) => void;
  lang: 'uk' | 'en';
  setLang: (lang: 'uk' | 'en') => void;
}

export const Header: React.FC<HeaderProps> = ({ currentTab, setCurrentTab, lang, setLang }) => {
  return (
    <header className="bg-white border-b border-slate-200 shadow-sm sticky top-0 z-40">
      {/* Top school info bar */}
      <div className="bg-slate-100 border-b border-slate-200 text-xs text-slate-600 py-1.5 px-4">
        <div className="max-w-7xl mx-auto flex flex-wrap items-center justify-between gap-2">
          <div className="flex flex-wrap items-center gap-4">
            <span className="flex items-center gap-1">
              <MapPin className="w-3.5 h-3.5 text-primary" />
              <span>вул. Освітня, 15, м. Київ, 01001</span>
            </span>
            <span className="flex items-center gap-1">
              <Phone className="w-3.5 h-3.5 text-primary" />
              <a href="tel:+380441234567" className="hover:underline">+38 (044) 123-45-67</a>
            </span>
            <span className="flex items-center gap-1">
              <Mail className="w-3.5 h-3.5 text-primary" />
              <a href="mailto:school@osvita.kyiv.ua" className="hover:underline">school@osvita.kyiv.ua</a>
            </span>
          </div>

          <div className="flex items-center gap-3">
            <span className="bg-amber-100 text-amber-800 px-2 py-0.5 rounded font-medium text-[11px]">
              ЄДРПОУ: 12345678
            </span>
            <button
              onClick={() => setLang(lang === 'uk' ? 'en' : 'uk')}
              className="flex items-center gap-1 hover:text-primary font-medium transition"
            >
              <Globe className="w-3.5 h-3.5" />
              <span>{lang === 'uk' ? 'EN' : 'УКР'}</span>
            </button>
          </div>
        </div>
      </div>

      {/* Main branding */}
      <div className="max-w-7xl mx-auto px-4 py-4 flex flex-wrap items-center justify-between gap-4">
        <div className="flex items-center gap-3 cursor-pointer" onClick={() => setCurrentTab('home')}>
          <div className="w-12 h-12 bg-primary rounded-xl flex items-center justify-center text-white shadow-md">
            <BookOpen className="w-7 h-7" />
          </div>
          <div>
            <h1 className="text-xl md:text-2xl font-bold text-slate-900 tracking-tight">
              Ліцей «Інтелект та Інновації»
            </h1>
            <p className="text-xs text-slate-500">
              Офіційний сайт закладу загальної середньої освіти • Засновник: Київська міська рада
            </p>
          </div>
        </div>

        {/* Quick compliance badge */}
        <div className="hidden lg:flex items-center gap-2 bg-emerald-50 text-emerald-800 px-3 py-1.5 rounded-lg border border-emerald-200 text-xs">
          <div className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></div>
          <span>Відповідність ст. 30 ЗУ «Про освіту» підтверджено</span>
        </div>
      </div>

      {/* Main Navigation Bar */}
      <nav className="bg-slate-900 text-slate-100 px-4">
        <div className="max-w-7xl mx-auto flex flex-wrap items-center gap-1 text-sm font-medium">
          <button
            onClick={() => setCurrentTab('home')}
            className={`px-3 py-2.5 transition border-b-2 ${currentTab === 'home' ? 'border-amber-400 text-amber-300 bg-slate-800' : 'border-transparent hover:bg-slate-800'}`}
          >
            Головна
          </button>

          <button
            onClick={() => setCurrentTab('legal')}
            className={`flex items-center gap-1.5 px-3 py-2.5 transition border-b-2 ${currentTab === 'legal' ? 'border-amber-400 text-amber-300 bg-slate-800' : 'border-transparent hover:bg-slate-800'}`}
          >
            <FileText className="w-4 h-4" />
            <span>Прозорість (ст. 30)</span>
          </button>

          <button
            onClick={() => setCurrentTab('admissions')}
            className={`flex items-center gap-1.5 px-3 py-2.5 transition border-b-2 ${currentTab === 'admissions' ? 'border-amber-400 text-amber-300 bg-slate-800' : 'border-transparent hover:bg-slate-800'}`}
          >
            <Users className="w-4 h-4" />
            <span>Зарахування та вільні місця</span>
          </button>

          <button
            onClick={() => setCurrentTab('finance')}
            className={`flex items-center gap-1.5 px-3 py-2.5 transition border-b-2 ${currentTab === 'finance' ? 'border-amber-400 text-amber-300 bg-slate-800' : 'border-transparent hover:bg-slate-800'}`}
          >
            <DollarSign className="w-4 h-4" />
            <span>Фінансова звітність</span>
          </button>

          <button
            onClick={() => setCurrentTab('nutrition')}
            className={`flex items-center gap-1.5 px-3 py-2.5 transition border-b-2 ${currentTab === 'nutrition' ? 'border-amber-400 text-amber-300 bg-slate-800' : 'border-transparent hover:bg-slate-800'}`}
          >
            <Utensils className="w-4 h-4" />
            <span>Харчування (Меню)</span>
          </button>

          <button
            onClick={() => setCurrentTab('schedule')}
            className={`flex items-center gap-1.5 px-3 py-2.5 transition border-b-2 ${currentTab === 'schedule' ? 'border-amber-400 text-amber-300 bg-slate-800' : 'border-transparent hover:bg-slate-800'}`}
          >
            <Calendar className="w-4 h-4" />
            <span>Розклад</span>
          </button>

          <button
            onClick={() => setCurrentTab('news')}
            className={`flex items-center gap-1.5 px-3 py-2.5 transition border-b-2 ${currentTab === 'news' ? 'border-amber-400 text-amber-300 bg-slate-800' : 'border-transparent hover:bg-slate-800'}`}
          >
            <Newspaper className="w-4 h-4" />
            <span>Новини</span>
          </button>

          <button
            onClick={() => setCurrentTab('gallery')}
            className={`flex items-center gap-1.5 px-3 py-2.5 transition border-b-2 ${currentTab === 'gallery' ? 'border-amber-400 text-amber-300 bg-slate-800' : 'border-transparent hover:bg-slate-800'}`}
          >
            <Image className="w-4 h-4" />
            <span>Галерея</span>
          </button>

          <button
            onClick={() => setCurrentTab('safety')}
            className={`flex items-center gap-1.5 px-3 py-2.5 transition border-b-2 ${currentTab === 'safety' ? 'border-amber-400 text-amber-300 bg-slate-800' : 'border-transparent hover:bg-slate-800'}`}
          >
            <ShieldAlert className="w-4 h-4 text-red-400" />
            <span className="text-red-300">Протидія булінгу</span>
          </button>
        </div>
      </nav>
    </header>
  );
};
