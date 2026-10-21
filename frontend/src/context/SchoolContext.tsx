import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import { fetchManifest } from '../api/client';

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
    edrpou: '',
    founder: 'Орган місцевого самоврядування',
    address: '',
    phone: '',
    email: '',
    licensed_capacity: 0,
    actual_students: 0,
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
    legal: false,
    admissions: false,
    nutrition: false,
    safety: false,
    news: false,
    schedule: false,
    gallery: false,
  },
  navigation: [],
  compliance: {
    article_30: false,
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
  error: string | null;
  refetch: () => Promise<void>;
}

const SchoolContext = createContext<SchoolContextValue>({
  manifest: DEFAULT_MANIFEST,
  school: DEFAULT_MANIFEST.school,
  modules: DEFAULT_MANIFEST.modules,
  navigation: DEFAULT_MANIFEST.navigation,
  isLoading: false,
  error: null,
  refetch: async () => {},
});

export const SchoolFrameworkProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const [manifest, setManifest] = useState<SchoolManifest>(DEFAULT_MANIFEST);
  const [isLoading, setIsLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  const loadManifest = async () => {
    setIsLoading(true);
    setError(null);
    try {
      const data = await fetchManifest<SchoolManifest>();
      if (data && data.school && data.modules && Array.isArray(data.navigation)) {
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
      } else throw new Error('Invalid manifest');
    } catch (e) {
      setManifest(DEFAULT_MANIFEST);
      setError('Не вдалося завантажити дані школи. Перевірте підключення до сервера.');
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
        error,
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
