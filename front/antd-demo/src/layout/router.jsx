import { createBrowserRouter} from "react-router-dom";
import RootLayout from "./root-layout";
import TestRoute from "../TestRoute";

// La estructura de las rutas de la aplicación

// El element en el objeto raiz define el layout principal (el header)
// Su children es el contenido que se renderiza en el Outlet
// Se defininen, a su vez, subrutas para cada tipo de contenido

// Las subrutas no tienen element, asi que renderizan el
// contenido de los hijos

// Detectado un problema que las rutas raiz se renderizan
// a pesar de que no tienen ningun componente asociado
// No debe importar, pues no se va a acceder a ellas de manera normal

// Se ha definido una ruta de testing para probar ahi los componentes
// y no tener que manchar el app con componentes de prueba
const router = createBrowserRouter([
    {
      path: "/",
      element: <RootLayout />,
      children: [
        { path: "/", element: <TestRoute /> },
        {
          path: "wikis",
          children: [
            {
              path: ":wiki_id/search",
              element: <TestRoute />,
            },
            {
              path: ":wiki_id/edit",
              element: <TestRoute />,
            },
            {
              path: ":wiki_id/articles",
              children: [
                {
                  path: "search",
                  element: <TestRoute />,
                },
                {
                  path: ":article_id/edit",
                  element: <TestRoute />,
                },
                {
                  path: ":article_id",
                  element: <TestRoute />,
                },
              ],
            },
            {
              path: ":wiki_id",
              element: <TestRoute />,
            },
          ],
        },
        {
            path: "testing",
            element: <TestRoute />,
        }
      ],
    },
    {
      path: "/login",
      element: <TestRoute />,
    },
    {
      path: "/register",
      element: <TestRoute />,
    },
  ]
);

export default router;