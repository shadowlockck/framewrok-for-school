import React, { useState } from 'react';
import { ShieldAlert, Send, CheckCircle2, Lock, FileText, PhoneCall, AlertCircle } from 'lucide-react';
import { submitConfidentialReport } from '../api/client';

export const SafetyView: React.FC = () => {
  const [role, setRole] = useState<'student' | 'parent' | 'teacher' | 'anonymous'>('student');
  const [description, setDescription] = useState('');
  const [contact, setContact] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [feedback, setFeedback] = useState<{ type: 'success' | 'error'; message: string } | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!description.trim()) {
      setFeedback({ type: 'error', message: 'Будь ласка, опишіть ситуацію чи обставини звернення.' });
      return;
    }

    setIsSubmitting(true);
    setFeedback(null);

    const res = await submitConfidentialReport({
      reporter_role: role,
      incident_description: description.trim(),
      contact_feedback: contact.trim() || undefined,
    });

    setIsSubmitting(false);
    if (res.success) {
      setFeedback({ type: 'success', message: res.message });
      setDescription('');
      setContact('');
    } else {
      setFeedback({ type: 'error', message: res.message });
    }
  };

  return (
    <div className="py-8 max-w-7xl mx-auto px-4">
      {/* Title */}
      <div className="bg-gradient-to-r from-rose-950 via-red-900 to-rose-900 text-white rounded-2xl p-6 md:p-8 mb-8 shadow-lg">
        <div className="inline-flex items-center gap-2 bg-rose-800/80 px-3 py-1 rounded-full text-xs font-semibold uppercase tracking-wider text-rose-200 mb-3">
          <ShieldAlert className="w-4 h-4" />
          <span>Безпечне освітнє середовище</span>
        </div>
        <h2 className="text-2xl md:text-3xl font-extrabold tracking-tight mb-2">
          Запобігання та протидія булінгу (цькуванню)
        </h2>
        <p className="text-rose-100 text-sm md:text-base max-w-3xl leading-relaxed">
          Відповідно до ст. 30 ЗУ «Про освіту» заклад освіти забезпечує відкритість плану заходів щодо протидії булінгу, порядку подання та розгляду заяв, а також гарантує конфіденційність кожному заявнику.
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
        {/* Left column: Policies & Contacts */}
        <div className="lg:col-span-7 space-y-6">
          <div className="bg-white rounded-2xl p-6 border border-slate-200 shadow-sm">
            <h3 className="text-lg font-bold text-slate-900 mb-4 flex items-center gap-2">
              <FileText className="w-5 h-5 text-rose-600" />
              <span>Порядок реагування та план заходів</span>
            </h3>
            <div className="space-y-4 text-xs md:text-sm text-slate-700 leading-relaxed">
              <div className="p-3 bg-slate-50 rounded-xl border border-slate-100">
                <span className="font-bold text-slate-900 block mb-1">1. Прийом та реєстрація заяви</span>
                <span>Заяви приймаються керівником закладу в письмовій формі або через електронну конфіденційну форму на цьому сайті.</span>
              </div>
              <div className="p-3 bg-slate-50 rounded-xl border border-slate-100">
                <span className="font-bold text-slate-900 block mb-1">2. Скликання комісії (до 3 робочих днів)</span>
                <span>Керівник закладу видає наказ про проведення розслідування та скликає комісію з розгляду випадків булінгу.</span>
              </div>
              <div className="p-3 bg-slate-50 rounded-xl border border-slate-100">
                <span className="font-bold text-slate-900 block mb-1">3. Психологічна підтримка та невідкладні заходи</span>
                <span>Залучення практичного психолога та соціального педагога для надання допомоги потерпілому та корекційної роботи.</span>
              </div>
            </div>
          </div>

          <div className="bg-rose-50 rounded-2xl p-6 border border-rose-100">
            <h4 className="font-bold text-rose-950 text-sm mb-3 flex items-center gap-2">
              <PhoneCall className="w-4 h-4 text-rose-700" />
              <span>Гарячі лінії психологічної підтримки та захисту прав дітей</span>
            </h4>
            <ul className="text-xs space-y-2 text-rose-900">
              <li><strong>Національна дитяча гаряча лінія:</strong> 0 800 500 225 або 116 111 (безкоштовно з мобільних)</li>
              <li><strong>Гаряча лінія з протидії булінгу:</strong> 116 000</li>
              <li><strong>Уповноважений Верховної Ради з прав людини:</strong> 0 800 50 17 20</li>
            </ul>
          </div>
        </div>

        {/* Right column: Confidential Submission Form */}
        <div className="lg:col-span-5">
          <div className="bg-white rounded-2xl p-6 md:p-8 border border-slate-200 shadow-sm">
            <div className="flex items-center gap-2 mb-2">
              <Lock className="w-5 h-5 text-rose-600" />
              <h3 className="font-bold text-slate-900 text-lg">Подати конфіденційне звернення</h3>
            </div>
            <p className="text-xs text-slate-600 mb-6">
              Ваше повідомлення надсилається виключно комісії закладу. Ви можете обрати статус анонімного відправника.
            </p>

            {feedback && (
              <div
                className={`p-4 rounded-xl text-xs flex items-start gap-2.5 mb-6 ${
                  feedback.type === 'success'
                    ? 'bg-emerald-50 text-emerald-900 border border-emerald-200'
                    : 'bg-rose-50 text-rose-900 border border-rose-200'
                }`}
              >
                {feedback.type === 'success' ? (
                  <CheckCircle2 className="w-4 h-4 text-emerald-600 flex-shrink-0 mt-0.5" />
                ) : (
                  <AlertCircle className="w-4 h-4 text-rose-600 flex-shrink-0 mt-0.5" />
                )}
                <span>{feedback.message}</span>
              </div>
            )}

            <form onSubmit={handleSubmit} className="space-y-4">
              <div>
                <label className="block text-xs font-semibold text-slate-700 mb-1.5">
                  Ваш статус у закладі освіти:
                </label>
                <select
                  value={role}
                  onChange={(e) => setRole(e.target.value as any)}
                  className="w-full border border-slate-300 rounded-xl p-2.5 text-xs text-slate-800 bg-white focus:outline-none focus:ring-2 focus:ring-rose-500"
                >
                  <option value="student">Учень / учениця</option>
                  <option value="parent">Батьки / законні представники</option>
                  <option value="teacher">Педагогічний працівник</option>
                  <option value="anonymous">Анонімне повідомлення</option>
                </select>
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-700 mb-1.5">
                  Опис інциденту чи обставин: <span className="text-rose-500">*</span>
                </label>
                <textarea
                  required
                  rows={4}
                  value={description}
                  onChange={(e) => setDescription(e.target.value)}
                  placeholder="Вкажіть факти, дату, місце або обставини події..."
                  className="w-full border border-slate-300 rounded-xl p-2.5 text-xs text-slate-800 bg-white focus:outline-none focus:ring-2 focus:ring-rose-500"
                />
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-700 mb-1.5">
                  Контакт для зворотного зв'язку (за бажанням):
                </label>
                <input
                  type="text"
                  value={contact}
                  onChange={(e) => setContact(e.target.value)}
                  placeholder="Номер телефону або email (необов'язково)"
                  className="w-full border border-slate-300 rounded-xl p-2.5 text-xs text-slate-800 bg-white focus:outline-none focus:ring-2 focus:ring-rose-500"
                />
                <span className="text-[11px] text-slate-500 mt-1 block">
                  Якщо поле порожнє, звернення залишається на 100% анонімним.
                </span>
              </div>

              <button
                type="submit"
                disabled={isSubmitting}
                className="w-full bg-rose-600 hover:bg-rose-700 disabled:opacity-50 text-white font-bold text-xs py-3 px-4 rounded-xl transition flex items-center justify-center gap-2 shadow-sm"
              >
                {isSubmitting ? (
                  <span>Надсилання...</span>
                ) : (
                  <>
                    <Send className="w-3.5 h-3.5" />
                    <span>Надіслати конфіденційно</span>
                  </>
                )}
              </button>
            </form>
          </div>
        </div>
      </div>
    </div>
  );
};
