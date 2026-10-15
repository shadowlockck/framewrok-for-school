import React from 'react';
import { DollarSign, Download, Clock, CheckCircle2, TrendingUp, HeartHandshake } from 'lucide-react';

export const FinancialTransparencyView: React.FC = () => {
  return (
    <div className="py-8 max-w-7xl mx-auto px-4">
      {/* Title */}
      <div className="bg-gradient-to-r from-amber-900 to-yellow-950 text-white rounded-2xl p-6 md:p-8 mb-8 shadow-lg">
        <div className="inline-flex items-center gap-2 bg-amber-800 px-3 py-1 rounded-full text-xs font-semibold uppercase tracking-wider text-amber-200 mb-3">
          <DollarSign className="w-4 h-4" />
          <span>Фінансова відкритість (ст. 30 ч. 3 ЗУ «Про освіту»)</span>
        </div>
        <h2 className="text-2xl md:text-3xl font-extrabold tracking-tight mb-2">
          Кошторис, фінансова звітність та благодійна допомога
        </h2>
        <p className="text-amber-100 text-sm md:text-base max-w-3xl leading-relaxed">
          Заклади освіти, що отримують публічні кошти, зобов’язані оприлюднювати кошторис і фінансовий звіт
          про надходження та використання всіх коштів, товарів і послуг не пізніше ніж через <strong>10 робочих днів</strong> із дня їх затвердження.
        </p>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
        <div className="bg-white p-6 rounded-xl border border-slate-200 shadow-sm flex items-center justify-between">
          <div>
            <span className="text-xs font-semibold uppercase tracking-wider text-slate-500">Затверджений кошторис 2026</span>
            <div className="text-2xl font-black text-slate-900 mt-1">14,250,000 ₴</div>
            <span className="text-[11px] text-emerald-600 font-medium">Бюджет міста Києва</span>
          </div>
          <div className="w-12 h-12 bg-amber-50 text-amber-600 rounded-xl flex items-center justify-center">
            <TrendingUp className="w-6 h-6" />
          </div>
        </div>

        <div className="bg-white p-6 rounded-xl border border-slate-200 shadow-sm flex items-center justify-between">
          <div>
            <span className="text-xs font-semibold uppercase tracking-wider text-slate-500">Використано за III квартали</span>
            <div className="text-2xl font-black text-slate-900 mt-1">10,890,400 ₴</div>
            <span className="text-[11px] text-slate-500 font-medium">76.4% від річного плану</span>
          </div>
          <div className="w-12 h-12 bg-blue-50 text-blue-600 rounded-xl flex items-center justify-center">
            <Clock className="w-6 h-6" />
          </div>
        </div>

        <div className="bg-white p-6 rounded-xl border border-slate-200 shadow-sm flex items-center justify-between">
          <div>
            <span className="text-xs font-semibold uppercase tracking-wider text-slate-500">Благодійна допомога</span>
            <div className="text-2xl font-black text-slate-900 mt-1">184,200 ₴</div>
            <span className="text-[11px] text-indigo-600 font-medium">Обладнання, меблі, книги</span>
          </div>
          <div className="w-12 h-12 bg-indigo-50 text-indigo-600 rounded-xl flex items-center justify-center">
            <HeartHandshake className="w-6 h-6" />
          </div>
        </div>
      </div>

      {/* Reports Table */}
      <div className="bg-white rounded-xl p-6 border border-slate-200 shadow-sm mb-8">
        <h3 className="font-bold text-slate-900 text-lg mb-4 flex items-center gap-2">
          <span>Офіційні фінансові звіти та кошториси</span>
        </h3>

        <div className="overflow-x-auto">
          <table className="w-full text-sm text-left border-collapse">
            <thead className="bg-slate-50 text-slate-700 text-xs uppercase font-semibold border-b border-slate-200">
              <tr>
                <th className="py-3 px-4">Назва документа</th>
                <th className="py-3 px-4">Період / Рік</th>
                <th className="py-3 px-4">Дата затвердження</th>
                <th className="py-3 px-4">Дата оприлюднення</th>
                <th className="py-3 px-4 text-center">Дотримання 10 днів</th>
                <th className="py-3 px-4 text-right">Файл</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100">
              {[
                { title: 'Кошторис закладу на 2026 рік (зі змінами від 15.09)', period: '2026', approved: '15.09.2026', published: '22.09.2026', size: '1.2 МБ (PDF)' },
                { title: 'Звіт про надходження та використання коштів загального фонду (Форма №2)', period: 'III кв. 2026', approved: '05.10.2026', published: '12.10.2026', size: '940 КБ (PDF)' },
                { title: 'Звіт про надходження і використання коштів спеціального фонду (Форма №4)', period: 'III кв. 2026', approved: '05.10.2026', published: '12.10.2026', size: '820 КБ (PDF)' },
                { title: 'Реєстр отриманої благодійної допомоги із зазначенням вартості', period: 'Січень-Вересень 2026', approved: '01.10.2026', published: '08.10.2026', size: '450 КБ (PDF)' },
              ].map((row, idx) => (
                <tr key={idx} className="hover:bg-slate-50 transition">
                  <td className="py-3 px-4 font-medium text-slate-900">{row.title}</td>
                  <td className="py-3 px-4 text-slate-600">{row.period}</td>
                  <td className="py-3 px-4 text-slate-600 font-mono text-xs">{row.approved}</td>
                  <td className="py-3 px-4 text-slate-600 font-mono text-xs">{row.published}</td>
                  <td className="py-3 px-4 text-center">
                    <span className="inline-flex items-center gap-1 text-xs font-semibold text-emerald-700 bg-emerald-50 px-2 py-0.5 rounded">
                      <CheckCircle2 className="w-3.5 h-3.5" /> Вчасно
                    </span>
                  </td>
                  <td className="py-3 px-4 text-right">
                    <button
                      className="inline-flex items-center gap-1.5 text-primary hover:underline font-medium text-xs"
                      onClick={() => alert(`Завантаження: ${row.title}`)}
                    >
                      <Download className="w-3.5 h-3.5" />
                      <span>{row.size}</span>
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};
