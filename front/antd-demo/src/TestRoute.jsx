import { useLocation } from "react-router-dom";
import { Button } from "antd";
import { useContext } from "react";
import { SettingsContext } from "./context/settings-context";

import ArticleList from "./modules/articles/components/article-list/article-list";
import EditWikiPage from "./modules/wiki/pages/wiki-edit-page/wiki-edit-page";
import ArticleEditPage from "./modules/articles/pages/edit-article-page/edit-article-page";
import WikiCreatePage from "./modules/wiki/pages/wiki-create-page/wiki-create-page";
import NotFoundPage from "./modules/wiki/pages/wiki-not-found/wiki-not-found";
import UserPage from "./modules/users/pages/UserPage";

const TestRoute = () => {
  const { colorTheme, toggleTheme } = useContext(SettingsContext);

    

  let location = useLocation();

  return (
    <>
      {/* <h1>{location.pathname}</h1>
      <Button onClick={toggleTheme}>Toggle theme</Button>
      <RatingsSection/> */}
      {/*<WikiCreatePage></WikiCreatePage>*/}
      {/*<NotFoundPage status_code={404} error_message={"Test message"}></NotFoundPage>*/}
      {<UserPage></UserPage>}
      {/* <WikiEditPage></WikiEditPage> */}
      {/* <ArticleEditPage></ArticleEditPage> */}
    </>
  );
};

export default TestRoute;
