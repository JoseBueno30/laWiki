import { createBrowserRouter } from "react-router-dom";
import RootLayout from "../layout/root-layout";
import TestRoute from "../TestRoute";
import WikiRecommendationPage from "../modules/wiki/pages/wiki-recommendation-page/wiki-recommendation-page";
import ArticlePage from "../modules/articles/pages/article-page/article-page";

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
          { path: "search", element: <TestRoute /> }, // Buscar wikis
          { path: "new", element: <TestRoute /> }, // Crear wiki
          {
            path: ":wiki_name",
            children: [
              { path: "", element: <TestRoute /> }, // Página principal de la wiki
              { path: "edit", element: <TestRoute /> }, // Editar wiki
              { path: "search", element: <TestRoute /> }, // Buscar artículos en la wiki
              {
                path: "articles",
                children: [
                  { path: "new", element: <TestRoute /> }, // Crear artículo
                  { path: ":article_name", element: <ArticlePage/> }, // Ver artículo
                  { path: ":article_name/edit", element: <TestRoute /> }, // Editar artículo
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
