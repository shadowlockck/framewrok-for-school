import React, { useState } from 'react';
import { FileCheck, Search, Download, Calendar, CheckCircle2 } from 'lucide-react';

interface LegalDoc {
  id: string;
  category: string;
  lawReference: string;
  title: string;
  status: 'published' | 'updated' | 'active';
  updatedAt: string;
  fileSize?: string;
  description: string;
}

const LEGAL_DOCUMENTS: LegalDoc[] = [
  {
    id: '1',
    category: 'Установчі документи',
    lawReference: 'ст. 30 ч. 2 ЗУ «Про освіту»',
    title: 'Статут закладу загальної середньої освіти',
    status: 'active',
    updatedAt: '12.01.2026',
    fileSize: '2.4 МБ (PDF)',
    description: 'Затверджений рішенням сесії міської ради. Визначає мету, завдання, структуру та статус закладу.',
  },
  {
    id: '2',
    category: 'Ліцензування та акредитація',
    lawReference: 'ст. 30 ч. 2 ЗУ «Про освіту»',
    title: 'Ліцензія на провадження освітньої діяльності (початкова, базова та профільна середня освіта)',
    status: 'active',
    updatedAt: '05.09.2023',
    fileSize: '840 КБ (PDF)',
    description: 'Видана Департаментом освіти і науки. Безстрокова.',
  },
  {
    id: '3',
    category: 'Ліцензування та акредитація',
    lawReference: 'ст. 30 ч. 2 ЗУ «Про освіту»',
    title: 'Сертифікати про акредитацію освітніх програм',
    status: 'active',
    updatedAt: '15.11.2025',
    fileSize: '1.1 МБ (PDF)',
    description: 'Сертифікати відповідності освітніх програм Державному стандарту загальної середньої освіти.',
  },
  {
    id: '4',
    category: 'Управління та кадри',
    lawReference: 'ст. 30 ч. 2 ЗУ «Про освіту»',
    title: 'Структура та органи управління закладу освіти',
    status: 'active',
    updatedAt: '01.09.2026',
    fileSize: '512 КБ (PDF)',
    description: 'Організаційна структура: директор, педагогічна рада, піклувальна рада, органи учнівського самоврядування.',
  },
  {
    id: '5',
    category: 'Управління та кадри',
    lawReference: 'ст. 30 ч. 2 ЗУ «Про освіту»',
    title: 'Кадровий склад закладу згідно з ліцензійними умовами',
    status: 'updated',
    updatedAt: '01.10.2026',
    fileSize: '1.8 МБ (PDF)',
    description: 'Список педагогічних працівників: кваліфікаційні категорії, педагогічні звання, підвищення кваліфікації.',
  },
  {
    id: '6',
    category: 'Освітній процес',
    lawReference: 'ст. 30 ч. 2 ЗУ «Про освіту»',
    title: 'Освітня програма закладу та перелік навчальних компонентів',
    status: 'active',
    updatedAt: '28.08.2026',
    fileSize: '3.2 МБ (PDF)',
    description: 'Навчальний план, опис модельних навчальних програм НУШ, форма оцінювання результатів навчання.',
  },
  {
    id: '7',
    category: 'Освітній процес',
    lawReference: 'ст. 30 ч. 2 ЗУ «Про освіту»',
    title: 'Мова освітнього процесу',
    status: 'active',
    updatedAt: '01.09.2026',
    description: 'Мовою освітнього процесу в закладі є державна мова — українська. Іноземні мови: англійська, німецька.',
  },
  {
    id: '8',
    category: 'Місткість та учні',
    lawReference: 'ст. 30 ч. 2 ЗУ «Про освіту»',
    title: 'Ліцензований обсяг та фактична кількість здобувачів освіти',
    status: 'updated',
    updatedAt: '05.10.2026',
    description: 'Ліцензований обсяг: 900 учнів. Фактично навчається: 824 учні (у тому числі 34 дитини на сімейній та дистанційній формах).',
  },
  {
    id: '9',
    category: 'Матеріально-технічне забезпечення',
    lawReference: 'ст. 30 ч. 2 ЗУ «Про освіту»',
    title: 'Матеріально-технічне забезпечення та укриття закладу',
    status: 'active',
    updatedAt: '10.09.2026',
    fileSize: '2.0 МБ (PDF)',
    description: 'Характеристика навчальних кабінетів, комп’ютерних класів, спортивної зали, сертифікованого укриття цивільного захисту на 950 місць.',
  },
  {
    id: '10',
    category: 'Інклюзія та доступність',
    lawReference: 'ст. 30 ч. 2 ЗУ «Про освіту»',
    title: 'Умови доступності закладу освіти для осіб з особливими освітніми потребами (ООП)',
    status: 'active',
    updatedAt: '20.08.2026',
    description: 'Безбар’єрний доступ: пандус на вході, спеціально обладнані санітарні кімнати, ресурсна кімната, асистенти вчителя.',
  },
  {
    id: '11',
    category: 'Якість освіти та звіти',
    lawReference: 'ст. 30 ч. 2, ст. 45 ЗУ «Про освіту»',
    title: 'Річний звіт про діяльність закладу та результати моніторингу якості',
    status: 'updated',
    updatedAt: '25.06.2026',
    fileSize: '4.5 МБ (PDF)',
    description: 'Публічний звіт директора перед педагогічним колективом та громадськістю за навчальний рік.',
  },
  {
    id: '12',
    category: 'Вакансії та конкурси',
    lawReference: 'ст. 30 ЗУ «Про освіту», ст. 39 ЗУ «Про повну загальну середню освіту»',
    title: 'Вакантні посади та умови проведення конкурсу',
    status: 'active',
    updatedAt: '14.10.2026',
    description: 'Оголошення про конкурси на заміщення вакантних посад педагогічних працівників та керівника закладу.',
  },
];

export const LegalRegisterView: React.FC = () => {
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedCategory, setSelectedCategory] = useState<string>('all');

  const categories = ['all', ...Array.from(new Set(LEGAL_DOCUMENTS.map((d) => d.category)))];

  const filteredDocs = LEGAL_DOCUMENTS.filter((doc) => {
    const matchesSearch =
      doc.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
      doc.description.toLowerCase().includes(searchTerm.toLowerCase()) ||
      doc.lawReference.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesCat = selectedCategory === 'all' || doc.category === selectedCategory;
    return matchesSearch && matchesCat;
  });

  return (
    <div className="py-8 max-w-7xl mx-auto px-4">
      {/* Header Info */}
      <div className="bg-gradient-to-r from-blue-900 to-indigo-950 text-white rounded-2xl p-6 md:p-8 mb-8 shadow-lg">
        <div className="inline-flex items-center gap-2 bg-blue-800/80 px-3 py-1 rounded-full text-xs font-semibold uppercase tracking-wider text-amber-300 mb-3">
          <FileCheck className="w-4 h-4" />
          <span>Нормативний реєстр</span>
        </div>
        <h2 className="text-2xl md:text-3xl font-extrabold tracking-tight mb-2">
          Прозорість та інформаційна відкритість закладу освіти
        </h2>
        <p className="text-blue-200 text-sm md:text-base max-w-3xl leading-relaxed">
          Згідно зі <strong>статтею 30 Закону України «Про освіту»</strong> заклад зобов’язаний забезпечувати
          відкритий доступ до інформації та документів про свою діяльність.
        </p>
      </div>

      {/* Filters & Search */}
      <div className="bg-white p-4 rounded-xl shadow-sm border border-slate-200 mb-6 flex flex-wrap items-center justify-between gap-4">
        <div className="flex-1 min-w-[280px] relative">
          <Search className="w-4 h-4 text-slate-400 absolute left-3 top-3" />
          <input
            type="text"
            placeholder="Пошук за назвою документа або статтею закону..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="w-full pl-9 pr-4 py-2 border border-slate-300 rounded-lg text-sm focus:ring-2 focus:ring-blue-600 focus:outline-none"
          />
        </div>

        <div className="flex flex-wrap items-center gap-2">
          {categories.map((cat) => (
            <button
              key={cat}
              onClick={() => setSelectedCategory(cat)}
              className={`px-3 py-1.5 rounded-lg text-xs font-medium transition ${selectedCategory === cat ? 'bg-primary text-white' : 'bg-slate-100 text-slate-700 hover:bg-slate-200'}`}
            >
              {cat === 'all' ? 'Всі документи' : cat}
            </button>
          ))}
        </div>
      </div>

      {/* Documents Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {filteredDocs.map((doc) => (
          <div
            key={doc.id}
            className="bg-white rounded-xl p-5 border border-slate-200 shadow-sm hover:shadow-md transition flex flex-col justify-between"
          >
            <div>
              <div className="flex items-start justify-between gap-2 mb-2">
                <span className="text-[11px] font-semibold uppercase tracking-wider text-primary bg-blue-50 px-2 py-0.5 rounded">
                  {doc.category}
                </span>
                <span className="text-[11px] text-slate-500 font-mono flex items-center gap-1">
                  <Calendar className="w-3 h-3" />
                  {doc.updatedAt}
                </span>
              </div>

              <h3 className="font-bold text-slate-900 text-base mb-1.5 leading-snug">
                {doc.title}
              </h3>

              <p className="text-slate-600 text-xs mb-3 leading-relaxed">
                {doc.description}
              </p>
            </div>

            <div className="pt-3 border-t border-slate-100 flex items-center justify-between mt-2">
              <span className="text-[11px] text-slate-400 italic">
                {doc.lawReference}
              </span>

              {doc.fileSize ? (
                <button
                  className="inline-flex items-center gap-1.5 bg-slate-100 hover:bg-primary hover:text-white text-slate-700 px-3 py-1.5 rounded-lg text-xs font-medium transition"
                  onClick={() => alert(`Завантаження документа: ${doc.title}`)}
                >
                  <Download className="w-3.5 h-3.5" />
                  <span>{doc.fileSize}</span>
                </button>
              ) : (
                <span className="inline-flex items-center gap-1 text-emerald-600 text-xs font-medium">
                  <CheckCircle2 className="w-3.5 h-3.5" />
                  <span>Текстовий розділ</span>
                </span>
              )}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
