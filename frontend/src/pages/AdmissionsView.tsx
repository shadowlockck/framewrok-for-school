import React, { useState } from 'react';
import { Users, MapPin, ShieldCheck, FileSpreadsheet, Search } from 'lucide-react';

interface ClassSlot {
  grade: string;
  totalCapacity: number;
  enrolled: number;
  availableSlots: number;
}

const CLASS_DATA: ClassSlot[] = [
  { grade: '1-А', totalCapacity: 30, enrolled: 30, availableSlots: 0 },
  { grade: '1-Б', totalCapacity: 30, enrolled: 28, availableSlots: 2 },
  { grade: '1-В', totalCapacity: 30, enrolled: 27, availableSlots: 3 },
  { grade: '2 класи (разом)', totalCapacity: 90, enrolled: 87, availableSlots: 3 },
  { grade: '3 класи (разом)', totalCapacity: 90, enrolled: 89, availableSlots: 1 },
  { grade: '4 класи (разом)', totalCapacity: 90, enrolled: 85, availableSlots: 5 },
  { grade: '5-9 класи (базова освіта)', totalCapacity: 450, enrolled: 420, availableSlots: 30 },
  { grade: '10-11 класи (профільна)', totalCapacity: 120, enrolled: 110, availableSlots: 10 },
];

const TERRITORY_STREETS = [
  'вул. Освітня: парні буд. 2-24, непарні 1-31',
  'вул. Шкільна: всі будинки',
  'просп. Науки: буд. 42, 44, 46, 48/1',
  'пров. Гімназійний: всі будинки',
  'вул. Тараса Шевченка: буд. 100-140',
];

export const AdmissionsView: React.FC = () => {
  const [streetQuery, setStreetQuery] = useState('');

  const filteredTerritory = TERRITORY_STREETS.filter((s) =>
    s.toLowerCase().includes(streetQuery.toLowerCase())
  );

  return (
    <div className="py-8 max-w-7xl mx-auto px-4">
      {/* Title */}
      <div className="bg-gradient-to-r from-emerald-900 to-teal-950 text-white rounded-2xl p-6 md:p-8 mb-8 shadow-lg">
        <div className="inline-flex items-center gap-2 bg-emerald-800 px-3 py-1 rounded-full text-xs font-semibold uppercase tracking-wider text-emerald-200 mb-3">
          <Users className="w-4 h-4" />
          <span>Кампанія зарахування 2026</span>
        </div>
        <h2 className="text-2xl md:text-3xl font-extrabold tracking-tight mb-2">
          Зарахування учнів, закріплена територія та вільні місця
        </h2>
        <p className="text-emerald-100 text-sm md:text-base max-w-3xl leading-relaxed">
          Відповідно до наказу МОН та Порядку зарахування, відрахування та переведення учнів.
          Заяви можуть подаватися особисто, електронною поштою або через систему <strong>АІКОМ</strong>.
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8 mb-8">
        {/* Available slots table */}
        <div className="lg:col-span-2 bg-white rounded-xl p-6 border border-slate-200 shadow-sm">
          <div className="flex items-center justify-between mb-4">
            <h3 className="font-bold text-slate-900 text-lg flex items-center gap-2">
              <FileSpreadsheet className="w-5 h-5 text-emerald-600" />
              <span>Наявність вільних місць у класах</span>
            </h3>
            <span className="text-xs bg-slate-100 text-slate-600 px-2.5 py-1 rounded-md font-medium">
              Оновлено: щоденно
            </span>
          </div>

          <div className="overflow-x-auto">
            <table className="w-full text-sm text-left border-collapse">
              <thead className="bg-slate-50 text-slate-700 text-xs uppercase font-semibold border-b border-slate-200">
                <tr>
                  <th className="py-3 px-4">Клас / Паралель</th>
                  <th className="py-3 px-4 text-center">Спроможність</th>
                  <th className="py-3 px-4 text-center">Фактично</th>
                  <th className="py-3 px-4 text-center">Вільні місця</th>
                  <th className="py-3 px-4 text-right">Статус</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100">
                {CLASS_DATA.map((item, idx) => (
                  <tr key={idx} className="hover:bg-slate-50 transition">
                    <td className="py-3 px-4 font-medium text-slate-900">{item.grade}</td>
                    <td className="py-3 px-4 text-center text-slate-600">{item.totalCapacity}</td>
                    <td className="py-3 px-4 text-center text-slate-600">{item.enrolled}</td>
                    <td className="py-3 px-4 text-center font-bold">
                      <span className={item.availableSlots > 0 ? 'text-emerald-600' : 'text-slate-400'}>
                        {item.availableSlots}
                      </span>
                    </td>
                    <td className="py-3 px-4 text-right">
                      {item.availableSlots > 0 ? (
                        <span className="inline-flex items-center gap-1 text-xs font-semibold text-emerald-700 bg-emerald-50 px-2 py-0.5 rounded">
                          Є місця
                        </span>
                      ) : (
                        <span className="inline-flex items-center gap-1 text-xs font-semibold text-rose-700 bg-rose-50 px-2 py-0.5 rounded">
                          Набір закрито
                        </span>
                      )}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        {/* Territory Lookup */}
        <div className="bg-white rounded-xl p-6 border border-slate-200 shadow-sm flex flex-col justify-between">
          <div>
            <h3 className="font-bold text-slate-900 text-lg flex items-center gap-2 mb-3">
              <MapPin className="w-5 h-5 text-emerald-600" />
              <span>Територія обслуговування</span>
            </h3>
            <p className="text-xs text-slate-500 mb-4">
              Діти, які зареєстровані або проживають на закріпленій території, мають право першочергового зарахування.
            </p>

            <div className="relative mb-3">
              <Search className="w-4 h-4 text-slate-400 absolute left-3 top-3" />
              <input
                type="text"
                placeholder="Введіть назву вулиці..."
                value={streetQuery}
                onChange={(e) => setStreetQuery(e.target.value)}
                className="w-full pl-9 pr-3 py-2 border border-slate-300 rounded-lg text-xs focus:ring-2 focus:ring-emerald-600 focus:outline-none"
              />
            </div>

            <div className="bg-slate-50 rounded-lg p-3 max-h-60 overflow-y-auto space-y-2 border border-slate-200">
              {filteredTerritory.length > 0 ? (
                filteredTerritory.map((street, idx) => (
                  <div key={idx} className="text-xs text-slate-700 flex items-start gap-2">
                    <span className="text-emerald-600 font-bold">•</span>
                    <span>{street}</span>
                  </div>
                ))
              ) : (
                <div className="text-xs text-slate-500 py-4 text-center">
                  Вулицю не знайдено на закріпленій території.
                </div>
              )}
            </div>
          </div>

          <div className="mt-4 pt-3 border-t border-slate-100">
            <span className="text-[11px] text-slate-500">
              Закріплено розпорядженням районної державної адміністрації.
            </span>
          </div>
        </div>
      </div>

      {/* GDPR / Personal Data Protection Banner for Enrolled Lists */}
      <div className="bg-amber-50 border border-amber-200 rounded-xl p-5 mb-8">
        <div className="flex items-start gap-3">
          <ShieldCheck className="w-6 h-6 text-amber-700 flex-shrink-0 mt-0.5" />
          <div>
            <h4 className="font-bold text-amber-900 text-sm mb-1">
              Дотримання Закону України «Про захист персональних даних»
            </h4>
            <p className="text-amber-800 text-xs leading-relaxed">
              Списки зарахованих учнів оприлюднюються <strong>виключно із зазначенням їхніх прізвищ</strong> (без імені,
              по батькові, адрес та інших ідентифікаційних даних). Накази про утворення конкурсної комісії для
              проведення жеребкування та результати жеребкування розміщуються у 2-денний термін.
            </p>
          </div>
        </div>
      </div>

      {/* Forms of Education Info */}
      <div className="bg-white rounded-xl p-6 border border-slate-200 shadow-sm">
        <h3 className="font-bold text-slate-900 text-lg mb-4">
          Доступні форми здобуття освіти в закладі
        </h3>
        <div className="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-5 gap-3">
          {[
            { title: 'Очна (денна)', desc: 'Безпосередня участь здобувачів у навчальному процесі в класах.' },
            { title: 'Дистанційна', desc: 'Індивідуалізований процес в онлайн-середовищі з використанням ІКТ.' },
            { title: 'Екстернат', desc: 'Самостійне засвоєння програми з проходженням річного оцінювання.' },
            { title: 'Сімейна (домашня)', desc: 'Організація навчання батьками з атестацією в школі.' },
            { title: 'Педагогічний патронаж', desc: 'Індивідуальний супровід учителями за станом здоров’я.' },
          ].map((form, idx) => (
            <div key={idx} className="bg-slate-50 p-4 rounded-lg border border-slate-200">
              <h5 className="font-bold text-slate-900 text-xs mb-1 text-emerald-800">{form.title}</h5>
              <p className="text-[11px] text-slate-600 leading-snug">{form.desc}</p>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};
