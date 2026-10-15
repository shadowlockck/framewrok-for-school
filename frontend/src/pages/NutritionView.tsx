import React, { useState, useEffect } from 'react';
import { Utensils, Calendar, ShieldCheck, Phone, Building2, Coffee, Soup, Apple } from 'lucide-react';
import { fetchFromAPI } from '../api/client';

interface DailyMenuData {
  id: number;
  menu_date: string;
  age_group: '1_4' | '5_9' | '10_11';
  breakfast: string;
  lunch: string;
  snack?: string;
  photo?: string | null;
}

interface ProviderData {
  id: number;
  company_name: string;
  contract_number: string;
  contact_person: string;
  phone: string;
}

const FALLBACK_MENUS: DailyMenuData[] = [
  {
    id: 1,
    menu_date: '2026-10-15',
    age_group: '1_4',
    breakfast: 'Каша вівсяна з яблуком та корицею (150г), чай трав’яний (200мл), банан (100г)',
    lunch: 'Суп овочевий з цільнозерновими грінками (200г), тефтелі рибні парових сортів (80г), пюре картопляно-гарбузове (130г), узвар (200мл)',
    snack: 'Сирники запечені з родзинками (100г), кисіль ягідний (180мл)',
  },
  {
    id: 2,
    menu_date: '2026-10-15',
    age_group: '5_9',
    breakfast: 'Омлет запечений з овочами (150г), хліб цільнозерновий (30г), какао з молоком без цукру (200мл)',
    lunch: 'Борщ український з квасолею (250г), філе куряче тушковане в томатному соусі (100г), каша гречана розсипчаста (150г), салат з буряка та чорносливу (100г), узвар (200мл)',
    snack: 'Яблуко запечене з сиром (120г), сік яблучний прямого віджиму (200мл)',
  },
  {
    id: 3,
    menu_date: '2026-10-15',
    age_group: '10_11',
    breakfast: 'Запіканка сирна з курагою (180г), ягідний соус (30г), чай зелений (200мл)',
    lunch: 'Суп-крем гороховий (250г), котлета яловича парова (100г), рис з овочами (180г), салат з моркви та капусти (100г), компот зі свіжих яблук (200мл)',
    snack: 'Булочка з висівками (60г), кефір вітамінізований 2.5% (200мл)',
  },
];

const FALLBACK_PROVIDER: ProviderData = {
  id: 1,
  company_name: 'КП «Шкільне якісне харчування»',
  contract_number: '№ 45-Х від 15.08.2026',
  contact_person: 'Коваленко Олена Василівна (головний технолог)',
  phone: '+380 44 234-56-78',
};

export const NutritionView: React.FC = () => {
  const [selectedGroup, setSelectedGroup] = useState<'1_4' | '5_9' | '10_11'>('1_4');
  const [menus, setMenus] = useState<DailyMenuData[]>(FALLBACK_MENUS);
  const [provider, setProvider] = useState<ProviderData>(FALLBACK_PROVIDER);

  useEffect(() => {
    fetchFromAPI<DailyMenuData[]>('/nutrition/daily-menus/', FALLBACK_MENUS)
      .then((data) => {
        if (data && data.length > 0) setMenus(data);
      })
      .catch(() => {});

    fetchFromAPI<ProviderData[]>('/nutrition/providers/', [FALLBACK_PROVIDER])
      .then((data) => {
        if (data && data.length > 0) setProvider(data[0]);
      })
      .catch(() => {});
  }, []);

  const currentMenu = menus.find((m) => m.age_group === selectedGroup) || menus[0];

  return (
    <div className="py-8 max-w-7xl mx-auto px-4">
      {/* Title banner */}
      <div className="bg-gradient-to-r from-emerald-900 to-teal-950 text-white rounded-2xl p-6 md:p-8 mb-8 shadow-lg">
        <div className="inline-flex items-center gap-2 bg-emerald-800 px-3 py-1 rounded-full text-xs font-semibold uppercase tracking-wider text-emerald-200 mb-3">
          <Utensils className="w-4 h-4" />
          <span>Харчування здобувачів освіти</span>
        </div>
        <h2 className="text-2xl md:text-3xl font-extrabold tracking-tight mb-2">
          Щоденне меню та організація харчування
        </h2>
        <p className="text-emerald-100 text-sm md:text-base max-w-3xl leading-relaxed">
          Оприлюднення щоденного меню, розкладу прийому їжі та відомостей про організацію, яка надає послуги харчування відповідно до вимог безпечності харчових продуктів (HACCP).
        </p>
      </div>

      {/* Age group selector tabs */}
      <div className="flex flex-wrap gap-2 mb-6">
        <button
          onClick={() => setSelectedGroup('1_4')}
          className={`px-4 py-2.5 rounded-xl font-bold text-xs md:text-sm transition flex items-center gap-2 ${
            selectedGroup === '1_4'
              ? 'bg-emerald-700 text-white shadow-md'
              : 'bg-white text-slate-700 border border-slate-200 hover:bg-slate-50'
          }`}
        >
          <span>1-4 класи</span>
          <span className="text-[11px] font-normal opacity-80">(Початкова школа)</span>
        </button>

        <button
          onClick={() => setSelectedGroup('5_9')}
          className={`px-4 py-2.5 rounded-xl font-bold text-xs md:text-sm transition flex items-center gap-2 ${
            selectedGroup === '5_9'
              ? 'bg-emerald-700 text-white shadow-md'
              : 'bg-white text-slate-700 border border-slate-200 hover:bg-slate-50'
          }`}
        >
          <span>5-9 класи</span>
          <span className="text-[11px] font-normal opacity-80">(Базова школа)</span>
        </button>

        <button
          onClick={() => setSelectedGroup('10_11')}
          className={`px-4 py-2.5 rounded-xl font-bold text-xs md:text-sm transition flex items-center gap-2 ${
            selectedGroup === '10_11'
              ? 'bg-emerald-700 text-white shadow-md'
              : 'bg-white text-slate-700 border border-slate-200 hover:bg-slate-50'
          }`}
        >
          <span>10-11 класи</span>
          <span className="text-[11px] font-normal opacity-80">(Старша школа)</span>
        </button>
      </div>

      {/* Current Menu Card */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-8">
        <div className="lg:col-span-2 bg-white rounded-2xl p-6 md:p-8 border border-slate-200 shadow-sm">
          <div className="flex items-center justify-between border-b border-slate-100 pb-4 mb-6">
            <div>
              <span className="text-xs font-semibold uppercase tracking-wider text-emerald-700">
                Затверджене меню на сьогодні
              </span>
              <h3 className="text-xl font-bold text-slate-900 mt-0.5">
                {currentMenu?.menu_date || 'Сьогодні'}
              </h3>
            </div>
            <div className="inline-flex items-center gap-1.5 bg-emerald-50 text-emerald-800 text-xs px-3 py-1 rounded-full font-medium">
              <Calendar className="w-3.5 h-3.5" />
              <span>Збалансоване харчування</span>
            </div>
          </div>

          <div className="space-y-6">
            {/* Breakfast */}
            <div className="flex items-start gap-4">
              <div className="w-10 h-10 rounded-xl bg-amber-50 text-amber-700 flex items-center justify-center flex-shrink-0">
                <Coffee className="w-5 h-5" />
              </div>
              <div className="flex-1">
                <h4 className="font-bold text-slate-900 text-sm mb-1">Сніданок</h4>
                <p className="text-xs md:text-sm text-slate-700 leading-relaxed bg-slate-50 p-3 rounded-lg border border-slate-100">
                  {currentMenu?.breakfast || 'Інформація уточнюється'}
                </p>
              </div>
            </div>

            {/* Lunch */}
            <div className="flex items-start gap-4">
              <div className="w-10 h-10 rounded-xl bg-emerald-50 text-emerald-700 flex items-center justify-center flex-shrink-0">
                <Soup className="w-5 h-5" />
              </div>
              <div className="flex-1">
                <h4 className="font-bold text-slate-900 text-sm mb-1">Обід</h4>
                <p className="text-xs md:text-sm text-slate-700 leading-relaxed bg-slate-50 p-3 rounded-lg border border-slate-100">
                  {currentMenu?.lunch || 'Інформація уточнюється'}
                </p>
              </div>
            </div>

            {/* Snack */}
            {currentMenu?.snack && (
              <div className="flex items-start gap-4">
                <div className="w-10 h-10 rounded-xl bg-indigo-50 text-indigo-700 flex items-center justify-center flex-shrink-0">
                  <Apple className="w-5 h-5" />
                </div>
                <div className="flex-1">
                  <h4 className="font-bold text-slate-900 text-sm mb-1">Полуденок / Підвечірок</h4>
                  <p className="text-xs md:text-sm text-slate-700 leading-relaxed bg-slate-50 p-3 rounded-lg border border-slate-100">
                    {currentMenu.snack}
                  </p>
                </div>
              </div>
            )}
          </div>
        </div>

        {/* Provider and Quality Info */}
        <div className="space-y-6">
          <div className="bg-white rounded-2xl p-6 border border-slate-200 shadow-sm">
            <div className="flex items-center gap-2 text-slate-900 font-bold text-base mb-4">
              <Building2 className="w-5 h-5 text-emerald-600" />
              <span>Організатор харчування</span>
            </div>
            <div className="space-y-3 text-xs">
              <div>
                <span className="text-slate-500 block">Постачальник:</span>
                <span className="font-semibold text-slate-800">{provider.company_name}</span>
              </div>
              <div>
                <span className="text-slate-500 block">Договір:</span>
                <span className="font-medium text-slate-700">{provider.contract_number}</span>
              </div>
              <div>
                <span className="text-slate-500 block">Відповідальна особа:</span>
                <span className="font-medium text-slate-700">{provider.contact_person}</span>
              </div>
              <div className="pt-2 border-t border-slate-100 flex items-center gap-2">
                <Phone className="w-4 h-4 text-emerald-600 flex-shrink-0" />
                <a href={`tel:${provider.phone}`} className="text-emerald-700 font-bold hover:underline">
                  {provider.phone}
                </a>
              </div>
            </div>
          </div>

          <div className="bg-emerald-50 rounded-2xl p-6 border border-emerald-100 text-emerald-900">
            <div className="flex items-center gap-2 font-bold text-sm mb-2">
              <ShieldCheck className="w-5 h-5 text-emerald-700" />
              <span>Стандарти безпеки НАССР</span>
            </div>
            <p className="text-xs leading-relaxed text-emerald-800">
              Харчування організовано відповідно до Санітарного регламенту для закладів загальної середньої освіти та Порядку організації харчування, затвердженого Постановою КМУ № 305.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};
