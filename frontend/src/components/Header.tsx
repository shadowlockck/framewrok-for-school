import React from 'react';
import {
  BookOpen, Phone, Mail, MapPin, Globe,
  FileCheck, Users, DollarSign, Utensils, Calendar, Newspaper, Image, ShieldAlert
} from 'lucide-react';
import { useSchool, useNavigation } from '../context/SchoolContext';

interface HeaderProps {
  currentTab: string;
  setCurrentTab: (tab: string) => void;
  lang: 'uk' | 'en';
  setLang: (lang: 'uk' | 'en') => void;
}

const ICON_MAP: Record<string, React.FC<{ className?: string }>> = {
  FileCheck,
  DollarSign,
  Users,
  Calendar,
  Utensils,
  ShieldAlert,
  Newspaper,
  Image,
};

export const Header: React.FC<HeaderProps> = ({ currentTab, setCurrentTab, lang, setLang }) => {
  const school = useSchool();
  const navigation = useNavigation();

  return (
    <header className="bg-white border-b border-slate-200 shadow-sm sticky top-0 z-40">
      {/* Top school info bar */}
      <div className="bg-slate-100 border-b border-slate-200 text-xs text-slate-600 py-1.5 px-4">
        <div className="max-w-7xl mx-auto flex flex-wrap items-center justify-between gap-2">
          <div className="flex flex-wrap items-center gap-4">
            {school.address && (
              <span className="flex items-center gap-1">
                <MapPin className="w-3.5 h-3.5 text-primary" />
                <span>{school.address}</span>
              </span>
            )}
            {school.phone && (
              <span className="flex items-center gap-1">
                <Phone className="w-3.5 h-3.5 text-primary" />
                <a href={`tel:${school.phone}`} className="hover:underline">{school.phone}</a>
              </span>
            )}
            {school.email && (
              <span className="flex items-center gap-1">
                <Mail className="w-3.5 h-3.5 text-primary" />
                <a href={`mailto:${school.email}`} className="hover:underline">{school.email}</a>
              </span>
            )}
          </div>

          <div className="flex items-center gap-3">
            {school.edrpou && (
              <span className="bg-amber-100 text-amber-800 px-2 py-0.5 rounded font-medium text-[11px]">
                ЄДРПОУ: {school.edrpou}
              </span>
            )}
            <button
              onClick={() => setLang(lang === 'uk' ? 'en' : 'uk')}
              className="flex items-center gap-1 hover:text-primary font-medium transition"
              title="Перемкнути мову"
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
          {school.logo ? (
            <img src={school.logo} alt={school.name} className="w-12 h-12 rounded-xl object-contain shadow-md" />
          ) : (
            <div className="w-12 h-12 bg-primary rounded-xl flex items-center justify-center text-white shadow-md">
              <BookOpen className="w-7 h-7" />
            </div>
          )}
          <div>
            <h1 className="text-xl md:text-2xl font-bold text-slate-900 tracking-tight">
              {school.name}
            </h1>
            <p className="text-xs text-slate-500">
              Офіційний сайт закладу загальної середньої освіти {school.founder ? `• Засновник: ${school.founder}` : ''}
            </p>
          </div>
        </div>

        {/* Dynamic navigation links from backend manifest */}
        <nav className="flex items-center gap-1 overflow-x-auto py-1 max-w-full">
          <button
            onClick={() => setCurrentTab('home')}
            className={`px-3 py-1.5 rounded-lg text-xs font-semibold transition whitespace-nowrap ${
              currentTab === 'home'
                ? 'bg-primary text-white shadow-sm'
                : 'text-slate-600 hover:text-primary hover:bg-slate-50'
            }`}
          >
            Головна
          </button>

          {navigation.map((item) => {
            const IconComponent = ICON_MAP[item.icon] || FileCheck;
            const isActive = currentTab === item.id;
            return (
              <button
                key={item.id}
                onClick={() => setCurrentTab(item.id)}
                className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-semibold transition whitespace-nowrap ${
                  isActive
                    ? 'bg-primary text-white shadow-sm'
                    : 'text-slate-600 hover:text-primary hover:bg-slate-50'
                }`}
              >
                <IconComponent className="w-3.5 h-3.5" />
                <span>{item.title}</span>
              </button>
            );
          })}
        </nav>
      </div>
    </header>
  );
};
