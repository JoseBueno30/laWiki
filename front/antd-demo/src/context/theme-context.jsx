import { ConfigProvider, theme } from "antd";
import { createContext, useState } from "react";

export const ThemeContext = createContext();

export const ThemeProvider = ({ children }) => {
  const [colorTheme, setTheme] = useState("light");

  const toggleTheme = () => {
    setTheme((prevTheme) => (prevTheme === "light" ? "dark" : "light"));
  };

  return (
    <ThemeContext.Provider value={{ colorTheme, toggleTheme }}>
      <ConfigProvider
        theme={{
          cssVar: true,
          algorithm:
            colorTheme === "light"
              ? theme.defaultAlgorithm
              : theme.darkAlgorithm,
        }}
      >
        {children}
      </ConfigProvider>
    </ThemeContext.Provider>
  );
};

export default ThemeProvider;
