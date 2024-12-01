import { useLocation } from "react-router-dom";
import { Button } from "antd";
import { useContext } from "react";
import { SettingsContext } from "./context/settings-context";

import ArticleList from "./modules/articles/components/article-list/article-list";
import WikiEditPage from "./modules/wiki/pages/wiki-edit-page/wiki-edit-page";
import ArticleEditPage from "./modules/articles/pages/article-edit-page/article-edit-page";
import RatingsList from "./modules/articles/components/ratings-list";
import RatingsSection from "./modules/articles/components/ratings-section";

const TestRoute = () => {
  const { colorTheme, toggleTheme } = useContext(SettingsContext);

    

  let location = useLocation();

  return (
    <>
      <h1>{location.pathname}</h1>
      <Button onClick={toggleTheme}>Toggle theme</Button>
      <RatingsSection/>
    </>
  );
};

export default TestRoute;
