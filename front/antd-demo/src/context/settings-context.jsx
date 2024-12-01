import { ConfigProvider, theme } from "antd";
import { createContext, useState } from "react";
import enUS from 'antd/es/locale/en_US';
import esES from 'antd/es/locale/es_ES';
import frFR from 'antd/es/locale/fr_FR';
import i18n from "../i18n";

export const SettingsContext = createContext();

const locales = {
  en: enUS,
  es: esES,
  fr: frFR,
};

export const SettingsProvider = ({ children }) => {
  const [colorTheme, setTheme] = useState(localStorage.getItem("theme") || "light");
  const [locale, setLocale] = useState(localStorage.getItem("locale") || "en");

  const toggleTheme = (newTheme) => {
    if(newTheme === "light" || newTheme === "dark"){
      setTheme(newTheme);
      localStorage.setItem("theme", newTheme);
    }
  };

  const changeLocale = (newLocale) => {
    localStorage.setItem("locale", newLocale);
    setLocale(newLocale);
    i18n.changeLanguage(newLocale);
  }
  return (
    <SettingsContext.Provider value={{ colorTheme, locale, toggleTheme, changeLocale }}>
      <ConfigProvider
        theme={{
          cssVar: true,
          algorithm:
            colorTheme === "light"
              ? theme.defaultAlgorithm
              : theme.darkAlgorithm,
        }}
        locale={locales[locale]}
      >
        {children}
      </ConfigProvider>
    </SettingsContext.Provider>
  );
};

export default SettingsContext;
