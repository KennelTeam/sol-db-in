import i18nnext, { i18n } from "i18next";
import I18nextBrowserLanguageDetector from "i18next-browser-languagedetector";
import Backend from 'i18next-http-backend';
import { initReactI18next } from "react-i18next";

i18nnext
  .use(Backend)  // loads translations from json files in public/locales
  .use(I18nextBrowserLanguageDetector)
  .use(initReactI18next) // passes i18n down to react-i18next
  .init({
    interpolation: {
      escapeValue: false // react already safes from xss
    }
  });

export default i18nnext;
