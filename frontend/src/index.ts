// ==========================================================
// School Website Framework — Frontend Component Kit & SDK
// ==========================================================

// Context and Hooks
export {
  SchoolFrameworkProvider,
  useSchool,
  useModules,
  useNavigation,
  useSchoolFramework,
} from './context/SchoolContext';
export type {
  SchoolProfile,
  SchoolTheme,
  ModulesState,
  NavigationItem,
  SchoolManifest,
} from './context/SchoolContext';

// Navigation & Core Components
export { Header } from './components/Header';
export { AccessibilityBar } from './components/AccessibilityBar';

// Legal & Compliance Views (Article 30 Law on Education)
export { LegalRegisterView } from './pages/LegalRegisterView';
export { FinancialTransparencyView } from './pages/FinancialTransparencyView';
export { AdmissionsView } from './pages/AdmissionsView';
export { SafetyView } from './pages/SafetyView';

// School Life Modules
export { NutritionView } from './pages/NutritionView';
export { ScheduleView } from './pages/ScheduleView';
export { NewsView } from './pages/NewsView';
export { GalleryView } from './pages/GalleryView';

// API Client
export { fetchFromAPI, submitConfidentialReport } from './api/client';
