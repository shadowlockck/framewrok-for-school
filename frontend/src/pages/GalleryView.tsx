import React from 'react';
import { Image, Calendar, Camera } from 'lucide-react';

interface Album {
  id: string;
  title: string;
  date: string;
  description: string;
  photoCount: number;
}

const ALBUMS: Album[] = [
  {
    id: '1',
    title: 'Свято Першого дзвоника та посвята першокласників у НУШ',
    date: '01.09.2026',
    description: 'Урочиста зустріч нового навчального року, святковий квест «Стежками знань» для перших класів.',
    photoCount: 24,
  },
  {
    id: '2',
    title: 'День захисників і захисниць України: благодійний ярмарок',
    date: '01.10.2026',
    description: 'Шкільний ярмарок учнівського самоврядування на підтримку Збройних Сил України.',
    photoCount: 38,
  },
  {
    id: '3',
    title: 'Відкриття інноваційної STEM-лабораторії та комп’ютерного класу',
    date: '15.09.2026',
    description: 'Презентація сучасних 3D-принтерів, наборів робототехніки та цифрових мікроскопів.',
    photoCount: 16,
  },
];

export const GalleryView: React.FC = () => {
  return (
    <div className="py-8 max-w-7xl mx-auto px-4">
      {/* Title */}
      <div className="bg-gradient-to-r from-purple-900 to-slate-900 text-white rounded-2xl p-6 md:p-8 mb-8 shadow-lg">
        <div className="inline-flex items-center gap-2 bg-purple-800 px-3 py-1 rounded-full text-xs font-semibold uppercase tracking-wider text-purple-200 mb-3">
          <Image className="w-4 h-4" />
          <span>Фотохроніка</span>
        </div>
        <h2 className="text-2xl md:text-3xl font-extrabold tracking-tight mb-2">
          Фотогалерея та яскраві миті шкільного життя
        </h2>
        <p className="text-purple-100 text-sm md:text-base max-w-3xl leading-relaxed">
          Тематичні фотоальбоми святкових подій, спортивних турнірів, олімпіад та навчальних буднів.
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {ALBUMS.map((album) => (
          <div
            key={album.id}
            className="bg-white rounded-xl overflow-hidden border border-slate-200 shadow-sm hover:shadow-md transition flex flex-col justify-between"
          >
            <div className="h-44 bg-gradient-to-tr from-indigo-100 to-purple-50 flex flex-col items-center justify-center p-4 text-purple-800 relative">
              <Camera className="w-12 h-12 mb-2 text-purple-400" />
              <span className="text-xs font-semibold bg-white/80 px-2.5 py-1 rounded-full text-slate-700 shadow-sm">
                {album.photoCount} світлин
              </span>
            </div>

            <div className="p-5 flex-1 flex flex-col justify-between">
              <div>
                <span className="text-xs text-slate-400 font-mono flex items-center gap-1 mb-2">
                  <Calendar className="w-3.5 h-3.5" />
                  {album.date}
                </span>
                <h3 className="font-bold text-slate-900 text-base mb-2 leading-snug">{album.title}</h3>
                <p className="text-slate-600 text-xs leading-relaxed">{album.description}</p>
              </div>

              <div className="pt-4 mt-4 border-t border-slate-100">
                <button
                  onClick={() => alert(`Перегляд альбому: ${album.title}`)}
                  className="w-full py-2 bg-slate-100 hover:bg-purple-600 hover:text-white rounded-lg text-xs font-medium text-slate-700 transition"
                >
                  Переглянути світлини
                </button>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
