import React, { useState } from 'react';
import { Calendar, Clock, BookOpen } from 'lucide-react';

const BELL_SCHEDULE = [
  { lesson: 1, start: '08:30', end: '09:15', break: '15 хв' },
  { lesson: 2, start: '09:30', end: '10:15', break: '20 хв (сніданок 1-4 кл.)' },
  { lesson: 3, start: '10:35', end: '11:20', break: '20 хв (сніданок 5-11 кл.)' },
  { lesson: 4, start: '11:40', end: '12:25', break: '15 хв' },
  { lesson: 5, start: '12:40', end: '13:25', break: '10 хв' },
  { lesson: 6, start: '13:35', end: '14:20', break: '10 хв' },
  { lesson: 7, start: '14:30', end: '15:15', break: 'Кінець уроків' },
];

const SAMPLE_LESSONS = [
  { day: 'Понеділок', lessons: ['Математика (каб. 102)', 'Українська мова (каб. 102)', 'Я досліджую світ (каб. 102)', 'Фізична культура (спортзал)'] },
  { day: 'Вівторок', lessons: ['Англійська мова (каб. 204)', 'Математика (каб. 102)', 'Читання (каб. 102)', 'Мистецтво (каб. 105)'] },
  { day: 'Середа', lessons: ['Українська мова (каб. 102)', 'Я досліджую світ (каб. 102)', 'Математика (каб. 102)', 'Інформатика (комп. клас)'] },
  { day: 'Четвер', lessons: ['Читання (каб. 102)', 'Англійська мова (каб. 204)', 'Фізична культура (спортзал)', 'Дизайн і технології (каб. 102)'] },
  { day: 'П’ятниця', lessons: ['Математика (каб. 102)', 'Українська мова (каб. 102)', 'Я досліджую світ (каб. 102)', 'Година спілкування (каб. 102)'] },
];

export const ScheduleView: React.FC = () => {
  const [selectedGrade, setSelectedGrade] = useState('1-Б');

  return (
    <div className="py-8 max-w-7xl mx-auto px-4">
      {/* Title */}
      <div className="bg-gradient-to-r from-teal-900 to-slate-900 text-white rounded-2xl p-6 md:p-8 mb-8 shadow-lg">
        <div className="inline-flex items-center gap-2 bg-teal-800 px-3 py-1 rounded-full text-xs font-semibold uppercase tracking-wider text-teal-200 mb-3">
          <Calendar className="w-4 h-4" />
          <span>Організація навчального дня</span>
        </div>
        <h2 className="text-2xl md:text-3xl font-extrabold tracking-tight mb-2">
          Розклад уроків та графік дзвінків
        </h2>
        <p className="text-teal-100 text-sm md:text-base max-w-3xl leading-relaxed">
          Чіткий графік дзвінків та актуальний розклад занять для учнів ліцею.
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Bell Schedule */}
        <div className="bg-white rounded-xl p-6 border border-slate-200 shadow-sm">
          <h3 className="font-bold text-slate-900 text-lg mb-4 flex items-center gap-2">
            <Clock className="w-5 h-5 text-teal-600" />
            <span>Розклад дзвінків</span>
          </h3>

          <div className="overflow-x-auto">
            <table className="w-full text-xs text-left border-collapse">
              <thead className="bg-slate-50 text-slate-600 uppercase font-semibold border-b border-slate-200">
                <tr>
                  <th className="py-2.5 px-3">Урок</th>
                  <th className="py-2.5 px-3">Час</th>
                  <th className="py-2.5 px-3 text-right">Перерва</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100">
                {BELL_SCHEDULE.map((b) => (
                  <tr key={b.lesson} className="hover:bg-slate-50">
                    <td className="py-2.5 px-3 font-bold text-slate-900">{b.lesson}</td>
                    <td className="py-2.5 px-3 font-mono text-slate-700">{b.start} - {b.end}</td>
                    <td className="py-2.5 px-3 text-right text-slate-500">{b.break}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        {/* Lesson Schedule */}
        <div className="lg:col-span-2 bg-white rounded-xl p-6 border border-slate-200 shadow-sm">
          <div className="flex flex-wrap items-center justify-between gap-3 mb-4">
            <h3 className="font-bold text-slate-900 text-lg flex items-center gap-2">
              <BookOpen className="w-5 h-5 text-teal-600" />
              <span>Розклад уроків класу</span>
            </h3>

            <div className="flex items-center gap-2">
              <span className="text-xs text-slate-500 font-medium">Оберіть клас:</span>
              <select
                value={selectedGrade}
                onChange={(e) => setSelectedGrade(e.target.value)}
                className="text-xs border border-slate-300 rounded-lg px-2.5 py-1.5 focus:ring-2 focus:ring-teal-600 font-semibold text-slate-800"
              >
                <option value="1-А">1-А клас</option>
                <option value="1-Б">1-Б клас (НУШ)</option>
                <option value="5-А">5-А клас</option>
                <option value="10-А">10-А клас</option>
              </select>
            </div>
          </div>

          <div className="space-y-4">
            {SAMPLE_LESSONS.map((d, idx) => (
              <div key={idx} className="bg-slate-50 p-4 rounded-xl border border-slate-200">
                <h4 className="font-bold text-sm text-teal-900 mb-2 border-b border-slate-200 pb-1">
                  {d.day}
                </h4>
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-2 text-xs">
                  {d.lessons.map((lesson, lIdx) => (
                    <div key={lIdx} className="bg-white p-2.5 rounded-lg border border-slate-200 flex items-center gap-2">
                      <span className="w-5 h-5 rounded-full bg-teal-100 text-teal-800 font-bold flex items-center justify-center flex-shrink-0 text-[11px]">
                        {lIdx + 1}
                      </span>
                      <span className="text-slate-800 font-medium">{lesson}</span>
                    </div>
                  ))}
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};
