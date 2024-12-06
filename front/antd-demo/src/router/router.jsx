import { createBrowserRouter } from "react-router-dom";
import RootLayout from "../layout/root-layout";
import TestRoute from "../TestRoute";
import ArticlesSearchResultPage from "../modules/articles/pages/articles-search-result-page/articles-search-result-page";
import WikiRecommendationPage from "../modules/wiki/pages/wiki-recommendation-page/wiki-recommendation-page";
import ArticlePage from "../modules/articles/pages/article-page/article-page";
import WikiMainPage from "../modules/wiki/pages/wiki-main-page/wiki-main-page";
import WikiEditPage from "../modules/wiki/pages/wiki-edit-page/wiki-edit-page";
import WikiCreatePage from "../modules/wiki/pages/wiki-create-page/wiki-create-page";
import ArticleEditPage from "../modules/articles/pages/article-edit-page/article-edit-page";
import WikiSearchResultsPage from "../modules/wiki/pages/wiki-search-results-page/wiki-search-results-page";

// The structure of the application's routes

// The element in the root object defines the main layout (the header)
// Its children represent the content rendered in the Outlet
// Additionally, subroutes are defined for each type of content

// The subroutes have no element, so they render
// the content of their children

// A problem was detected: the root routes are rendered
// even though they don't have any associated component
// It shouldn't matter since they won't be accessed normally

// A testing route has been defined to test components there
// without cluttering the app with test components
const router = createBrowserRouter([
  {
    path: "/",
    element: <RootLayout />,
    children: [
      { path: "", element: <WikiRecommendationPage /> }, // Página principal
      {
        path: "wikis",
        children: [
          { path: "search", element: <WikiSearchResultsPage/> }, // Buscar wikis
          { path: "new", element: <WikiCreatePage /> }, // Crear wiki
          {
            path: ":wiki_name",
            children: [
              { path: "", element: <WikiMainPage /> }, // Página principal de la wiki
              { path: "edit", element: <WikiEditPage /> }, // Editar wiki
              { path: "search", element: <ArticlesSearchResultPage /> }, // Buscar artículos en la wiki
              {
                path: "articles",
                children: [
                  { path: "new", element: <TestRoute /> }, // Crear artículo
                  { path: ":article_name", element: <ArticlePage/> }, // Ver artículo
                  { path: ":article_name/edit", element: <ArticleEditPage /> }, // Editar artículo
                ],
              },
            ],
          },
        ],
      },
      { path: "testing", element: <TestRoute /> }, // Ruta de testing
    ],
  },
  { path: "/login", element: <TestRoute /> },
  { path: "/register", element: <TestRoute /> },
]);

export default router;
