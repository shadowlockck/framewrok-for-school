import React, { useState, useEffect } from 'react';
import { Eye, Type, Contrast, RotateCcw } from 'lucide-react';

export const AccessibilityBar: React.FC = () => {
  const [fontSize, setFontSize] = useState<'normal' | 'large' | 'xlarge'>('normal');
  const [contrast, setContrast] = useState<'normal' | 'inverted' | 'yellow-black'>('normal');
  const [isOpen, setIsOpen] = useState(false);

  useEffect(() => {
    const html = document.documentElement;
    html.classList.remove('font-size-large', 'font-size-xlarge');
    if (fontSize === 'large') html.classList.add('font-size-large');
    if (fontSize === 'xlarge') html.classList.add('font-size-xlarge');
  }, [fontSize]);

  useEffect(() => {
    const html = document.documentElement;
    html.classList.remove('contrast-inverted', 'contrast-yellow-black');
    if (contrast === 'inverted') html.classList.add('contrast-inverted');
    if (contrast === 'yellow-black') html.classList.add('contrast-yellow-black');
  }, [contrast]);

  const resetAccessibility = () => {
    setFontSize('normal');
    setContrast('normal');
  };

  return (
    <div className="bg-slate-900 text-white text-xs border-b border-slate-800">
      <div className="max-w-7xl mx-auto px-4 py-1.5 flex items-center justify-between">
        <div className="flex items-center gap-2">
          <button
            onClick={() => setIsOpen(!isOpen)}
            className="flex items-center gap-1.5 px-2 py-0.5 rounded bg-slate-800 hover:bg-slate-700 transition font-medium focus:ring-2 focus:ring-amber-400"
            aria-label="Налаштування доступності для людей з порушенням зору"
          >
            <Eye className="w-3.5 h-3.5 text-amber-400" />
            <span>Версія для людей з порушенням зору (WCAG 2.1)</span>
          </button>
        </div>

        {isOpen && (
          <div className="flex flex-wrap items-center gap-3">
            {/* Розмір шрифту */}
            <div className="flex items-center gap-1">
              <Type className="w-3.5 h-3.5 text-slate-400 mr-1" />
              <button
                onClick={() => setFontSize('normal')}
                className={`px-2 py-0.5 rounded text-xs ${fontSize === 'normal' ? 'bg-amber-500 text-slate-950 font-bold' : 'bg-slate-800'}`}
              >
                A
              </button>
              <button
                onClick={() => setFontSize('large')}
                className={`px-2 py-0.5 rounded text-sm ${fontSize === 'large' ? 'bg-amber-500 text-slate-950 font-bold' : 'bg-slate-800'}`}
              >
                A+
              </button>
              <button
                onClick={() => setFontSize('xlarge')}
                className={`px-2 py-0.5 rounded text-base ${fontSize === 'xlarge' ? 'bg-amber-500 text-slate-950 font-bold' : 'bg-slate-800'}`}
              >
                A++
              </button>
            </div>

            {/* Контрастність */}
            <div className="flex items-center gap-1">
              <Contrast className="w-3.5 h-3.5 text-slate-400 mr-1" />
              <button
                onClick={() => setContrast('normal')}
                className={`px-2 py-0.5 rounded ${contrast === 'normal' ? 'bg-amber-500 text-slate-950 font-bold' : 'bg-slate-800'}`}
              >
                Стандарт
              </button>
              <button
                onClick={() => setContrast('inverted')}
                className={`px-2 py-0.5 rounded ${contrast === 'inverted' ? 'bg-amber-500 text-slate-950 font-bold' : 'bg-slate-800'}`}
              >
                Ч/Б
              </button>
              <button
                onClick={() => setContrast('yellow-black')}
                className={`px-2 py-0.5 rounded ${contrast === 'yellow-black' ? 'bg-amber-500 text-slate-950 font-bold' : 'bg-slate-800'}`}
              >
                Ж/Ч
              </button>
            </div>

            {/* Скинути */}
            <button
              onClick={resetAccessibility}
              className="flex items-center gap-1 text-slate-400 hover:text-white ml-2"
              title="Скинути налаштування"
            >
              <RotateCcw className="w-3 h-3" />
              <span>Скинути</span>
            </button>
          </div>
        )}
      </div>
    </div>
  );
};
