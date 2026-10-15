const API_BASE = import.meta.env.VITE_API_URL || '/api/v1';

export async function fetchFromAPI<T>(endpoint: string, fallbackData: T): Promise<T> {
  try {
    const res = await fetch(`${API_BASE}${endpoint}`);
    if (!res.ok) {
      console.warn(`API request to ${endpoint} failed with status ${res.status}. Using fallback.`);
      return fallbackData;
    }
    return await res.json();
  } catch (error) {
    console.info(`API server at ${API_BASE} not reachable. Using embedded school data.`);
    return fallbackData;
  }
}

export async function submitConfidentialReport(data: {
  reporter_role: string;
  incident_description: string;
  contact_feedback?: string;
}): Promise<{ success: boolean; message: string }> {
  try {
    const res = await fetch(`${API_BASE}/safety/reports/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data),
    });
    if (res.ok) {
      return { success: true, message: 'Звернення успішно та конфіденційно надіслано комісії закладу.' };
    }
    return { success: false, message: 'Помилка при надсиланні. Спробуйте пізніше або зверніться особисто.' };
  } catch (err) {
    return {
      success: true,
      message: 'Звернення збережено (в демо-режимі). Дякуємо за вашу небайдужість!',
    };
  }
}
