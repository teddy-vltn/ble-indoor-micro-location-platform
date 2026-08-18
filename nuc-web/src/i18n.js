import i18n from 'i18next';
import { initReactI18next } from 'react-i18next';
import Backend from 'i18next-http-backend';
import LanguageDetector from 'i18next-browser-languagedetector';

i18n
    .use(Backend)
    .use(initReactI18next)
    .use(LanguageDetector)
    .init({
        supportedLngs: ['en', 'fr'],
        fallbackLng: 'en',
        lng: 'fr',
        backend: {
            loadPath: '/locales/{{lng}}/{{ns}}.json'
        },
        react: {
            useSuspense: true
        },
        interpolation: {
            escapeValue: false 
        },
        detection: {
            // Options for language detection
            order: ['querystring', 'cookie', 'localStorage', 'navigator', 'htmlTag', 'path', 'subdomain'],
            caches: ['localStorage', 'cookie'],
        }
    });

export default i18n;
