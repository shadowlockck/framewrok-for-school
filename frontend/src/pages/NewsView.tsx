import React, { useState } from 'react';
import { Newspaper, BellRing, Calendar, Search } from 'lucide-react';

interface NewsItem {
  id: string;
  title: string;
  category: string;
  summary: string;
  date: string;
  isUrgent?: boolean;
}

const NEWS_LIST: NewsItem[] = [
  {
    id: '1',
    title: 'Початок прийому заяв до 1-х класів на 2026/2027 навчальний рік',
    category: 'Оголошення',
    summary: 'З 1 квітня розпочинається прийом документів для зарахування дітей, які проживають на закріпленій території обслуговування. Документи можна подати особисто, поштою або через електронну систему АІКОМ.',
    date: '14.10.2026',
    isUrgent: true,
  },
  {
    id: '2',
    title: 'Перемога учнів ліцею на Всеукраїнській олімпіаді з інформатики та робототехніки',
    category: 'Події та свята',
    summary: 'Команда учнів 10-х класів здобула дипломи І та ІІ ступенів. Щиро вітаємо наших переможців та наставників із блискучим результатом!',
    date: '10.10.2026',
  },
  {
    id: '3',
    title: 'Проведення тижня цифрової безпеки та медіаграмотності',
    category: 'Освітній процес',
    summary: 'У ліцеї відбулися інтерактивні воркшопи для учнів 5-9 класів щодо безпечної поведінки в інтернеті та протидії кібербулінгу.',
    date: '02.10.2026',
  },
];

export const NewsView: React.FC = () => {
  const [search, setSearch] = useState('');

  const filteredNews = NEWS_LIST.filter(
    (n) => n.title.toLowerCase().includes(search.toLowerCase()) || n.summary.toLowerCase().includes(search.toLowerCase())
  );

  return (
    <div className="py-8 max-w-7xl mx-auto px-4">
      {/* Title */}
      <div className="bg-gradient-to-r from-blue-900 to-slate-900 text-white rounded-2xl p-6 md:p-8 mb-8 shadow-lg">
        <div className="inline-flex items-center gap-2 bg-blue-800 px-3 py-1 rounded-full text-xs font-semibold uppercase tracking-wider text-amber-300 mb-3">
          <Newspaper className="w-4 h-4" />
          <span>Життя закладу освіти</span>
        </div>
        <h2 className="text-2xl md:text-3xl font-extrabold tracking-tight mb-2">
          Новини, анонси та важливі оголошення
        </h2>
        <p className="text-blue-200 text-sm md:text-base max-w-3xl leading-relaxed">
          Актуальна інформація про освітній процес, свята, досягнення учнів та важливі повідомлення адміністрації ліцею.
        </p>
      </div>

      {/* Urgent Announcements */}
      {filteredNews.some((n) => n.isUrgent) && (
        <div className="mb-8 space-y-4">
          {filteredNews
            .filter((n) => n.isUrgent)
            .map((item) => (
              <div
                key={item.id}
                className="bg-amber-50 border-l-4 border-amber-500 rounded-xl p-5 shadow-sm flex items-start gap-4"
              >
                <div className="p-2 bg-amber-100 rounded-lg text-amber-800 flex-shrink-0">
                  <BellRing className="w-6 h-6 animate-bounce" />
                </div>
                <div>
                  <div className="flex items-center gap-2 mb-1">
                    <span className="bg-amber-500 text-slate-950 font-black text-[10px] uppercase px-2 py-0.5 rounded">
                      Термінове оголошення
                    </span>
                    <span className="text-xs text-slate-500 font-mono">{item.date}</span>
                  </div>
                  <h3 className="font-bold text-slate-900 text-lg mb-1">{item.title}</h3>
                  <p className="text-slate-700 text-sm leading-relaxed">{item.summary}</p>
                </div>
              </div>
            ))}
        </div>
      )}

      {/* Search */}
      <div className="mb-6 relative max-w-md">
        <Search className="w-4 h-4 text-slate-400 absolute left-3 top-3" />
        <input
          type="text"
          placeholder="Пошук новин..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          className="w-full pl-9 pr-4 py-2 border border-slate-300 rounded-lg text-sm focus:ring-2 focus:ring-blue-600 focus:outline-none"
        />
      </div>

      {/* News Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {filteredNews
          .filter((n) => !n.isUrgent)
          .map((item) => (
            <div
              key={item.id}
              className="bg-white rounded-xl p-6 border border-slate-200 shadow-sm hover:shadow-md transition flex flex-col justify-between"
            >
              <div>
                <div className="flex items-center justify-between gap-2 mb-3">
                  <span className="text-xs font-semibold uppercase tracking-wider text-primary bg-blue-50 px-2 py-0.5 rounded">
                    {item.category}
                  </span>
                  <span className="text-xs text-slate-400 font-mono flex items-center gap-1">
                    <Calendar className="w-3.5 h-3.5" />
                    {item.date}
                  </span>
                </div>
                <h3 className="font-bold text-slate-900 text-lg mb-2 leading-snug">{item.title}</h3>
                <p className="text-slate-600 text-sm leading-relaxed">{item.summary}</p>
              </div>
            </div>
          ))}
      </div>
    </div>
  );
};
