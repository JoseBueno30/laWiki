import { ConfigProvider, theme } from "antd";
import { createContext, useState } from "react";
import enUS from 'antd/es/locale/en_US';
import esES from 'antd/es/locale/es_ES';
import frFR from 'antd/es/locale/fr_FR';

export const ThemeContext = createContext();

const locales = {
  en: enUS,
  es: esES,
  fr: frFR,
};

export const ThemeProvider = ({ children }) => {
  const [colorTheme, setTheme] = useState("light");
  const [locale, setLocale] = useState("en");

  const toggleTheme = () => {
    setTheme((prevTheme) => (prevTheme === "light" ? "dark" : "light"));
  };

  const changeLocale = (newLocale) => {
    setLocale(newLocale);
  }
  return (
    <ThemeContext.Provider value={{ colorTheme, locale, toggleTheme, changeLocale }}>
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
    </ThemeContext.Provider>
  );
};

export default ThemeProvider;
