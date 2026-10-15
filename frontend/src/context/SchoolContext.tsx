import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import { fetchFromAPI } from '../api/client';

export interface SchoolTheme {
  primary_color: string;
  primary_hover: string;
  secondary_color: string;
  accent_color: string;
  font_family: string;
}

export interface SchoolProfile {
  name: string;
  short_name: string;
  edrpou: string;
  founder: string;
  address: string;
  phone: string;
  email: string;
  website?: string;
  licensed_capacity: number;
  actual_students: number;
  education_language: string;
  logo?: string | null;
  theme?: SchoolTheme;
}

export interface ModulesState {
  legal: boolean;
  admissions: boolean;
  nutrition: boolean;
  safety: boolean;
  news: boolean;
  schedule: boolean;
  gallery: boolean;
  [key: string]: boolean;
}

export interface NavigationItem {
  id: string;
  title: string;
  icon: string;
}

export interface SchoolManifest {
  school: SchoolProfile;
  modules: ModulesState;
  navigation: NavigationItem[];
  compliance: {
    article_30: boolean;
    wcag_version: string;
    privacy_law_enforced: boolean;
    financial_deadline_days: number;
  };
}

const DEFAULT_MANIFEST: SchoolManifest = {
  school: {
    name: 'Офіційний вебсайт закладу освіти',
    short_name: 'Заклад освіти',
    edrpou: '12345678',
    founder: 'Орган місцевого самоврядування',
    address: 'вул. Освітня, 1, м. Київ',
    phone: '+380 44 123-45-67',
    email: 'school@osvita.kyiv.ua',
    licensed_capacity: 1000,
    actual_students: 920,
    education_language: 'Українська',
    theme: {
      primary_color: '#1e3a8a',
      primary_hover: '#172554',
      secondary_color: '#059669',
      accent_color: '#d97706',
      font_family: 'Inter, system-ui, sans-serif',
    },
  },
  modules: {
    legal: true,
    admissions: true,
    nutrition: true,
    safety: true,
    news: true,
    schedule: true,
    gallery: true,
  },
  navigation: [
    { id: 'legal', title: 'Прозорість (ст. 30)', icon: 'FileCheck' },
    { id: 'finance', title: 'Кошторис та звітність', icon: 'DollarSign' },
    { id: 'admissions', title: 'Вступ та зарахування', icon: 'Users' },
    { id: 'schedule', title: 'Розклад', icon: 'Calendar' },
    { id: 'nutrition', title: 'Харчування', icon: 'Utensils' },
    { id: 'safety', title: 'Безпека та булінг', icon: 'ShieldAlert' },
    { id: 'news', title: 'Новини', icon: 'Newspaper' },
    { id: 'gallery', title: 'Галерея', icon: 'Image' },
  ],
  compliance: {
    article_30: true,
    wcag_version: '2.1 AA',
    privacy_law_enforced: true,
    financial_deadline_days: 10,
  },
};

interface SchoolContextValue {
  manifest: SchoolManifest;
  school: SchoolProfile;
  modules: ModulesState;
  navigation: NavigationItem[];
  isLoading: boolean;
  refetch: () => Promise<void>;
}

const SchoolContext = createContext<SchoolContextValue>({
  manifest: DEFAULT_MANIFEST,
  school: DEFAULT_MANIFEST.school,
  modules: DEFAULT_MANIFEST.modules,
  navigation: DEFAULT_MANIFEST.navigation,
  isLoading: false,
  refetch: async () => {},
});

export const SchoolFrameworkProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const [manifest, setManifest] = useState<SchoolManifest>(DEFAULT_MANIFEST);
  const [isLoading, setIsLoading] = useState<boolean>(true);

  const loadManifest = async () => {
    setIsLoading(true);
    try {
      const data = await fetchFromAPI<SchoolManifest>('/core/manifest/', DEFAULT_MANIFEST);
      if (data && data.school) {
        setManifest(data);
        // Apply dynamic theme CSS variables if provided
        if (data.school.theme) {
          const root = document.documentElement;
          if (data.school.theme.primary_color) {
            root.style.setProperty('--color-primary', data.school.theme.primary_color);
          }
          if (data.school.theme.secondary_color) {
            root.style.setProperty('--color-secondary', data.school.theme.secondary_color);
          }
          if (data.school.theme.accent_color) {
            root.style.setProperty('--color-accent', data.school.theme.accent_color);
          }
        }
      }
    } catch (e) {
      console.warn('Failed to load school manifest, using defaults:', e);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    loadManifest();
  }, []);

  return (
    <SchoolContext.Provider
      value={{
        manifest,
        school: manifest.school,
        modules: manifest.modules,
        navigation: manifest.navigation,
        isLoading,
        refetch: loadManifest,
      }}
    >
      {children}
    </SchoolContext.Provider>
  );
};

export const useSchool = () => useContext(SchoolContext).school;
export const useModules = () => useContext(SchoolContext).modules;
export const useNavigation = () => useContext(SchoolContext).navigation;
export const useSchoolFramework = () => useContext(SchoolContext);
