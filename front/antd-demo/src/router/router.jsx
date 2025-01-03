import { createBrowserRouter, Navigate } from "react-router-dom";
import RootLayout from "../layout/root-layout";
import TestRoute from "../TestRoute";
import ArticlesSearchResultPage from "../modules/articles/pages/articles-search-result-page/articles-search-result-page";
import WikiRecommendationPage from "../modules/wiki/pages/wiki-recommendation-page/wiki-recommendation-page";
import ArticlePage from "../modules/articles/pages/article-page/article-page";
import WikiMainPage from "../modules/wiki/pages/wiki-main-page/wiki-main-page";
import EditArticlePage from "../modules/articles/pages/edit-article-page/edit-article-page";
import CreateArticlePage from "../modules/articles/pages/create-article-page/create-article-page";
import WikiEditPage from "../modules/wiki/pages/wiki-edit-page/wiki-edit-page";
import WikiCreatePage from "../modules/wiki/pages/wiki-create-page/wiki-create-page";
import NotFoundPage from "../modules/wiki/pages/wiki-not-found/wiki-not-found";
import WikiSearchResultsPage from "../modules/wiki/pages/wiki-search-results-page/wiki-search-results-page";
import UserPage from "../modules/users/pages/UserPage";

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
      // { path: "", element: <WikiRecommendationPage /> }, // Página principal
      { path: "user_not_found", element: <NotFoundPage status_code={404} resource_type="User" /> }, // Usuario no encontrado
      { path: "wiki_not_found", element: <NotFoundPage status_code={404} resource_type="Wiki" /> },
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
              { path: "article_not_found", element: <NotFoundPage status_code={404} resource_type="Article" /> },
              {
                path: "articles",
                children: [
                  { path: "new", element: <CreateArticlePage /> }, // Crear artículo
                  { path: ":article_name", element: <ArticlePage/> }, // Ver artículo
                  { path: ":article_name/edit", element: <EditArticlePage/> }, // Editar artículo
                  { path: "*", element: <Navigate to="not_found" relative replace/> }, // Página no encontrada
                ],
              },
            ],
          },
          {
            path: "*", element: <Navigate to="not_found" relative replace/>,
          }
        ],
      },
      {
        path: "users",
        children: [
          { path: ":user_id", element: <UserPage /> }, // Página de usuario
        ]
      },
      { path: "testing", element: <TestRoute /> }, // Ruta de testing
    ],
  },
  { path: "/login", element: <TestRoute /> },
  { path: "/register", element: <TestRoute /> },
  { path: "*", element: <NotFoundPage status_code={404} resource_type="Page" /> }, // Página no encontrada
]);

export default router;
